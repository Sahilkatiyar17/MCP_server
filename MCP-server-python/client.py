import asyncio
from mcp.client.session import ClientSession
from mcp.client.stdio import stdio_client
from mcp import ClientSession, StdioServerParameters
from groq import Groq
import os 
from dotenv import load_dotenv
from utils import get_response_from_llm

load_dotenv() 


server_params = StdioServerParameters(
    command="python",
    args=['mcp_server.py'],
    env=None
)

async def main():
    async with stdio_client(server_params) as (read_stream, write_stream):
        async with ClientSession(read_stream, write_stream) as session:
            
            await session.initialize()
            tools_response = await session.list_tools()
            print("Available tools:", [t.name for t in tools_response.tools])
            query = "what to download the langchain?"
            library = "langchain"
            res = await session.call_tool("get_docs",arguments={"query":query,"library":library})
            context = res.content
            user_prompt = f"Context: {context}\n\nQuestion: {query}"
            # LLM function to create a human readable response
            SYSTEM_PROMPT = """
            "Answer only using the provided context. If information is missing say you don't know."
            "Keep every 'SOURCE' line exactly; list sources in the end."
            """
            answer = get_response_from_llm(user_prompt=user_prompt,system_prompt=SYSTEM_PROMPT,model="openai/gpt-oss-20b")
            print(answer)
if __name__ == "__main__":
    asyncio.run(main())