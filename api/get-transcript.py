from youtube_transcript_api import YouTubeTranscriptApi
from youtube_transcript_api._errors import TranscriptsDisabled, NoTranscriptFound

def handler(request):
    video_id = request.query.get("videoId")

    if not video_id:
        return {
            "statusCode": 400,
            "body": {"error": "Missing videoId parameter"}
        }

    try:
        transcript = YouTubeTranscriptApi.get_transcript(video_id)
        return {
            "statusCode": 200,
            "body": transcript
        }
    except TranscriptsDisabled:
        return {"statusCode": 403, "body": {"error": "Transcripts are disabled"}}
    except NoTranscriptFound:
        return {"statusCode": 404, "body": {"error": "No transcript found"}}
    except Exception as e:
        return {"statusCode": 500, "body": {"error": str(e)}}
