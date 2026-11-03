"""Check published gallery coverage, provenance, files, timing and data references."""
import hashlib
import json
from pathlib import Path
import re

from PIL import Image

HERE = Path(__file__).resolve().parent
REPO = HERE.parents[1]
EXPECTED = {f"A{i:02}" for i in range(1,5)} | {f"B{i:02}" for i in range(1,8)} | {f"P{i:02}" for i in range(1,10)}

def sha(p):
    return hashlib.sha256(p.read_bytes()).hexdigest()

def main():
    manifest=json.loads((HERE/"manifest.json").read_text(encoding="utf-8"))
    assert set(manifest)==EXPECTED, "All twenty models are required."
    sources={}
    checks=[]
    for mid,record in manifest.items():
        source=REPO/record["source"]
        assert source.is_file()
        assert record["source"].startswith("v33/numerics/"), "Final gallery must use V3.3 results."
        if str(source) not in sources:
            sources[str(source)]=(sha(source),json.loads(source.read_text(encoding="utf-8")))
        source_hash,data=sources[str(source)]
        assert source_hash==record["source_sha256"], f"{mid}: numerical input changed"
        case=next(c for c in data["cases"] if c["id"]==record["case_id"])
        assert case["model_id"]==mid
        indices=record["sampled_indices"]
        assert len(indices)==48 and indices==sorted(indices)
        assert all(0<=i<len(case["x"]) for i in indices)
        assert case["x"][indices[0]]==record["x_display_min"]
        assert case["x"][indices[-1]]==record["x_display_max"]
        for key in ("title","explanation","axis","limits"):
            assert record[key+"_en"] and record[key+"_zh"]
            assert not re.search(r"[\u4e00-\u9fff]",record[key+"_en"])
        assert all(not re.search(r"[\u4e00-\u9fff]",name) for group in record["plot_signal_names"] for name in group)
        gif,poster=REPO/record["gif"],REPO/record["poster"]
        assert sha(gif)==record["gif_sha256"] and sha(poster)==record["poster_sha256"]
        assert gif.stat().st_size==record["bytes"]
        with Image.open(gif) as im:
            assert im.size==(1080,720)
            assert im.n_frames==record["frames"]==48
            assert im.info["loop"]==0
            duration=0
            for i in range(im.n_frames):
                im.seek(i)
                duration+=im.info["duration"]
                im.load()
            assert duration==record["duration_ms"]==8400
        with Image.open(poster) as im:
            assert im.size==(1080,720)
            im.verify()
        if mid=="A04":
            assert record["statistical_sample_count"]==case["metrics"]["sample_count"]==80000
        checks.append(dict(model_id=mid,case_id=case["id"],status="PASS",
                           gif_bytes=gif.stat().st_size,frames=48,duration_ms=duration))
    result=dict(status="PASS",models=len(checks),gif_count=len(list((HERE/"gifs").glob("*.gif"))),
                poster_count=len(list((HERE/"posters").glob("*.png"))),
                total_gif_bytes=sum(c["gif_bytes"] for c in checks),
                max_gif_bytes=max(c["gif_bytes"] for c in checks),
                checks="Coverage; V3.3 source hashes and case IDs; sampled indices and ranges; bilingual metadata; English plotted names; output hashes; full GIF decoding, frames, loop, dimensions and duration; PNG integrity.",
                model_checks=checks)
    assert result["gif_count"]==result["poster_count"]==20
    (HERE/"validation.json").write_text(json.dumps(result,ensure_ascii=False,indent=2)+"\n",encoding="utf-8")
    print(json.dumps({k:v for k,v in result.items() if k not in ("model_checks",)},ensure_ascii=False,indent=2))

if __name__=="__main__":
    main()
