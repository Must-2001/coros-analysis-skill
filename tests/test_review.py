import importlib.util
from pathlib import Path
import unittest

path=Path(__file__).resolve().parents[1]/'skills/coros-analysis/scripts/render_review.py'
spec=importlib.util.spec_from_file_location('review',path)
review=importlib.util.module_from_spec(spec)
spec.loader.exec_module(review)

class ReviewTests(unittest.TestCase):
    def data(self):
        return {'timezone':'Asia/Shanghai','start_date':'2026-01-01','end_date':'2026-01-04','days':[
            {'date':'2026-01-01','complete':True,'main_sleep_minutes':420,'steps':0,'training':[], 'sources':{'main_sleep_minutes':'overview/asleep','steps':'daily/steps','training':'records/full'}},
            {'date':'2026-01-02','complete':True,'main_sleep_minutes':None,'nap_minutes':60,'training':None,'sources':{'nap_minutes':'overview/nap asleep'}},
            {'date':'2026-01-04','complete':False,'main_sleep_minutes':900,'training':[{'sport':'Run','minutes':50}],'sources':{'main_sleep_minutes':'overview/asleep','training':'records/partial'}}]}

    def test_missing_nap_only_partial_and_zero(self):
        result=review.summary(self.data())
        self.assertEqual(result['calendar_days'],4)
        self.assertEqual(result['complete_observed_days'],2)
        self.assertEqual(result['main_sleep_observed_days'],1)
        self.assertEqual(result['main_sleep_median_minutes'],420)
        self.assertEqual(result['training_observed_days'],1)
        self.assertEqual(result['recorded_training_minutes_by_sport'],{})
        self.assertEqual(result['partial_days_excluded'],1)

    def test_mixed_sport_minutes(self):
        d=self.data();d['days'][0]['training']=[{'sport':'Run','minutes':30.5},{'sport':'Hike','minutes':120}]
        self.assertEqual(review.summary(d)['recorded_training_minutes_by_sport'],{'Hike':120,'Run':30.5})

    def test_reject_duplicate_dates(self):
        d=self.data();d['days'].append(d['days'][0])
        with self.assertRaises(ValueError):review.summary(d)

    def test_reject_unproven_metric(self):
        d=self.data();d['days'][0]['sources'].pop('steps')
        with self.assertRaises(ValueError):review.summary(d)

    def test_reject_negative_nan_bool(self):
        for value in (-1,float('nan'),True):
            d=self.data();d['days'][0]['steps']=value
            with self.subTest(value=value), self.assertRaises(ValueError):review.summary(d)

    def test_reject_duplicate_activity(self):
        d=self.data();d['days'][0]['training']=[{'id':'synthetic','sport':'Run','minutes':30}]*2
        with self.assertRaises(ValueError):review.summary(d)

    def test_reject_wrong_time_range(self):
        d=self.data();d['end_date']='2025-12-01'
        with self.assertRaises(ValueError):review.summary(d)

    def test_reject_sleep_sum_over_day(self):
        d=self.data();d['days'][0]['nap_minutes']=1200;d['days'][0]['sources']['nap_minutes']='overview/naps'
        with self.assertRaises(ValueError):review.summary(d)

class RenderTests(unittest.TestCase):
    def test_chart_exports_with_missing_and_partial_data(self):
        import tempfile
        with tempfile.TemporaryDirectory() as folder:
            d=ReviewTests().data()
            for suffix in ('png','svg'):
                output=Path(folder)/('review.'+suffix)
                review.render(d,output)
                content=output.read_bytes()
                self.assertGreater(len(content),1000)
                if suffix=='png':
                    self.assertEqual(content[:8],b'\x89PNG\r\n\x1a\n')
                else:
                    self.assertIn(b'<svg',content)

if __name__=='__main__':unittest.main()
