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


async def fetch_url(url:str):
    #client
    async with httpx.AsyncClient() as client:
        #hit request to url
        response = await client.get(url,timeout=30.0)
        #parse and clean data
        cleaned_response = clean_html_to_text(response.text)
        #return cleaned data 
        return cleaned_response
    
    
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
        raise ValueError(f"Library {library} not found")
    
    speical_query = f"site:{docs_urls[library]} {query}"
    results = await search_web(speical_query)
    if len(results["organic"]) == 0:
        return "No results found"
    
    
    text_parts = []
    for result in results["organic"]:
        link = result.get("link","")
        if len(link) == 0:
            print('No link found')
        raw = await fetch_url(link)
        if raw:
            labeled = f'SORUCE: {link}\n\n{raw}'
            print('SORUCE',link)
            text_parts.append(labeled)
    return "\n\n".join(text_parts)


def main():
    mcp.run(transport ="stdio")
    
if __name__ == "__main__":
    main()