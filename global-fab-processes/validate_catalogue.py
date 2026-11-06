"""Read-only standard-library validation; print JSON and exit nonzero on failure.

Run from any directory. --strict-artifacts also requires the pending release ZIP
and package manifest. This is a data-consistency check, not process qualification.
"""
from __future__ import annotations

import argparse
from collections import Counter, defaultdict
import csv
from datetime import date
import hashlib
from html.parser import HTMLParser
import json
from pathlib import Path
import re
import sys
from urllib.parse import unquote, urlsplit

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent
PAIRS = ('company', 'region', 'business_type', 'platform', 'node', 'wafer',
         'voltage', 'voltage_kind', 'devices', 'application', 'dcdc_relevance',
         'availability', 'limitations', 'reading_depth', 'record_type')
NULLABLE_PAIRS = {'region', 'node', 'wafer', 'voltage', 'voltage_kind', 'devices', 'application'}
ENUMS = ('scope_category', 'entity_role', 'publication_state', 'evidence_kind', 'source_date_kind')
# Explicit public export contract; original research/status metadata stays in JSON.
CSV_FIELDS = ['id'] + [f'{k}_{lang}' for k in PAIRS for lang in ('en', 'zh')] + [
    'process_family', 'material', 'scope_category', 'entity_role', 'parent_group',
    'publication_state', 'evidence_kind', 'source_date_kind', 'source_title',
    'source_url', 'source_date', 'checked_date', 'catalogue_revision_added']
JSON_ONLY = {'research_id', 'source_status', 'source_status_en', 'source_status_zh'}
GAP_FIELDS = ['name', 'status', 'reason_en', 'reason_zh', 'source_url']
PENDING = {(ROOT / 'V3-3_20261106_catalogue2.zip').resolve(),
           (ROOT / 'V3-3/package_manifest.json').resolve()}


def canonical_sha256(value):
    raw = json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(',', ':')).encode('utf-8')
    return hashlib.sha256(raw).hexdigest()


def parse_json(text):
    def unique_object(pairs):
        result = {}
        for key, value in pairs:
            if key in result:
                raise ValueError(f'Duplicate JSON key: {key}')
            result[key] = value
        return result
    def invalid(value):
        raise ValueError(f'Non-finite JSON constant: {value}')
    return json.loads(text, object_pairs_hook=unique_object, parse_constant=invalid)


def text_value(value):
    return isinstance(value, str) and bool(value.strip())


def https(value):
    if not text_value(value) or re.search(r'\s', value):
        return False
    try:
        p = urlsplit(value)
        return p.scheme == 'https' and bool(p.hostname) and p.username is None and p.password is None
    except ValueError:
        return False


def iso_date(value):
    try:
        return isinstance(value, str) and date.fromisoformat(value).isoformat() == value
    except (ValueError, TypeError):
        return False


def extra_url(extra):
    return extra.get('url', extra.get('source_url'))


class DatasetParser(HTMLParser):
    def __init__(self):
        super().__init__(convert_charrefs=False)
        self.blocks, self.active = [], None

    def handle_starttag(self, tag, attrs):
        attrs = dict(attrs)
        if tag == 'script' and attrs.get('id') == 'catalogue-data':
            self.active = {'type': attrs.get('type'), 'chunks': []}
            self.blocks.append(self.active)

    def handle_data(self, value):
        if self.active is not None:
            self.active['chunks'].append(value)

    def handle_endtag(self, tag):
        if tag == 'script':
            self.active = None


def markdown_links(text):
    """Inline, reference and HTML destinations, including balanced parentheses."""
    text = re.sub(r'(?ms)^\s*(`{3,}|~{3,}).*?^\s*\1\s*$', '', text)
    for match in re.finditer(r'(?<!\\)\]\(', text):
        start = pos = match.end()
        depth, escaped = 1, False
        while pos < len(text) and depth:
            char = text[pos]
            if escaped:
                escaped = False
            elif char == '\\':
                escaped = True
            elif char == '(':
                depth += 1
            elif char == ')':
                depth -= 1
            pos += 1
        if depth:
            continue
        target = text[start:pos - 1].strip()
        if target.startswith('<') and '>' in target:
            yield target[1:target.index('>')]
        elif target:
            yield re.split(r'(?<!\\)\s', target, maxsplit=1)[0]
    for match in re.finditer(r'(?m)^\s{0,3}\[[^\]\n]+\]:\s*(?:<([^>]+)>|(\S+))', text):
        yield match.group(1) or match.group(2)
    for match in re.finditer(r'''\b(?:href|src)\s*=\s*['"]([^'"]+)['"]''', text, re.I):
        yield match.group(1)


class Audit:
    def __init__(self):
        self.checks, self.errors, self.pending = [], [], []

    def check(self, name, issues):
        issues = list(issues)
        self.checks.append({'check': name, 'status': 'FAIL' if issues else 'PASS', 'errors': len(issues)})
        self.errors.extend({'check': name, 'detail': str(x)} for x in issues)
        return not issues

    def report(self, **details):
        return {'status': 'FAIL' if self.errors else 'PASS', 'checks_run': len(self.checks),
                'checks_passed': sum(c['status'] == 'PASS' for c in self.checks),
                'checks': self.checks, 'errors': self.errors, 'pending_artifact_links': self.pending,
                **details, 'scope': 'Structure, exported fields, source index, baseline fingerprints and local file links. No live URL, PDF content, Excel or device-qualification assertion. Semantic ID stability is locked for fingerprinted baseline records; later records require a future baseline update.'}


def validate(strict_artifacts=False):
    audit = Audit()
    paths = {'rows': 'data/processes.json', 'gaps': 'data/gaps.json', 'tax': 'data/taxonomy.json',
             'meta': 'catalogue.json', 'coverage': 'coverage.json', 'sources': 'data/source_index.json',
             'baseline': 'data/baseline_fingerprints.json'}
    data, issues = {}, []
    for key, path in paths.items():
        try:
            data[key] = parse_json((HERE / path).read_text(encoding='utf-8'))
        except (OSError, ValueError) as exc:
            issues.append(f'{path}: {exc}')
    if not audit.check('canonical_json_readable_no_duplicate_keys', issues):
        return audit.report()
    issues = []
    for key, value in data.items():
        if key in {'rows', 'gaps', 'sources'}:
            if not isinstance(value, list) or not all(isinstance(x, dict) for x in value):
                issues.append(f'{key}: expected a list of objects')
        elif not isinstance(value, dict):
            issues.append(f'{key}: expected an object')
    if not data['rows']:
        issues.append('Empty catalogue')
    if not audit.check('top_level_schema', issues):
        return audit.report()
    rows, gaps, tax, meta, coverage, sources, baseline = (data[k] for k in paths)
    issues = []
    for key in (*ENUMS, 'gap_status'):
        labels = tax.get(key)
        if not isinstance(labels, dict) or not labels:
            issues.append(f'taxonomy.{key}: missing enumeration')
        else:
            for value, label in labels.items():
                if not text_value(value) or not isinstance(label, list) or len(label) != 2 or not all(map(text_value, label)):
                    issues.append(f'taxonomy.{key}.{value}: expected English and Chinese labels')
    if not audit.check('taxonomy_bilingual_enumerations', issues):
        return audit.report()
    issues = []
    for pos, row in enumerate(rows, 1):
        ident = row.get('id', f'row {pos}')
        for key, value in row.items():
            if isinstance(value, (bool, int, float)) or (isinstance(value, str) and value.strip() == '0'):
                issues.append(f'{ident}.{key}: catalogue fields use text or null, not numeric placeholders')
        missing = set(CSV_FIELDS) - row.keys()
        if missing:
            issues.append(f'{ident}: missing {sorted(missing)}')
        for key in PAIRS:
            en, zh = row.get(key + '_en'), row.get(key + '_zh')
            if (en is None) != (zh is None):
                issues.append(f'{ident}.{key}: asymmetric bilingual null')
            for lang, value in (('en', en), ('zh', zh)):
                if value is None and key in NULLABLE_PAIRS:
                    continue
                if not text_value(value):
                    issues.append(f'{ident}.{key}_{lang}: expected text or allowed null, never 0')
        for key in ('process_family', 'material', 'parent_group', 'source_date'):
            if row.get(key) is not None and not text_value(row[key]):
                issues.append(f'{ident}.{key}: expected text or null, never numeric 0')
        for key in ('id', 'source_title', 'catalogue_revision_added'):
            if not text_value(row.get(key)):
                issues.append(f'{ident}.{key}: expected nonempty text')
        for key in ENUMS:
            if row.get(key) not in tax[key]:
                issues.append(f'{ident}.{key}: unknown enumeration')
        if not iso_date(row.get('checked_date')):
            issues.append(f'{ident}: invalid checked_date')
        if not https(row.get('source_url')):
            issues.append(f'{ident}: invalid primary HTTPS URL')
        extras = row.get('additional_sources', [])
        if not isinstance(extras, list):
            issues.append(f'{ident}: additional_sources must be a list')
        else:
            for extra in extras:
                if not isinstance(extra, dict) or not https(extra_url(extra)) or not text_value(extra.get('title', extra.get('source_title'))):
                    issues.append(f'{ident}: additional source requires a title and HTTPS URL')
    if not audit.check('required_bilingual_fields_types_enums_and_sources', issues):
        return audit.report()
    ids = [r['id'] for r in rows]
    audit.check('unique_contiguous_ordered_ids', [] if ids == [f'FAB{i:03d}' for i in range(1, len(rows) + 1)] else ['IDs must be unique and contiguous, ordered from FAB001'])
    pairs = Counter((r['company_en'].strip().casefold(), r['platform_en'].strip().casefold()) for r in rows)
    audit.check('no_duplicate_company_platform', [f'{key}: {n} copies' for key, n in pairs.items() if n > 1])
    issues, entries = [], baseline.get('records')
    if baseline.get('baseline_commit') != meta.get('baseline_catalogue_commit'):
        issues.append('Baseline provenance commit differs from catalogue metadata')
    if baseline.get('algorithm') != 'sha256' or not isinstance(entries, list) or not entries:
        issues.append('Expected nonempty baseline SHA256 records')
    else:
        current, seen = {r['id']: r for r in rows}, set()
        for entry in entries:
            if not isinstance(entry, dict):
                issues.append('Malformed baseline entry')
                continue
            ident, fields = entry.get('id'), entry.get('fields')
            if ident in seen:
                issues.append(f'Duplicate baseline ID {ident}')
            seen.add(ident)
            if not isinstance(fields, list) or not fields or not all(map(text_value, fields)) or len(fields) != len(set(fields)) or 'id' not in fields:
                issues.append(f'{ident}: malformed baseline field list')
            elif ident not in current or not set(fields) <= current[ident].keys():
                issues.append(f'{ident}: missing baseline record or original fields')
            elif canonical_sha256({k: current[ident][k] for k in fields}) != entry.get('sha256'):
                issues.append(f'{ident}: original field values changed (SHA256 mismatch)')
        if seen != {r['id'] for r in rows if r['catalogue_revision_added'] == baseline.get('catalogue_revision')}:
            issues.append('Fingerprint IDs differ from records labelled with baseline revision')
    audit.check('stable_baseline_ids_and_original_fields', issues)
    companies = sorted({r['company_en'] for r in rows})
    expected = {re.sub(r'[^a-z0-9]+', '-', n.lower()).strip('-') + '.md' for n in companies}
    actual = {p.name for p in (HERE / 'companies').glob('*.md')}
    issues = [] if expected == actual else [f'Missing: {sorted(expected - actual)}; stale: {sorted(actual - expected)}']
    if len(expected) != len(companies):
        issues.append('Company filename collision')
    audit.check('company_pages_exact_set', issues)
    issues, names = [], set()
    for gap in gaps:
        name = gap.get('name')
        missing = set(GAP_FIELDS) - gap.keys()
        if missing:
            issues.append(f'{name}: missing {sorted(missing)}')
        for key in ('name', 'reason_en', 'reason_zh'):
            if not text_value(gap.get(key)):
                issues.append(f'{name}.{key}: expected nonempty text')
        if name in names:
            issues.append(f'Duplicate gap name: {name}')
        names.add(name)
        if gap.get('status') not in tax['gap_status']:
            issues.append(f'{name}: unknown status')
        if gap.get('source_url') is not None and not https(gap['source_url']):
            issues.append(f'{name}: expected HTTPS source or null')
        if 'checked_date' in gap and not iso_date(gap['checked_date']):
            issues.append(f'{name}: invalid checked_date')
        if 'evidence_kind' in gap and gap['evidence_kind'] not in tax['evidence_kind']:
            issues.append(f'{name}: unknown evidence_kind')
    audit.check('coverage_gaps_schema', issues)
    for filename, expected_rows, fields, extra_sources in (
        ('processes.csv', rows, CSV_FIELDS, True), ('gaps.csv', gaps, GAP_FIELDS, False)):
        issues = []
        try:
            with (HERE / 'data' / filename).open(encoding='utf-8-sig', newline='') as stream:
                reader = csv.DictReader(stream)
                columns = fields + (['additional_sources_json'] if extra_sources else [])
                if reader.fieldnames != columns:
                    issues.append(f'Header differs from export contract: {reader.fieldnames}')
                exported = list(reader)
            if len(exported) != len(expected_rows):
                issues.append('CSV row count differs from canonical JSON')
            for pos, (saved, record) in enumerate(zip(exported, expected_rows), 1):
                if None in saved:
                    issues.append(f'Row {pos}: extra CSV cells')
                for field in fields:
                    value = record.get(field)
                    if saved.get(field) != ('' if value is None else str(value)):
                        issues.append(f'Row {pos}.{field}: value differs from canonical JSON')
                if extra_sources:
                    try:
                        if parse_json(saved.get('additional_sources_json', '')) != record.get('additional_sources', []):
                            issues.append(f'Row {pos}: supplemental sources differ')
                    except (ValueError, TypeError):
                        issues.append(f'Row {pos}: invalid additional_sources_json')
        except (OSError, csv.Error, UnicodeError) as exc:
            issues.append(str(exc))
        audit.check(filename + '_columns_and_cell_values', issues)
    json_only = set().union(*(r.keys() for r in rows)) - set(CSV_FIELDS) - {'additional_sources'}
    audit.check('no_unacknowledged_json_only_fields', [f'Unexpected non-exported field: {k}' for k in sorted(json_only - JSON_ONLY)])
    issues = []
    try:
        parser = DatasetParser()
        parser.feed((HERE / 'index.html').read_text(encoding='utf-8'))
        if len(parser.blocks) != 1 or parser.blocks[0]['type'] != 'application/json' or parser.active is not None:
            issues.append('Expected one closed application/json script with id catalogue-data')
        elif parse_json(''.join(parser.blocks[0]['chunks'])) != {'rows': rows, 'gaps': gaps, 'taxonomy': tax, 'meta': meta}:
            issues.append('HTML dataset differs from canonical rows/gaps/taxonomy/metadata')
    except (OSError, ValueError) as exc:
        issues.append(str(exc))
    audit.check('html_dataset_matches_canonical', issues)
    expected_sources = defaultdict(set)
    for row in rows:
        for url in [row['source_url'], *[extra_url(x) for x in row.get('additional_sources', [])]]:
            expected_sources[url].add(row['id'])
    issues, indexed = [], {}
    for source in sources:
        url, record_ids = source.get('url'), source.get('record_ids')
        if not https(url) or not text_value(source.get('title')) or not isinstance(record_ids, list) or not all(map(text_value, record_ids)):
            issues.append(f'Malformed source-index entry: {url}')
            continue
        if url in indexed or len(record_ids) != len(set(record_ids)):
            issues.append(f'Duplicate source or record IDs: {url}')
        indexed[url] = set(record_ids)
    if indexed != dict(expected_sources):
        issues.append('URL-to-record mapping differs from canonical sources')
    audit.check('source_index_complete_and_exact', issues)
    recomputed = {
        'version': meta.get('version'), 'checked_date': meta.get('review_date'),
        'entities': len(companies), 'records': len(rows),
        'technical_records': sum(r['scope_category'] != 'corporate_history' for r in rows),
        'corporate_history_records': sum(r['scope_category'] == 'corporate_history' for r in rows),
        'record_type_counts': dict(Counter(r['record_type_en'] for r in rows)),
        'companies': companies, 'source_urls': len(expected_sources),
        'primary_source_urls': len({r['source_url'] for r in rows}),
        'scope_counts': dict(Counter(r['scope_category'] for r in rows)),
        'state_counts': dict(Counter(r['publication_state'] for r in rows)),
        'evidence_counts': dict(Counter(r['evidence_kind'] for r in rows)), 'gap_candidates': len(gaps),
        'baseline_records_preserved': sum(r['catalogue_revision_added'] == baseline.get('catalogue_revision') for r in rows),
        'all_required_fields_present': True}
    issues = [f'coverage.{k}: expected {v!r}, got {coverage.get(k)!r}' for k, v in recomputed.items() if coverage.get(k) != v]
    if set(coverage) != set(recomputed) | {'scope'}:
        issues.append('Coverage fields changed: update the recomputation contract explicitly')
    if not text_value(coverage.get('scope')):
        issues.append('Missing coverage scope')
    audit.check('coverage_totals_recomputed', issues)
    markdown_files = [ROOT / 'README.md', ROOT / 'V3-3/README.md', *sorted(HERE.rglob('*.md'))]
    issues = []
    for path in markdown_files:
        try:
            content = path.read_text(encoding='utf-8')
        except OSError as exc:
            issues.append(str(exc))
            continue
        for destination in markdown_links(content):
            destination = re.sub(r'\\([ ()])', r'\1', destination)
            parsed = urlsplit(destination)
            if parsed.scheme or parsed.netloc or not parsed.path:
                continue
            decoded = unquote(parsed.path)
            target = ((ROOT / decoded.lstrip('/')) if decoded.startswith('/') else (path.parent / decoded)).resolve()
            location = path.relative_to(ROOT).as_posix()
            if not target.is_relative_to(ROOT):
                issues.append(f'{location}: local path escapes repository: {destination}')
            elif not target.exists():
                if not strict_artifacts and target in PENDING:
                    audit.pending.append({'document': location, 'destination': destination})
                else:
                    issues.append(f'{location}: missing {destination}')
    audit.check('local_markdown_links', issues)
    return audit.report(catalogue_version=meta.get('version'), review_date=meta.get('review_date'),
        records=len(rows), entities=len(companies), gaps=len(gaps), source_urls=len(expected_sources),
        baseline_records_verified=len(entries) if isinstance(entries, list) else 0,
        markdown_files_checked=len(markdown_files), json_only_metadata=sorted(json_only),
        catalogue_sha256=hashlib.sha256((HERE / 'data/processes.json').read_bytes()).hexdigest(),
        strict_artifacts=strict_artifacts)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--strict-artifacts', action='store_true', help='Require the pending release ZIP and manifest')
    args = parser.parse_args()
    try:
        report = validate(args.strict_artifacts)
    except Exception as exc:
        report = {'status': 'FAIL', 'errors': [{'check': 'validator_execution', 'detail': f'{type(exc).__name__}: {exc}'}]}
    print(json.dumps(report, ensure_ascii=False, indent=2))
    return 0 if report['status'] == 'PASS' else 1


if __name__ == '__main__':
    sys.exit(main())
