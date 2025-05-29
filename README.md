# ai-agent-mcp-servers
This project provide mcp servers to fintech backend services to support data analysis.
The stock market data can be fetched from https://akshare.akfamily.xyz/data/stock/stock.html

# How to run
```bash
uv --directory /Users/fengshiyi/Downloads/shayne/learning/LLM/my-projects/fintech/ai-agent-mcp-servers/src/financial_mcp_server run ai-agent-mcp-servers
```
- Claude Desktop or Cline
when start the server as stdio
```json
{
    "mcpServers": {
        "job_hunting_server": {
            "command": "uv",
            "args": [
              "--directory",
              "/Users/fengshiyi/Downloads/shayne/learning/LLM/my-projects/fintech/ai-agent-mcp-servers/src/financial_mcp_server",
              "run",
              "ai-agent-mcp-servers"
            ]
          }
    }
  }

```
when start the server as sse
```json
{
    "mcpServers": {
        "job_hunting_server": {
            "command": "uv",
            "args": [
              "--directory",
              "/Users/fengshiyi/Downloads/shayne/learning/LLM/my-projects/fintech/ai-agent-mcp-servers/src/financial_mcp_server",
              "run",
              "ai-agent-mcp-servers"
            ]
          }
    }
  }

```