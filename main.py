from fastapi import FastAPI, Form, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
import requests

app = FastAPI()

templates = Jinja2Templates(directory="templates")

def classify_email(email_text):
    prompt = f"""
    You are an email classification assistant. Analyze the following email and classify it into one of these categories:

    1. Important: Work-related, actionable emails meant for general recipients.  
    2. Classified: Confidential or sensitive information meant for restricted recipients. Includes phrases like "confidential," "internal use," or "do not share."  
    3. Spam: Promotional, unsolicited, or irrelevant emails.
    
    Email Content:  
    \"\"\"{email_text}\"\"\"
    
    Respond only with the category name: Important, Classified, or Spam.
    """

    url = "http://localhost:11434/api/generate"
    payload = {"model": "llama3", "prompt": prompt, "stream": False}

    try:
        response = requests.post(url, json=payload)
        result = response.json()
        return result.get('response', 'Error: No response').strip()
    except Exception as e:
        return f"Error: {e}"

@app.get("/", response_class=HTMLResponse)
async def read_root(request: Request):
    return templates.TemplateResponse("index.html", {"request": request, "result": None})

@app.post("/", response_class=HTMLResponse)
async def classify(request: Request, email_text: str = Form(...)):
    result = classify_email(email_text)
    return templates.TemplateResponse("index.html", {"request": request, "result": result, "email_text": email_text})