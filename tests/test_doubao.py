import sys
import unittest
from pathlib import Path
from unittest.mock import patch
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
import ai_service

class DoubaoTests(unittest.TestCase):
    def test_ark_key_live(self):
        with patch.object(ai_service, '_config', return_value={'ARK_API_KEY':'test-ark-key','OPENAI_API_KEY':'','AI_MODE':'','AI_MODEL':'','AI_BASE_URL':''}):
            self.assertEqual(ai_service.mode(),'live')
    def test_default_endpoint(self):
        class FakeResponse:
            def __enter__(self): return self
            def __exit__(self,*args): pass
            def read(self): return b'{"choices":[{"message":{"content":"Hello from Doubao"}}]}'
        with patch.object(ai_service, '_config', return_value={'ARK_API_KEY':'test-ark-key','OPENAI_API_KEY':'','AI_MODE':'','AI_MODEL':'','AI_BASE_URL':''}), patch.object(ai_service,'urlopen',return_value=FakeResponse()) as fn:
            text,model=ai_service.generate('Hello',{})
            self.assertEqual(text,'Hello from Doubao')
            self.assertEqual(model,'deepseek-v4-1-flash-261017')
            self.assertEqual(fn.call_args.args[0].full_url,'https://ark.cn-beijing.volces.com/api/v3/chat/completions')
