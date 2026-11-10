import io
import sys
import unittest
from pathlib import Path
from unittest.mock import patch
from urllib.error import HTTPError
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
import ai_service

class ProviderErrorTests(unittest.TestCase):
    def test_404_exposes_code_without_secret(self):
        payload = b'{"error":{"code":"ModelNotFound","message":"Model access unavailable"}}'
        err = HTTPError('https://example.org',404,'Not Found',{},io.BytesIO(payload))
        cfg={'ARK_API_KEY':'private-example-secret','OPENAI_API_KEY':'','AI_MODE':'','AI_MODEL':'deepseek-v4-1-flash-261017','AI_BASE_URL':''}
        with patch.object(ai_service,'_config',return_value=cfg), patch.object(ai_service,'urlopen',side_effect=err):
            with self.assertRaises(RuntimeError) as caught:
                ai_service.generate('hello',{})
        self.assertIn('ModelNotFound',str(caught.exception))
        self.assertNotIn(cfg['ARK_API_KEY'],str(caught.exception))

if __name__ == '__main__': unittest.main()
