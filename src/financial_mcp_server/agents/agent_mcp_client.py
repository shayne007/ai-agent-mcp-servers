from financial_mcp_server.llms.DeepSeek import DeepSeekV3
from langchain_mcp_adapters.client import MultiServerMCPClient
from langgraph.prebuilt import create_react_agent
import asyncio

async def get_tools(mcp_client):
    return await mcp_client.get_tools()

async def main():
    # 初始化DeepSeek
    llm = DeepSeekV3()

    # 配置MCP Client Using SSE
    mcp_client = MultiServerMCPClient(
        {
            "finance": {
                "transport": "sse",
                "url": "http://127.0.0.1:8000/sse"  # AKShare MCP Server SSE endpoint
            }
        }
    )

    # 获取工具
    tools = await get_tools(mcp_client)

    # 创建反应代理
    agent = create_react_agent(llm, tools)
    
    # 测试代理
    response = await agent.ainvoke({
        "messages": [{
            "role": "user",
            "content": "腾讯控股过去一周的股价表现如何？"
        }]
    })
    print("Agent response:", response)

# 运行主协程
asyncio.run(main())