import json,unittest,datetime
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
load=lambda f:json.loads((ROOT/'research'/f).read_text(encoding='utf-8'))
class ResearchTests(unittest.TestCase):
    def test_unique_people_and_papers(self):
        people=load('people200.json');papers=load('papers.json')
        self.assertEqual(len(people),200);self.assertEqual(len({p['id']for p in people}),200)
        self.assertEqual(len(papers),182);self.assertEqual(len({p['doi']for p in papers}),182)
        self.assertEqual(len({p['region_en']for p in people}),22)
    def test_complete_join_and_bilingual_topics(self):
        papers={p['id']:p for p in load('papers.json')}
        for p in load('people200.json'):
            self.assertEqual(papers[p['paper_id']]['doi'],p['doi'])
            self.assertTrue(p['paper_title_en'] and p['paper_topic_zh'])
            self.assertIn(p['id'],papers[p['paper_id']]['associated_people'])
    def test_dates_and_metadata_status(self):
        for p in load('papers.json'):
            d=p['published_date_parts'];date=datetime.date(*(d+[1,1])[:3])
            self.assertLessEqual(date,datetime.date(2026,11,2))
            self.assertTrue(p['doi_record_verified']);self.assertFalse(p['update_notice_in_record'])
    def test_scope_and_reproduction_claims(self):
        allowed={'Data converters','Frequency synthesis and clocking','Power management ICs','RF and high-speed analog ICs','Precision analog and sensor interfaces','Analog device modeling and matching','Analog design automation and testing','Analog/RF components and parasitics'}
        for p in load('papers.json'):
            self.assertIn(p['category_en'],allowed);self.assertFalse(p['article_reproduction'])
            self.assertNotIn('guest editorial',p['title_en'].lower())
        self.assertEqual(sum(bool(p['primary_source_id'])for p in load('papers.json')),5)
    def test_analog_scope_evidence_and_byline(self):
        audit={p['id']:p for p in load('analog_scope_audit.json')}
        papers={p['id']:p for p in load('papers.json')}
        self.assertEqual(len(audit),200)
        for p in load('people200.json'):
            self.assertIn(p['scope_class'],{'circuit','method','component'})
            self.assertEqual(audit[p['id']]['doi'],p['doi'])
            self.assertIn(p['matched_author_name'],papers[p['paper_id']]['authors'])
            self.assertTrue(p['scope_reason_en'] and p['scope_reason_zh'])
            self.assertTrue(p['scope_evidence_url'].startswith('https://'))
            self.assertEqual(p['scope_checked'],'2026-11-02')
    def test_reconciliation_and_conservative_model_mapping(self):
        rows=load('scope_reconciliation_v31.json');people=load('people200.json')
        self.assertEqual(len(rows),200)
        self.assertEqual(sum(r['decision']=='excluded_from_current_cohort'for r in rows),16)
        self.assertEqual(sum(r['decision']=='paper_replaced'for r in rows),4)
        excluded={r['previous_id']for r in rows if r['decision']=='excluded_from_current_cohort'}
        self.assertFalse(excluded & {p['id']for p in people})
        self.assertEqual(sum(bool(p['mechanism_model_ids'])for p in load('papers.json')),8)
        for p in load('papers.json'):
            if p['scope_class']=='component':self.assertEqual(p['mechanism_model_ids'],[])
if __name__=='__main__':unittest.main()
