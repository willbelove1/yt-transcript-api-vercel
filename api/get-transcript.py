from youtube_transcript_api import YouTubeTranscriptApi
from youtube_transcript_api._errors import NoTranscriptFound, TranscriptsDisabled
from http.server import BaseHTTPRequestHandler
import json
from urllib.parse import urlparse, parse_qs

class handler(BaseHTTPRequestHandler):
    def do_GET(self):
        parsed_path = urlparse(self.path)
        query = parse_qs(parsed_path.query)
        video_id = query.get("videoId", [None])[0]

        self.send_response(200)
        self.send_header("Content-Type", "application/json")
        self.end_headers()

        if not video_id:
            self.wfile.write(json.dumps({"error": "Missing videoId"}).encode())
            return

        try:
            transcript = YouTubeTranscriptApi.get_transcript(video_id)
            self.wfile.write(json.dumps(transcript).encode())
        except NoTranscriptFound:
            self.wfile.write(json.dumps({"error": "No transcript found"}).encode())
        except TranscriptsDisabled:
            self.wfile.write(json.dumps({"error": "Transcripts are disabled"}).encode())
        except Exception as e:
            self.wfile.write(json.dumps({"error": str(e)}).encode())
