import boto3
import json
from dotenv import load_dotenv
import os
import base64
import io
from io import BytesIO
from PIL import Image

# loading in variables from .env file
load_dotenv()

# instantiating the Bedrock client, and passing in the CLI profile
boto3.setup_default_session(profile_name="admin")
bedrock = boto3.client('bedrock-runtime', 'us-west-2', endpoint_url='https://bedrock-runtime.us-west-2.amazonaws.com')


def image_to_text(image_name, text):
    # open file and convert to base64
    open_image = Image.open(image_name)
    image_bytes = io.BytesIO()
    open_image.save(image_bytes, format=open_image.format)
    image_bytes = image_bytes.getvalue()
    image_base64 = base64.b64encode(image_bytes).decode('utf-8')

    file_type = f"image/{open_image.format.lower()}"

    system_prompt = """Describe every detail you can about this image, be extremely thorough and detail even the most minute aspects of the image. 
    
    If a more specific question is presented by the user, make sure to prioritize that answer.
    """
    if text is None:
        text = "Use the system prompt"
    print("text" + text)

    prompt = {
        "anthropic_version": "bedrock-2023-05-31",
        "max_tokens": 1000,
        "temperature": 0.5,
        "system": system_prompt,
        "messages": [
            {
                "role": "user",
                "content": [
                    {
                        "type": "image",
                        "source": {
                            "type": "base64",
                            "media_type": file_type,
                            "data": image_base64
                        }
                    },
                    {
                        "type": "text",
                        "text": text
                    }
                ]
            }
        ]
    }

    json_prompt = json.dumps(prompt)
    response = bedrock.invoke_model(body=json_prompt, modelId="anthropic.claude-3-sonnet-20240229-v1:0",
                                    accept="application/json", contentType="application/json")
    response_body = json.loads(response.get('body').read())
    llm_output = response_body['content'][0]['text']
    return llm_output


def text_to_text(text):
    system_prompt = """Answer every aspect of the provided question as thoroughly as possible. Be extremely thorough and provide detailed answers to the user provided question.
    """
    prompt = {
        "anthropic_version": "bedrock-2023-05-31",
        "max_tokens": 1000,
        "temperature": 0.5,
        "system": system_prompt,
        "messages": [
            {
                "role": "user",
                "content": [
                    {
                        "type": "text",
                        "text": text
                    }
                ]
            }
        ]
    }

    json_prompt = json.dumps(prompt)
    response = bedrock.invoke_model(body=json_prompt, modelId="anthropic.claude-3-sonnet-20240229-v1:0",
                                    accept="application/json", contentType="application/json")
    response_body = json.loads(response.get('body').read())
    llm_output = response_body['content'][0]['text']
    return llm_output
