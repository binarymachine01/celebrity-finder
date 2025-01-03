import boto3
import asyncio
import logging
from botocore.exceptions import BotoCoreError, ClientError


async def analyze_image_async(task_id: str, image_bytes: bytes, task_manager):
    client = boto3.client("rekognition")
    try:

        task_manager.update_task(task_id, "IN_PROGRESS")


        loop = asyncio.get_event_loop()
        response = await loop.run_in_executor(
            None, lambda: client.recognize_celebrities(Image={"Bytes": image_bytes})
        )


        celebrities = []
        for celeb in response.get("CelebrityFaces", []):
            celebrities.append({
                "name": celeb["Name"],
                "confidence": celeb["MatchConfidence"],
                "urls": celeb.get("Urls", []),
            })


        task_manager.update_task(task_id, {"status": "COMPLETED", "result": celebrities})
    except (BotoCoreError, ClientError) as e:
        logging.error(f"Error with AWS Rekognition: {e}")
        task_manager.update_task(task_id, {"status": "FAILED", "error": str(e)})
