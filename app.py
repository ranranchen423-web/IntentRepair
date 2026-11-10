"""Run with `python app.py`. Local UI with optional real AI backend."""
from http.server import ThreadingHTTPServer, BaseHTTPRequestHandler
from pathlib import Path
from urllib.parse import urlparse
import json
from intent_engine import process, refine
from ai_service import mode, generate, suggest_refinements

ROOT = Path(__file__).resolve().parent
FILES = {'/': ('templates/index.html', 'text/html; charset=utf-8'),
         '/static/app.css': ('static/app.css', 'text/css; charset=utf-8'),
         '/static/app.js': ('static/app.js', 'application/javascript; charset=utf-8')}

class Handler(BaseHTTPRequestHandler):
    def do_GET(self):
        path = urlparse(self.path).path
        if path == '/api/health':
            return self.send_json(200, {'status': 'ok', 'mode': mode(), 'model': 'configured' if mode() == 'live' else None})
        if path not in FILES:
            return self.send_json(404, {'error': 'Not found'})
        name, mime = FILES[path]
        data = (ROOT / name).read_bytes()
        self.send_response(200)
        self.send_header('Content-Type', mime)
        self.send_header('Content-Length', str(len(data)))
        self.send_header('Cache-Control', 'no-store')
        self.end_headers()
        self.wfile.write(data)

    def do_POST(self):
        path = urlparse(self.path).path
        if path not in ('/api/chat', '/api/refine', '/api/clarify'):
            return self.send_json(404, {'error': 'Not found'})
        try:
            length = int(self.headers.get('Content-Length', '0'))
            if not 0 < length <= 10000:
                raise ValueError('Invalid request size.')
            payload = json.loads(self.rfile.read(length))
            if not isinstance(payload, dict):
                raise ValueError('Expected a JSON object.')
            if path == '/api/clarify':
                message = payload.get('message')
                answer = payload.get('answer')
                history = payload.get('history', [])
                if not isinstance(message,str) or not message.strip() or not isinstance(answer,str) or not isinstance(history,list):
                    raise ValueError('message, answer and history must be valid.')
                result=suggest_refinements(message[:2000],answer[:4000],history=history[-8:])
                return self.send_json(200,result)
            if path == '/api/chat':
                if not isinstance(payload.get('message'), str):
                    raise ValueError('message must be text.')
                result = process(payload['message'])
                if mode() == 'live':
                    reply, model = generate(payload['message'], result['intent'], history=payload.get('history'))
                    result['recommendation'] = {'title': 'AI response', 'description': reply, 'details': [], 'disclaimer': 'AI-generated content. Trip details are not verified.'}
                    result['engine'] = 'live-ai'
                    result['model'] = model
            else:
                if not isinstance(payload.get('intent'), dict) or not isinstance(payload.get('updates'), dict):
                    raise ValueError('intent and updates must be objects.')
                result = refine(payload['intent'], payload['updates'])
                if mode() == 'live':
                    original = payload.get('original_message', 'Suggest a day trip')
                    if not isinstance(original, str): raise ValueError('original_message must be text.')
                    reply, model = generate(original[:1000] + '\nPlease revise the answer using my updated preferences.', result['intent'], history=payload.get('history'))
                    result['recommendation'] = {'title': 'Updated AI response', 'description': reply, 'details': [], 'disclaimer': 'AI-generated content. Trip details are not verified.'}
                    result['engine'] = 'live-ai'
                    result['model'] = model
            self.send_json(200, result)
        except (ValueError, json.JSONDecodeError) as exc:
            self.send_json(400, {'error': str(exc)})
        except RuntimeError as exc:
            self.send_json(503, {'error': str(exc)})

    def send_json(self, status, body):
        data = json.dumps(body, ensure_ascii=False).encode('utf-8')
        self.send_response(status)
        self.send_header('Content-Type', 'application/json; charset=utf-8')
        self.send_header('Content-Length', str(len(data)))
        self.send_header('Cache-Control', 'no-store')
        self.end_headers()
        self.wfile.write(data)

if __name__ == '__main__':
    print('IntentRepair running at http://127.0.0.1:8000')
    ThreadingHTTPServer(('127.0.0.1', 8000), Handler).serve_forever()
