import unittest
from unittest.mock import patch
from ai_service import suggest_refinements

class DynamicRefinementTests(unittest.TestCase):
    @patch('ai_service.generate', return_value=('''{"question":"What Python help?","options":["Debugging","Beginner lesson","Practice"]}''', 'test-model'))
    @patch('ai_service.mode', return_value='live')
    def test_relevant_json(self, mode, generate):
        result=suggest_refinements('Help me with Python','Here is Python',history=[])
        self.assertEqual(result['options'][0], 'Debugging')
        self.assertIn('Python',generate.call_args.args[0])

    @patch('ai_service.generate', return_value=('not json', 'test-model'))
    @patch('ai_service.mode', return_value='live')
    def test_malformed_output(self, mode, generate):
        with self.assertRaises(RuntimeError): suggest_refinements('hello','world')

    @patch('ai_service.mode', return_value='demo')
    def test_live_required(self, mode):
        with self.assertRaises(RuntimeError): suggest_refinements('hello','world')

if __name__ == '__main__': unittest.main()
