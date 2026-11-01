import json,unittest,datetime
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
load=lambda f:json.loads((ROOT/'research'/f).read_text(encoding='utf-8'))
class ResearchTests(unittest.TestCase):
    def test_unique_people_and_papers(self):
        people=load('people200.json');papers=load('papers.json')
        self.assertEqual(len(people),200);self.assertEqual(len({p['id']for p in people}),200)
        self.assertEqual(len(papers),184);self.assertEqual(len({p['doi']for p in papers}),184)
        self.assertEqual(len({p['region_en']for p in people}),20)
    def test_complete_join_and_bilingual_topics(self):
        papers={p['id']:p for p in load('papers.json')}
        for p in load('people200.json'):
            self.assertEqual(papers[p['paper_id']]['doi'],p['doi'])
            self.assertTrue(p['paper_title_en'] and p['paper_topic_zh'])
            self.assertIn(p['id'],papers[p['paper_id']]['associated_people'])
    def test_dates_and_metadata_status(self):
        for p in load('papers.json'):
            d=p['published_date_parts'];date=datetime.date(*(d+[1,1])[:3])
            self.assertLessEqual(date,datetime.date(2026,11,1))
            self.assertTrue(p['doi_record_verified']);self.assertFalse(p['update_notice_in_record'])
    def test_scope_and_reproduction_claims(self):
        allowed={'Data converters','Frequency synthesis and clocking','Power management ICs','RF and high-speed analog ICs','Precision analog and sensor interfaces','Analog device modeling and matching','Analog design automation and testing','Semiconductor devices and integration'}
        for p in load('papers.json'):
            self.assertIn(p['category_en'],allowed);self.assertFalse(p['article_reproduction'])
            self.assertNotIn('guest editorial',p['title_en'].lower())
        self.assertEqual(sum(bool(p['primary_source_id'])for p in load('papers.json')),5)
if __name__=='__main__':unittest.main()
