"""Render the FINAL cell-heightfield solids used by the printable-model STL export.

Only NumPy and Pillow are required. No source primitives, interpolation, TCAD
fields, inferred electrical currents, or material cross-sections are drawn.

    python printable-models/build_preview.py
    python printable-models/build_preview.py --ids V1_01 V2_01 --no-contact-sheets

The catalogue is a JSON array. Each entry needs print_id and name_en. Optional
fields: group (or version), heightfield, pitch_mm, base_mm, size_mm. Heightfields
are positive finite cell-top heights in mm, shape (ny, nx), with bottom z=0.
The engine's 0.4-mm pitch is the default. Each cell has a FLAT top; discontinuous
neighbouring heights have vertical walls. The preview uses those same cells.

Paths default to this script's directory and are independent of the user's cwd.
Output: previews/{id}.png and {id}_top.png, grouped contact sheets, and
preview_manifest.json. Both views use the same saved final heightfield.
"""
from __future__ import annotations

import argparse
from collections import defaultdict
from functools import lru_cache
import hashlib
import io
import json
import math
import os
from pathlib import Path
import re
import sys

import numpy as np
from PIL import Image, ImageDraw, ImageFilter, ImageFont


HERE = Path(__file__).resolve().parent
BG = (245, 248, 251)
INK = (26, 49, 72)
MUTED = (88, 107, 123)
PALETTE = np.asarray([
    [157, 181, 205], [81, 151, 172], [71, 168, 151],
    [228, 186, 87], [224, 117, 83],
], dtype=float)


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for block in iter(lambda: stream.read(1 << 20), b""):
            digest.update(block)
    return digest.hexdigest()


@lru_cache(maxsize=48)
def font(size: int, bold: bool = False) -> ImageFont.ImageFont:
    """Use common OS fonts, with Pillow's portable default as the last fallback."""
    windows = Path(os.environ.get("WINDIR", "C:/Windows")) / "Fonts"
    candidates = [
        windows / ("segoeuib.ttf" if bold else "segoeui.ttf"),
        "DejaVuSans-Bold.ttf" if bold else "DejaVuSans.ttf",
        "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf" if bold
        else "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf",
    ]
    for candidate in candidates:
        try:
            return ImageFont.truetype(str(candidate), size)
        except (OSError, ValueError):
            pass
    return ImageFont.load_default(size=size)


def wrap(draw: ImageDraw.ImageDraw, value: str, face, width: int) -> list[str]:
    lines, current = [], ""
    for word in str(value).split():
        candidate = f"{current} {word}".strip()
        if current and draw.textlength(candidate, font=face) > width:
            lines.append(current)
            current = word
        else:
            current = candidate
    if current:
        lines.append(current)
    return lines or [""]


def shade(rgb, factor: float) -> tuple[int, int, int]:
    return tuple(int(round(max(0, min(255, c * factor)))) for c in rgb)


def height_colors(heights: np.ndarray, bottom: float, top: float) -> np.ndarray:
    """Color encodes printed relief height only, never material or field strength."""
    t = np.clip((heights - bottom) / max(top - bottom, 1e-12), 0.0, 1.0)
    position = t * (len(PALETTE) - 1)
    lower = np.minimum(position.astype(int), len(PALETTE) - 2)
    fraction = (position - lower)[..., None]
    rgb = PALETTE[lower] * (1.0 - fraction) + PALETTE[lower + 1] * fraction
    return np.rint(rgb).astype(np.uint8)


def canonical_group(record: dict) -> str:
    value = str(record.get("group") or record.get("version")
                or record.get("source_version") or "")
    compact = re.sub(r"[^A-Z0-9]", "", value.upper())
    if compact in {"V33", "V330", "33", "V3"}:
        return "V33"
    if compact in {"V1", "1", "V10"}:
        return "V1"
    if compact in {"V2", "2", "V20"}:
        return "V2"
    identifier = str(record["print_id"]).upper()
    if identifier.startswith(("V33", "V3_", "V3-")):
        return "V33"
    for prefix in ("V1", "V2"):
        if identifier.startswith(prefix):
            return prefix
    return re.sub(r"[^A-Za-z0-9_-]", "_", value or "Other")


def input_path(record: dict, root: Path) -> Path:
    value = record.get("heightfield") or record.get("heightfield_path")
    if not value:
        return root / "heightfields" / f"{record['print_id']}.npy"
    path = Path(str(value).replace("\\", "/"))
    if path.is_absolute():
        return path
    local = root / path
    if local.is_file():
        return local
    # A catalogue may deliberately store repository-relative paths.
    return root.parent / path


def checked_geometry(record: dict, root: Path) -> tuple[np.ndarray, dict]:
    path = input_path(record, root)
    source_bytes = path.read_bytes()
    heightfield = np.load(io.BytesIO(source_bytes), allow_pickle=False)
    if heightfield.ndim != 2 or not heightfield.size:
        raise ValueError(f"{record['print_id']}: expected a nonempty (ny,nx) heightfield")
    if not np.issubdtype(heightfield.dtype, np.number):
        raise ValueError(f"{record['print_id']}: heightfield is not numeric")
    heights = np.asarray(heightfield, dtype=np.float64)
    if not np.all(np.isfinite(heights)) or np.any(heights <= 0):
        raise ValueError(f"{record['print_id']}: heights must be positive and finite")
    pitch = record.get("pitch_mm")
    if pitch is None:
        pitch = 0.4
    if isinstance(pitch, (list, tuple)):
        dx, dy = map(float, pitch[:2])
    else:
        dx = dy = float(pitch)
    if not (dx > 0 and dy > 0):
        raise ValueError(f"{record['print_id']}: pitch must be positive")
    ny, nx = heights.shape
    physical = [float(nx * dx), float(ny * dy), float(heights.max())]
    supplied = record.get("size_mm")
    if isinstance(supplied, dict):
        supplied = [supplied.get(k) for k in ("width", "depth", "height")]
    if supplied and len(supplied) >= 2:
        for axis, expected in enumerate(supplied[:3]):
            if expected is not None and not math.isclose(
                float(expected), physical[axis], rel_tol=1e-8, abs_tol=1e-7
            ):
                raise ValueError(
                    f"{record['print_id']}: size_mm disagrees with final heightfield "
                    f"on axis {axis}: {expected} vs {physical[axis]}"
                )
    return heights, dict(path=path, dx=dx, dy=dy, size_mm=physical,
                         shape=list(heights.shape), minimum_top_mm=float(heights.min()),
                         sha256=hashlib.sha256(source_bytes).hexdigest())


def render_preview(heights: np.ndarray, record: dict, geometry: dict,
                   size: tuple[int, int] = (1100, 850), supersample: int = 2) -> Image.Image:
    """Render exact flat-topped cell geometry by orthographic depth ordering.

    The camera looks from +X,-Y,+Z at elevation atan(1/sqrt(2)), so the
    front-edge embossed text is seen from its reading side. Forward walls
    are +X and -Y faces where the adjacent cell is lower. Vertical columns
    are drawn back-to-front in increasing X-Y order. Every shared sightline
    crosses the columns in this order. No per-vertex interpolation is used.
    """
    scale_image = supersample
    W, H = size
    canvas = Image.new("RGB", (W * scale_image, H * scale_image), BG)
    draw = ImageDraw.Draw(canvas)
    def f(points):
        return [(int(round(x * scale_image)), int(round(y * scale_image))) for x, y in points]
    def text(x, y, value, sz=18, color=INK, bold=False, anchor=None):
        draw.text((int(x * scale_image), int(y * scale_image)), str(value),
                  font=font(max(1, int(sz * scale_image)), bold), fill=color, anchor=anchor)

    group = canonical_group(record)
    text(38, 21, f"{group}  /  {record['print_id']}", 16, MUTED, True)
    title = str(record.get("name_en") or record["print_id"])
    title_size = 30
    title_font = font(title_size * scale_image, True)
    title_lines = wrap(draw, title, title_font, (W - 76) * scale_image)
    while len(title_lines) > 2 and title_size > 20:
        title_size -= 1
        title_font = font(title_size * scale_image, True)
        title_lines = wrap(draw, title, title_font, (W - 76) * scale_image)
    for j, line in enumerate(title_lines):
        text(38, 47 + j * (title_size + 5), line, title_size, INK, True)
    heading_bottom = 47 + len(title_lines) * (title_size + 5)
    text(38, heading_bottom + 9, "ENLARGED CONCEPT / NOT TO SCALE", 17, (160, 87, 25), True)
    nx, ny = heights.shape[1], heights.shape[0]
    dx, dy = geometry["dx"], geometry["dy"]
    width, depth, zmax = geometry["size_mm"]
    zmin = float(heights.min())
    text(38, heading_bottom + 37,
         f"Printed envelope: {width:g} x {depth:g} x {zmax:g} mm", 18, MUTED)
    top = heading_bottom + 79
    bottom = H - 155
    if bottom - top < 230:
        raise ValueError("Preview canvas is too short for the complete title and solid")
    invsqrt2 = 1.0 / math.sqrt(2.0)
    sine = 1.0 / math.sqrt(3.0)
    cosine = math.sqrt(2.0 / 3.0)
    def raw_project(x, y, z):
        return ((x + y) * invsqrt2, (x - y) * sine * invsqrt2 - z * cosine)
    corners = [raw_project(x, y, z) for x in (0, width)
               for y in (0, depth) for z in (0, zmax)]
    xmin = min(p[0] for p in corners)
    xmax = max(p[0] for p in corners)
    ymin = min(p[1] for p in corners)
    ymax = max(p[1] for p in corners)
    zoom = min((W - 130) / (xmax - xmin), (bottom - top - 25) / (ymax - ymin))
    tx = W / 2 - zoom * (xmin + xmax) / 2
    ty = (top + bottom) / 2 - zoom * (ymin + ymax) / 2
    def project(x, y, z):
        u, v = raw_project(x, y, z)
        return (tx + zoom * u, ty + zoom * v)
    def polygon(points, color):
        draw.polygon(f([project(*p) for p in points]), fill=color)

    # A neutral footprint shadow is a graphic depth cue, not a physical field.
    shadow = Image.new("RGBA", canvas.size, (0, 0, 0, 0))
    sd = ImageDraw.Draw(shadow)
    footprint = [project(0, 0, 0), project(width, 0, 0),
                 project(width, depth, 0), project(0, depth, 0)]
    sd.polygon(f([(x + 5, y + 12) for x, y in footprint]), fill=(30, 55, 75, 50))
    shadow = shadow.filter(ImageFilter.GaussianBlur(11 * scale_image))
    canvas.paste(shadow, (0, 0), shadow)
    draw = ImageDraw.Draw(canvas)
    colors = height_colors(heights, zmin, zmax)
    # Render ALL final cells, including stair steps introduced by the repair.
    # Visible internal side walls span adjacent tops, not down through solids.
    cells = sorted(np.ndindex(ny, nx), key=lambda cell: cell[1] * dx - cell[0] * dy)
    for row, col in cells:
        x0, x1 = col * dx, (col + 1) * dx
        y0, y1 = row * dy, (row + 1) * dy
        z = float(heights[row, col])
        color = tuple(int(c) for c in colors[row, col])
        front_y = float(heights[row - 1, col]) if row > 0 else 0.0
        front_x = float(heights[row, col + 1]) if col + 1 < nx else 0.0
        if z > front_y:
            polygon([(x0, y0, front_y), (x1, y0, front_y),
                     (x1, y0, z), (x0, y0, z)], shade(color, 0.66))
        if z > front_x:
            polygon([(x1, y0, front_x), (x1, y1, front_x),
                     (x1, y1, z), (x1, y0, z)], shade(color, 0.82))
        polygon([(x0, y0, z), (x1, y0, z), (x1, y1, z), (x0, y1, z)], color)

    # Camera orientation is explicit; these are geometric axes, not current arrows.
    ax, ay, length = W - 100, bottom - 10, 43
    axis_end = {
        "X": (ax + length * invsqrt2, ay + length * sine * invsqrt2),
        "Y": (ax + length * invsqrt2, ay - length * sine * invsqrt2),
        "Z": (ax, ay - length * cosine),
    }
    axis_colors = {"X": (180, 70, 61), "Y": (54, 134, 104), "Z": (63, 112, 179)}
    for label, endpoint in axis_end.items():
        draw.line(f([(ax, ay), endpoint]), fill=axis_colors[label], width=2 * scale_image)
        text(endpoint[0], endpoint[1] - 5, label, 15, axis_colors[label], True, "mm")

    legend_y = H - 120
    text(38, legend_y - 10, "COLOR = CELL TOP HEIGHT (mm)", 16, INK, True)
    lx, ly, lw, lh = 38, legend_y + 22, min(430, W - 400), 16
    gradient = height_colors(np.linspace(zmin, zmax, max(2, lw))[None, :], zmin, zmax)
    strip = Image.fromarray(gradient).resize((lw * scale_image, lh * scale_image))
    canvas.paste(strip, (lx * scale_image, ly * scale_image))
    draw = ImageDraw.Draw(canvas)
    for fraction in (0, 0.5, 1):
        value = zmin + fraction * (zmax - zmin)
        text(lx + fraction * lw, ly + 22, f"{value:g}", 15, MUTED,
             anchor="lt" if fraction == 0 else ("rt" if fraction == 1 else "mt"))
    remark_x = lx + lw + 32
    remark_lines = wrap(draw, "Wall shades follow the top. Not material or electrical data.",
                        font(16 * scale_image), (W - remark_x - 25) * scale_image)
    for j, line in enumerate(remark_lines):
        text(remark_x, ly - 1 + j * 21, line, 16, MUTED)
    text(38, H - 31, "Final repaired cell geometry  |  Flat tops and vertical walls  |  Orthographic view", 14, MUTED)
    if supersample > 1:
        canvas = canvas.resize(size, Image.Resampling.LANCZOS)
    return canvas


def render_top_view(heights: np.ndarray, record: dict, geometry: dict,
                    size: tuple[int, int] = (1100, 850), supersample: int = 2) -> Image.Image:
    """Direct plan projection: +X right, +Y up; no hidden labels are invented.

    Nearest-neighbour image scaling preserves the cell segmentation. Thin
    outlines mark actual height discontinuities, including the final repair
    and embossed lettering. Color encodes cell-top height, not doping/material.
    """
    ss = supersample
    W, H = size
    canvas = Image.new("RGB", (W * ss, H * ss), BG)
    draw = ImageDraw.Draw(canvas)
    def text(x, y, value, sz=18, color=INK, bold=False, anchor=None):
        draw.text((int(x * ss), int(y * ss)), str(value),
                  font=font(max(1, int(sz * ss)), bold), fill=color, anchor=anchor)
    text(38, 21, f"{canonical_group(record)}  /  {record['print_id']}  /  TOP VIEW", 16, MUTED, True)
    title_size = 30
    title = str(record.get("name_en") or record["print_id"])
    title_lines = wrap(draw, title, font(title_size * ss, True), (W - 76) * ss)
    while len(title_lines) > 2 and title_size > 20:
        title_size -= 1
        title_lines = wrap(draw, title, font(title_size * ss, True), (W - 76) * ss)
    for j, line in enumerate(title_lines):
        text(38, 47 + j * (title_size + 5), line, title_size, INK, True)
    heading_bottom = 47 + len(title_lines) * (title_size + 5)
    text(38, heading_bottom + 9, "ENLARGED CONCEPT / NOT TO SCALE", 17, (160, 87, 25), True)
    width, depth, zmax = geometry["size_mm"]
    text(38, heading_bottom + 37,
         f"Printed envelope: {width:g} x {depth:g} x {zmax:g} mm", 18, MUTED)
    top, bottom = heading_bottom + 79, H - 155
    if bottom - top < 230:
        raise ValueError("Preview canvas is too short for the complete title and top view")
    zoom = min((W - 180) / width, (bottom - top - 20) / depth)
    plot_width, plot_height = width * zoom, depth * zoom
    x0 = (W - plot_width) / 2
    y0 = (top + bottom - plot_height) / 2
    zmin = float(heights.min())
    colors = height_colors(heights, zmin, zmax)
    cell_image = Image.fromarray(np.flipud(colors)).resize(
        (round(plot_width * ss), round(plot_height * ss)), Image.Resampling.NEAREST
    )
    canvas.paste(cell_image, (round(x0 * ss), round(y0 * ss)))
    draw = ImageDraw.Draw(canvas)
    ny, nx = heights.shape
    dx, dy = geometry["dx"], geometry["dy"]
    contour = (48, 80, 96)
    line_width = max(1, ss // 2)
    def segment(a, b):
        draw.line([(round(a[0] * ss), round(a[1] * ss)),
                   (round(b[0] * ss), round(b[1] * ss))],
                  fill=contour, width=line_width)
    for row, col in np.argwhere(np.abs(heights[:, 1:] - heights[:, :-1]) > 1e-8):
        xx = x0 + (col + 1) * dx * zoom
        yy = y0 + (ny - row - 1) * dy * zoom
        segment((xx, yy), (xx, yy + dy * zoom))
    for row, col in np.argwhere(np.abs(heights[1:, :] - heights[:-1, :]) > 1e-8):
        xx = x0 + col * dx * zoom
        yy = y0 + (ny - row - 1) * dy * zoom
        segment((xx, yy), (xx + dx * zoom, yy))
    draw.rectangle((round(x0 * ss), round(y0 * ss),
                    round((x0 + plot_width) * ss), round((y0 + plot_height) * ss)),
                   outline=contour, width=max(1, ss))
    ax, ay, length = W - 88, bottom - 10, 40
    draw.line([(round(ax * ss), round(ay * ss)),
               (round((ax + length) * ss), round(ay * ss))], fill=(180, 70, 61), width=2 * ss)
    draw.line([(round(ax * ss), round(ay * ss)),
               (round(ax * ss), round((ay - length) * ss))], fill=(54, 134, 104), width=2 * ss)
    text(ax + length + 7, ay, "X", 15, (180, 70, 61), True, "lm")
    text(ax, ay - length - 8, "Y", 15, (54, 134, 104), True, "mm")
    legend_y = H - 120
    text(38, legend_y - 10, "COLOR = CELL TOP HEIGHT (mm)", 16, INK, True)
    lx, ly, lw, lh = 38, legend_y + 22, min(430, W - 400), 16
    gradient = height_colors(np.linspace(zmin, zmax, max(2, lw))[None, :], zmin, zmax)
    canvas.paste(Image.fromarray(gradient).resize((lw * ss, lh * ss)), (lx * ss, ly * ss))
    draw = ImageDraw.Draw(canvas)
    for fraction in (0, 0.5, 1):
        value = zmin + fraction * (zmax - zmin)
        text(lx + fraction * lw, ly + 22, f"{value:g}", 15, MUTED,
             anchor="lt" if fraction == 0 else ("rt" if fraction == 1 else "mt"))
    remark_x = lx + lw + 32
    remarks = wrap(draw, "Outlines mark height steps. Not material or electrical data.",
                   font(16 * ss), (W - remark_x - 25) * ss)
    for j, line in enumerate(remarks):
        text(remark_x, ly - 1 + j * 21, line, 16, MUTED)
    text(38, H - 31, "Final repaired cell geometry  |  Plan view from +Z  |  +X right, +Y up", 14, MUTED)
    if ss > 1:
        canvas = canvas.resize(size, Image.Resampling.LANCZOS)
    return canvas


def contact_sheet(records: list[dict], root: Path, group: str,
                  view: str = "iso") -> tuple[Path, dict]:
    columns = min(4, max(1, len(records)))
    tile_width, tile_height = 420, 370
    gutter, header = 16, 90
    rows = math.ceil(len(records) / columns)
    width = gutter + columns * (tile_width + gutter)
    height = header + rows * (tile_height + gutter)
    canvas = Image.new("RGB", (width, height), BG)
    draw = ImageDraw.Draw(canvas)
    heading = (f"{group} | Printable semiconductor teaching models" if view == "iso"
               else f"{group} | Top views of printable teaching models")
    heading_size = 27 if columns > 1 else 18
    while heading_size > 12 and draw.textlength(heading, font=font(heading_size, True)) > width - 2 * gutter:
        heading_size -= 1
    draw.text((gutter, 17), heading, font=font(heading_size, True), fill=INK)
    subtitle = (f"{len(records)} final heightfield previews | Colors indicate printed height only"
                if columns > 1 else f"{len(records)} final preview | Color = printed height")
    draw.text((gutter, 54), subtitle, font=font(17), fill=MUTED)
    for index, record in enumerate(records):
        x = gutter + (index % columns) * (tile_width + gutter)
        y = header + (index // columns) * (tile_height + gutter)
        draw.rounded_rectangle((x, y, x + tile_width, y + tile_height), radius=10,
                               fill=(255, 255, 255), outline=(217, 226, 233), width=1)
        with Image.open(root / record["png" if view == "iso" else "top"]) as im:
            im = im.convert("RGB")
            im.thumbnail((tile_width - 12, tile_height - 47), Image.Resampling.LANCZOS)
            canvas.paste(im, (x + (tile_width - im.width) // 2, y + 37))
        draw.text((x + 12, y + 10), record["print_id"], font=font(16, True), fill=INK)
    suffix = "" if view == "iso" else "_top"
    destination = root / "contact_sheets" / f"{group}{suffix}.png"
    destination.parent.mkdir(parents=True, exist_ok=True)
    canvas.save(destination, optimize=True)
    with Image.open(destination) as check:
        check.load()
        assert check.size == canvas.size
    return destination, dict(group=group, view=view, count=len(records),
                             png=destination.relative_to(root).as_posix(),
                             width_px=width, height_px=height,
                             sha256=sha256_file(destination))


def main(argv=None) -> int:
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("--catalogue", type=Path, default=HERE / "catalogue.json")
    parser.add_argument("--out-dir", type=Path, default=None,
                        help="Default: catalogue's parent directory")
    parser.add_argument("--ids", nargs="+", help="Render only these print_id values")
    parser.add_argument("--width", type=int, default=1100)
    parser.add_argument("--height", type=int, default=850)
    parser.add_argument("--supersample", type=int, default=2)
    parser.add_argument("--no-contact-sheets", action="store_true")
    args = parser.parse_args(argv)
    if args.width < 800 or args.height < 700 or not 1 <= args.supersample <= 4:
        parser.error("Use width>=800, height>=700 and supersample in [1,4]")
    catalogue = args.catalogue.resolve()
    root = catalogue.parent
    output = (args.out_dir or root).resolve()
    data = json.loads(catalogue.read_text(encoding="utf-8-sig"))
    if not isinstance(data, list):
        raise ValueError("Catalogue must be a JSON array")
    identifiers = [str(entry["print_id"]) for entry in data]
    if len(set(identifiers)) != len(identifiers):
        raise ValueError("Duplicate print_id values in catalogue")
    if args.ids:
        unknown = set(args.ids) - set(identifiers)
        if unknown:
            raise ValueError(f"Unknown print_id values: {sorted(unknown)}")
        data = [entry for entry in data if str(entry["print_id"]) in set(args.ids)]
    if not data:
        raise ValueError("No catalogue entries selected")
    (output / "previews").mkdir(parents=True, exist_ok=True)
    results = []
    for number, entry in enumerate(data, 1):
        identifier = str(entry["print_id"])
        if not re.fullmatch(r"[A-Za-z0-9_.-]+", identifier) or identifier in {".", ".."}:
            raise ValueError(f"Unsafe print_id filename: {identifier}")
        heights, geometry = checked_geometry(entry, root)
        destination = output / "previews" / f"{identifier}.png"
        im = render_preview(heights, entry, geometry,
                            size=(args.width, args.height), supersample=args.supersample)
        im.save(destination, optimize=True)
        with Image.open(destination) as check:
            check.load()
            if check.size != im.size or check.mode != "RGB":
                raise ValueError(f"PNG decode validation failed: {destination}")
        top_destination = output / "previews" / f"{identifier}_top.png"
        top_image = render_top_view(heights, entry, geometry,
                                    size=(args.width, args.height), supersample=args.supersample)
        top_image.save(top_destination, optimize=True)
        with Image.open(top_destination) as check:
            check.load()
            if check.size != top_image.size or check.mode != "RGB":
                raise ValueError(f"Top PNG decode validation failed: {top_destination}")
        try:
            height_path = geometry["path"].relative_to(root).as_posix()
        except ValueError:
            height_path = str(geometry["path"])
        results.append(dict(print_id=identifier, name_en=entry.get("name_en", identifier),
                            group=canonical_group(entry), png=destination.relative_to(output).as_posix(),
                            sha256=sha256_file(destination), bytes=destination.stat().st_size,
                            top=top_destination.relative_to(output).as_posix(),
                            top_sha256=sha256_file(top_destination), top_bytes=top_destination.stat().st_size,
                            top_png_decode_verified=True,
                            width_px=args.width, height_px=args.height,
                            heightfield=height_path, heightfield_sha256=geometry["sha256"],
                            shape=geometry["shape"], pitch_mm=[geometry["dx"], geometry["dy"]],
                            size_mm=geometry["size_mm"], minimum_top_mm=geometry["minimum_top_mm"],
                            png_decode_verified=True, rendered_all_final_cells=True))
        print(f"[{number:02d}/{len(data):02d}] {identifier}: ISO + TOP", flush=True)
    sheets = []
    if not args.no_contact_sheets:
        grouped = defaultdict(list)
        for record in results:
            grouped[record["group"]].append(record)
        for group in sorted(grouped):
            for view in ("iso", "top"):
                _, summary = contact_sheet(grouped[group], output, group, view=view)
                sheets.append(summary)
    manifest = dict(schema_version="1.0", catalogue_sha256=sha256_file(catalogue),
                    renderer_sha256=sha256_file(Path(__file__).resolve()),
                    projection="Orthographic; camera +X,-Y,+Z; elevation 35.26438968 degrees",
                    top_projection="Orthographic from +Z; +X right, +Y up; contours at final cell-height discontinuities",
                    geometry="Final saved positive cell heights; flat tops; vertical neighbour walls; bottom z=0",
                    color_meaning="Cell-top height in mm; walls darkened from their column's top color; independently normalized per model; not material or electrical fields",
                    microscopic_scope="Enlarged educational concept; not a dimensionally accurate semiconductor cross-section",
                    selected_ids=args.ids, model_count=len(results), png_count=2 * len(results), previews=results,
                    contact_sheets=sheets)
    manifest_path = output / "preview_manifest.json"
    manifest_path.write_text(json.dumps(manifest, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(f"Validated {2 * len(results)} PNGs for {len(results)} models; {len(sheets)} contact sheets. Manifest: {manifest_path}", flush=True)
    return 0


if __name__ == "__main__":
    sys.exit(main())
