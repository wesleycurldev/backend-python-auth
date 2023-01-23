import requests
import json

from dotenv import load_dotenv
from os import environ

load_dotenv()


def cashback_processing(request_body: dict):
    try:
        payload = json.dumps(request_body)
        headers = {
            'Content-Type': 'application/json'
        }

        response = requests.request("POST", environ.get("CASHBACK_PROCESSING_URL"), headers=headers, data=payload)
 
        return response.json()
    except Exception as e:
        return {'message': str(e), 'code': 'EXTERNAL_REQUEST_ERROR', 'error': True}
