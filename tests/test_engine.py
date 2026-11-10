import sys
import unittest
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from intent_engine import detect, process, refine

class EngineTests(unittest.TestCase):
    def test_clear_hiking(self):
        data=process('Suggest a quiet one-day hiking trip near Birmingham')
        self.assertFalse(data['needs_clarification'])
        self.assertEqual(data['intent']['activity'], 'Hiking')
        self.assertEqual(data['intent']['place'], 'Birmingham')
    def test_ambiguous(self):
        data=process('Suggest a day trip')
        self.assertTrue(data['needs_clarification'])
        self.assertIn('assumption', data['recommendation']['title'].lower())
    def test_refine_repairs(self):
        original=process('Suggest a day trip')
        revised=refine(original['intent'], {'activity':'Hiking','budget':'Low'})
        self.assertFalse(revised['needs_clarification'])
        self.assertEqual(revised['intent']['activity'], 'Hiking')
        self.assertIn('Low', revised['recommendation']['details'][-1])
    def test_ambiguous_multiple(self):
        self.assertTrue(detect('hiking or museum?')['ambiguous'])
    def test_invalid_options_rejected(self):
        with self.assertRaises(ValueError): refine(detect('day trip'), {'activity':'Skydiving'})
    def test_empty_input_rejected(self):
        with self.assertRaises(ValueError):process('   ')
    def test_no_options_rejected(self):
        with self.assertRaises(ValueError):refine(detect('day trip'), {})
    def test_negative_city_correction(self):
        result=process('i dont want to go to city')
        self.assertNotIn('museum', result['recommendation']['description'].lower())
        self.assertIn('not suggest', result['recommendation']['description'].lower())
    def test_unrelated_question_is_not_city_trip(self):
        result=process('What is a binary search tree?')
        self.assertIn('only supports day-trip',result['recommendation']['description'])
        self.assertFalse(result['needs_clarification'])
    def test_sightseeing(self):
        self.assertEqual(detect('I want a city tour')['activity'],'City sightseeing')

if __name__ == '__main__': unittest.main()
