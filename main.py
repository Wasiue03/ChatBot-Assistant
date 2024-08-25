from fastapi import FastAPI, Request, HTTPException
from transformers import pipeline
from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup
import requests
import time

app = FastAPI()

summarizer = pipeline("summarization", model="facebook/bart-large-cnn")

def search_web(query):
    chrome_driver_path = r"C:\\Users\\HP\\Downloads\\chromedriver-win64\\chromedriver-win64\\chromedriver.exe"
    chrome_options = Options()
    chrome_options.add_argument("--start-maximized")  # Optional: Start Chrome maximized
    service = ChromeService(executable_path=chrome_driver_path)
    driver = None
    try:
        driver = webdriver.Chrome(service=service, options=chrome_options)
        driver.get(f"https://www.google.com/search?q={query}")
        
        # Wait for a few seconds to ensure the page loads
        time.sleep(10)
        
        # Get the page source and print for debugging
        page_source = driver.page_source
        print(page_source[:1000])  # Print the first 1000 characters for debugging
        
        # Example: Extracting search results (modify according to your needs)
        # This is just an example, actual implementation may vary
        results = driver.find_elements_by_css_selector('h3')  # Example CSS selector for search result titles
        if not results:
            print("No results found")
        
        search_results = [result.text for result in results]
        print(f"Search results: {search_results}")
        return search_results

    except Exception as e:
        print(f"Error searching web: {e}")
        raise HTTPException(status_code=500, detail="Failed to perform search")
    finally:
        if driver:
            driver.quit()

def fetch_article_content(url):
    try:
        response = requests.get(url)
        soup = BeautifulSoup(response.content, 'html.parser')
        paragraphs = soup.find_all('p')
        content = ' '.join([para.get_text() for para in paragraphs])
        return content
    except Exception as e:
        print(f"Error fetching article content: {e}")
        return None

@app.get("/ping")
async def ping():
    return {"message": "Server is running"}

@app.post("/chatbot")
async def chatbot(request: Request):
    try:
        data = await request.json()
        user_input = data['input']

        if "search" in user_input:
            query = user_input.split("search for ")[-1]
            urls = search_web(query)
            
            summaries = []
            for url in urls:
                content = fetch_article_content(url)
                if content:
                    summary = summarizer(content, max_length=150, min_length=50, do_sample=False)
                    summaries.append({"url": url, "summary": summary[0]['summary_text']})
            
            return {"summaries": summaries}

        return {"message": "Command not recognized"}

    except Exception as e:
        print(f"Error processing request: {e}")
        raise HTTPException(status_code=500, detail="Internal Server Error")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)
