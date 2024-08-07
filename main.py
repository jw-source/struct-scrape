from pydantic import BaseModel
from openai import OpenAI
import requests
import minify_html
import os
from dotenv import load_dotenv
load_dotenv()

client = OpenAI(api_key=os.environ["OPENAI_API_KEY"])

class CNNExtractor(BaseModel):
    title: str
    author: str
    summary: str
    comments: str

def extract_info(input: str):
    completion = client.beta.chat.completions.parse(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": "You are an expert at structured data extraction. You will be given unstructured HTML from a website and should convert it into the given structure."},
            {"role": "user", "content": f"{input}"}
        ],
        response_format=CNNExtractor,
    )
    return completion.choices[0].message.parsed

def get_html(url: str):
    res = requests.get(url)
    html_page = res.content.decode('utf-8')[:100000]
    output = minify_html.minify(html_page, minify_js=True, remove_processing_instructions=True)
    return output

print(extract_info(get_html("https://www.cnn.com/2024/08/07/politics/tim-walz-military-record-vance-attack/index.html")))
