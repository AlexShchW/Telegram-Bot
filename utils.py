import httpx
import os
from dotenv import load_dotenv

load_dotenv()
API_URL = os.getenv('API_URL')
QWEN_API_KEY = os.getenv('QWEN_API_KEY')

async def make_api_call(message: str):
    url = API_URL
    headers = {
        "Authorization": f"Bearer {QWEN_API_KEY}",
        "Content-Type": "application/json",
    }
    payload = {
        "model": "qwen/qwen2.5-vl-72b-instruct:free",
        "messages": [
            {
                "role": "user",
                "content": [
                    {
                        "type": "text",
                        "text": message
                    }
                ]
            }
        ]
    }

    try:
        async with httpx.AsyncClient() as client:
            response = await client.post(url, headers=headers, json=payload)
            if response.status_code == 200:
                data = response.json()
                # print("whole API response:", data)
                if "error" in data:
                    return f"API Error: {data['error']['message']}"
                if "choices" in data and data["choices"]:
                    return data["choices"][0]["message"]["content"]
                else:
                    return "Error: Unexpected response format from the API."
            else:
                return f"API Error: {response.status_code} - {response.text}"
    except httpx.NetworkError as e:
        return f"Network Error: {str(e)}"
    except Exception as e:
        return f"Unexpected Error: {str(e)}"
