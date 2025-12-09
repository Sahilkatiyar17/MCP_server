#Create AI webscrapping tool
#step1: Search the web
import http.client
import json
import os
from dotenv import load_dotenv
import asyncio # to run the async function 
import httpx #to create async function 
from utils import clean_html_to_text
from fastmcp import FastMCP 
import sys 

load_dotenv()

mcp = FastMCP('docs')

async def search_web(query:str) -> dict:
    payload = json.dumps({
    "q": query,
    "num":2
    })
    headers = {
    'X-API-KEY': os.getenv("SERPER_API_KEY"),
    'Content-Type': 'application/json'
    }
    
    
    
    
    #conn = http.client.HTTPSConnection("google.serper.dev")
    async with httpx.AsyncClient() as client:
        response = await client.post("https://google.serper.dev/search", headers=headers, data=payload,timeout=30.0)
        #conn.request("POST", "/search", payload, headers)
        response.raise_for_status()  #throw error , which will be helpful in debugging
        return response.json()
        
 
#res = asyncio.run(search_web(query)) 
#print(res)
#step2: Open only the official website


async def fetch_url(url: str):
    # MIMIC A BROWSER: Many sites block python-httpx without this header
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36"
    }
    async with httpx.AsyncClient(follow_redirects=True) as client:
        try:
            response = await client.get(url, headers=headers, timeout=30.0)
            # If status is 403/404, we should skip
            if response.status_code != 200:
                sys.stderr.write(f"Failed to fetch {url}: Status {response.status_code}\n")
                return None
            
            cleaned_response = clean_html_to_text(response.text)
            return cleaned_response
        except Exception as e:
            sys.stderr.write(f"Error fetching {url}: {e}\n")
            return None
    
#step3: Read doc and write code accordingly 
docs_urls = {
    "langchain":"python.langchain.com/docs",
    "llama-index":"docs.llamaindex.ai/en/stable",
    "openai":"platform.openai.com/docs",
    "uv":"docs.astral.sh/uv",
}
@mcp.tool()
async def get_docs(query:str,library:str):
    """
    Search the latest docs for a given query and library.
    Supports langchain,openai,llama-index and uv.
    
    Args:
        query (str): The query to search for(eg:"Publish a package with UV").
        library (str): The library to search in(e.g. "UV").
        
    Returns:
        Summarized text from the docs with source links.
        
    """
   
    if library not in docs_urls:
        return f"Library {library} not found"
    
    special_query = f"site:{docs_urls[library]} {query}"
    
    # Debug log
    sys.stderr.write(f"Searching for: {special_query}\n")
    
    results = await search_web(special_query)

    if "organic" not in results:
        return "No search results found."

    text_parts = []
    for result in results["organic"]:
        link = result.get("link", "")
        if not link:
            continue
            
        sys.stderr.write(f"Scraping: {link}\n") # Debug to stderr
        raw = await fetch_url(link)
        
        if raw:
            labeled = f'SOURCE: {link}\n\n{raw}'
            text_parts.append(labeled)
        else:
             sys.stderr.write(f"Could not extract text from: {link}\n")

    if not text_parts:
        return "Found links, but could not extract text from any of them. (Check stderr for details)"

    return "\n\n".join(text_parts)

def main():
    mcp.run(transport ="stdio",log_level="debug")
    
if __name__ == "__main__":
    main()