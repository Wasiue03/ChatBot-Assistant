from fastapi import FastAPI, Request
from transformers import pipeline
from selenium import webdriver

app = FastAPI()

summarizer = pipeline("summarization", model="facebook/bart-large-cnn")

def open_website(url):
    driver = webdriver.Chrome()
    driver.get(url)

def search_web(query):
    driver = webdriver.Chrome()
    driver.get(f"https://www.google.com/search?q={query}")

@app.get("/ping")
async def ping():
    return {"message": "Server is running"}

@app.post("/chatbot")
async def chatbot(request: Request):
    data = await request.json()
    user_input = data['input']
    
    if "open" in user_input:
        url = user_input.split("open ")[-1]
        open_website(f"https://{url}.com")
        return {"message": f"Opening {url}.com"}
    
    elif "search" in user_input:
        query = user_input.split("search for ")[-1]
        search_web(query)
        return {"message": f"Searching for {query}"}
    
    elif "summarize" in user_input:
        article = data.get("article", "Default long article text here")
        summary = summarizer(article, max_length=50, min_length=25, do_sample=False)
        return {"summary": summary[0]['summary_text']}

    return {"message": "Command not recognized"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)

