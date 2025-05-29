from langchain_deepseek import ChatDeepSeek
from langchain_mcp_adapters.client import MultiServerMCPClient
from langgraph.prebuilt import create_react_agent
 
# 初始化DeepSeek
llm = ChatDeepSeek(
    model="deepseek-chat",
    api_key="your_api_key_here",
    temperature=0.3
)
 
# 配置MCP Client
mcp_client = MultiServerMCPClient(
    servers={
        "finance": "http://localhost:8000"  # AKShare MCP Server地址
    }
)
 
# 创建React Agent
agent = create_react_agent(llm, mcp_client)