from langgraph.prebuilt import create_react_agent
from langchain_core.messages import HumanMessage
from financial_mcp_server.llms.DeepSeek import DeepSeekV3
from financial_mcp_server.tools.stock_price import tools

llm = DeepSeekV3()

pre_built_agent = create_react_agent(llm, tools=tools)

# 保存代理工作流程图到文件
graph_png = pre_built_agent.get_graph(xray=True).draw_mermaid_png()
with open("agent_graph.png", "wb") as f:
    f.write(graph_png)


# Invoke
messages = [HumanMessage(content="300750 是哪只股票的代码？")]
messages = pre_built_agent.invoke({"messages": messages})
for m in messages["messages"]:
    m.pretty_print()