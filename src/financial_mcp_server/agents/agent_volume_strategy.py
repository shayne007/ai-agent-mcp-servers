from langgraph.prebuilt import create_react_agent
from langchain_core.messages import SystemMessage, HumanMessage
from financial_mcp_server.llms.DeepSeek import DeepSeekV3
from financial_mcp_server.tools.stock_price_volume import stock_price
from financial_mcp_server.tools.strategies import vol_info

llm = DeepSeekV3()

pre_built_agent = create_react_agent(llm, tools=[stock_price, vol_info])

# 保存代理工作流程图到文件
graph_png = pre_built_agent.get_graph(xray=True).draw_mermaid_png()
with open("agent_graph.png", "wb") as f:
    f.write(graph_png)


# Invoke
prompt = """
你是一位金融分析师，擅长使用工具对股票进行量能分析。
工具1：stock_price
    获取股票指定日期前三天与后三天（包含指定日期）的收盘价
    
工具2：vol_info
    计算指定日期后3天（含指定日期）与前3天的成交量比值

要求：
需要分析出股票属于以下量价关系（量增价涨，量缩价涨，量增价跌，量缩价跌）中的哪一种，并给出分析结论
"""
messages = [SystemMessage(content=prompt), HumanMessage(content="600600 这只股票在 2024-09-26 左右的表现如何？")]
messages = pre_built_agent.invoke({"messages": messages})
for m in messages["messages"]:
    m.pretty_print()