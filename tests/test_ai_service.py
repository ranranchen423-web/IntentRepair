import json
import sys
import unittest
from pathlib import Path
from unittest.mock import patch
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
import ai_service

class FakeResponse:
    def __enter__(self): return self
    def __exit__(self, *args): pass
    def read(self): return json.dumps({'choices':[{'message':{'content':'A suggested hiking day.'}}]}).encode()

class LiveAiTests(unittest.TestCase):
    def test_demo_when_no_key(self):
        with patch.object(ai_service,'_config',return_value={'OPENAI_API_KEY':'','AI_MODE':'','AI_MODEL':'','AI_BASE_URL':''}):
            self.assertEqual(ai_service.mode(),'demo')
    def test_live_when_key_exists(self):
        with patch.object(ai_service,'_config',return_value={'OPENAI_API_KEY':'test','AI_MODE':'','AI_MODEL':'','AI_BASE_URL':''}):
            self.assertEqual(ai_service.mode(),'live')
    def test_api_response_parsed(self):
        with patch.object(ai_service,'_config',return_value={'OPENAI_API_KEY':'fake','AI_MODE':'','AI_MODEL':'test-model','AI_BASE_URL':''}), patch.object(ai_service,'urlopen',return_value=FakeResponse()) as sender:
            answer,model=ai_service.generate('day trip',{'activity':'Hiking'})
            self.assertEqual(answer,'A suggested hiking day.')
            self.assertEqual(model,'test-model')
            self.assertIn(b'Hiking', sender.call_args.args[0].data)
    def test_http_requires_https(self):
        with patch.object(ai_service,'_config',return_value={'OPENAI_API_KEY':'fake','AI_MODE':'','AI_MODEL':'test-model','AI_BASE_URL':'http://example.com/v1'}):
            with self.assertRaises(RuntimeError): ai_service.generate('x',{})
if __name__=='__main__': unittest.main()
