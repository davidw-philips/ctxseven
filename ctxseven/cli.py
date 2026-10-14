#!/usr/bin/env python3
"""ctxseven: dynamically inspect and call the Context7 remote MCP server."""

from __future__ import annotations

import json
import os
import sys
import urllib.error
import urllib.request
from typing import Any, Dict, List, Optional

MCP_URL = os.environ.get("CTXSEVEN_ENDPOINT", "https://mcp.context7.com/mcp")
USER_AGENT = "ctxseven-cli/0.1.0 (+https://github.com/davidw-philips/ctxseven)"


def get_api_key() -> str:
    """Retrieve the Context7 API key or provide an actionable error."""
    api_key = os.environ.get("CONTEXT7_API_KEY", "").strip()
    if not api_key:
        print(
            "Error: CONTEXT7_API_KEY environment variable is not set.\n"
            "Set it with: export CONTEXT7_API_KEY='your-api-key'",
            file=sys.stderr,
        )
        sys.exit(1)
    return api_key


def rpc_request(method: str, params: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
    """Send a JSON-RPC request to Context7 and parse JSON or SSE responses."""
    payload = {
        "jsonrpc": "2.0",
        "id": 1,
        "method": method,
        "params": params or {},
    }
    request = urllib.request.Request(
        MCP_URL,
        data=json.dumps(payload).encode("utf-8"),
        headers={
            "Content-Type": "application/json",
            "Accept": "application/json, text/event-stream",
            "User-Agent": USER_AGENT,
            "CONTEXT7_API_KEY": get_api_key(),
        },
    )

    try:
        with urllib.request.urlopen(request, timeout=60) as response:
            raw_response = response.read().decode("utf-8")
    except urllib.error.HTTPError as error:
        body = error.read().decode("utf-8", errors="replace")
        print(f"HTTP {error.code} calling Context7 MCP: {body}", file=sys.stderr)
        sys.exit(1)
    except urllib.error.URLError as error:
        print(f"Network error calling Context7 MCP: {error.reason}", file=sys.stderr)
        sys.exit(1)

    for line in raw_response.splitlines():
        if line.startswith("data:"):
            try:
                return json.loads(line.removeprefix("data:").strip())
            except json.JSONDecodeError:
                continue

    try:
        return json.loads(raw_response)
    except json.JSONDecodeError as error:
        print(f"Failed to decode Context7 MCP response: {error}\n{raw_response}", file=sys.stderr)
        sys.exit(1)


def list_tools() -> List[Dict[str, Any]]:
    """Get the current Context7 tool definitions."""
    response = rpc_request("tools/list")
    if "error" in response:
        print(f"MCP error: {json.dumps(response['error'])}", file=sys.stderr)
        sys.exit(1)
    return response.get("result", {}).get("tools", [])


def find_tool(tool_name: str, tools: List[Dict[str, Any]]) -> Optional[Dict[str, Any]]:
    """Match a live tool by its exact name."""
    return next((tool for tool in tools if tool.get("name") == tool_name), None)


def print_help(tools: List[Dict[str, Any]]) -> None:
    """Print usage and dynamically discovered Context7 tools."""
    print("usage: ctxseven [--help] [--tool TOOL_NAME description] [call TOOL_NAME [ARGS_JSON]]\n")
    print("Context7 MCP CLI - fetch current, version-specific library documentation.\n")
    print("Commands:")
    print("  --help, -h                  List tools currently available from Context7")
    print("  --tool <name> description   Print a tool's live description and input schema")
    print("  call <tool_name> [args]     Call a Context7 tool with JSON arguments\n")
    print(f"Available tools from {MCP_URL}:")
    for tool in tools:
        name = tool.get("name", "unknown")
        description = tool.get("description", "").splitlines()[0].strip()
        print(f"  {name:<24} {description}")
    print("\nInspect a tool before calling it: ctxseven --tool <tool_name> description")


def print_tool_description(tool_name: str, tools: List[Dict[str, Any]]) -> None:
    """Print live metadata and input schema for a Context7 tool."""
    tool = find_tool(tool_name, tools)
    if tool is None:
        names = ", ".join(tool.get("name", "unknown") for tool in tools)
        print(f"Error: Tool '{tool_name}' was not found. Available tools: {names}", file=sys.stderr)
        sys.exit(1)

    print(f"Tool: {tool.get('name')}")
    print("=" * 60)
    print(f"\nDescription:\n{tool.get('description', 'No description available.')}\n")
    print("Input Schema:")
    print(json.dumps(tool.get("inputSchema", {}), indent=2))


def print_result(response: Dict[str, Any]) -> None:
    """Render Context7 text results without hiding non-text MCP content."""
    if "error" in response:
        print(f"MCP error: {json.dumps(response['error'], indent=2)}", file=sys.stderr)
        sys.exit(1)

    result = response.get("result", {})
    content = result.get("content", [])
    if not content:
        print(json.dumps(result, indent=2))
        return

    for item in content:
        if item.get("type") == "text":
            print(item.get("text", ""))
        else:
            print(json.dumps(item, indent=2))


def call_tool(tool_name: str, args_json: Optional[str], tools: List[Dict[str, Any]]) -> None:
    """Call one dynamically discovered Context7 tool."""
    if find_tool(tool_name, tools) is None:
        names = ", ".join(tool.get("name", "unknown") for tool in tools)
        print(f"Error: Tool '{tool_name}' was not found. Available tools: {names}", file=sys.stderr)
        sys.exit(1)

    try:
        arguments = json.loads(args_json) if args_json else {}
    except json.JSONDecodeError as error:
        print(f"Error parsing JSON arguments: {error}", file=sys.stderr)
        sys.exit(1)
    if not isinstance(arguments, dict):
        print("Error: Tool arguments must be a JSON object.", file=sys.stderr)
        sys.exit(1)

    print_result(rpc_request("tools/call", {"name": tool_name, "arguments": arguments}))


def main() -> None:
    """Run the ctxseven command-line interface."""
    args = sys.argv[1:]
    tools = list_tools()

    if not args or args[0] in {"--help", "-h", "help"}:
        print_help(tools)
        return

    if args[0] == "--tool":
        if len(args) < 3 or args[2] != "description":
            print("Usage: ctxseven --tool <tool_name> description", file=sys.stderr)
            sys.exit(1)
        print_tool_description(args[1], tools)
        return

    if args[0] == "call":
        if len(args) < 2:
            print("Usage: ctxseven call <tool_name> [json_arguments]", file=sys.stderr)
            sys.exit(1)
        call_tool(args[1], " ".join(args[2:]) or None, tools)
        return

    print(f"Unknown command: {' '.join(args)}", file=sys.stderr)
    print("Run 'ctxseven --help' for usage.", file=sys.stderr)
    sys.exit(1)


if __name__ == "__main__":
    main()