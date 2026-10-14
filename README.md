# ctxseven: Context7 Remote MCP CLI Client

`ctxseven` is a lightweight, token-efficient command-line interface for the official [Context7 remote MCP server](https://mcp.context7.com/mcp).

It dynamically discovers the live Context7 tools, retrieves a tool's current description and schema only when needed, and calls it directly. This avoids configuring an MCP client or loading tool definitions into an agent's context before they are useful.

- **Zero third-party dependencies:** pure Python 3 standard library.
- **Cross-platform:** macOS, Linux, and Windows.
- **Version-aware documentation:** retrieve current library documentation and code examples instead of relying on stale model knowledge.
- **Dynamic contract:** `--help` lists live tools, `--tool <name> description` inspects one, and `call` invokes it.

## Prerequisites

Create a Context7 API key and expose it as `CONTEXT7_API_KEY`:

```bash
export CONTEXT7_API_KEY="your-context7-api-key"
```

On Windows PowerShell:

```powershell
$env:CONTEXT7_API_KEY="your-context7-api-key"
```

## Installation

### `uv` (recommended)

```bash
uv tool install git+https://github.com/davidw-philips/ctxseven
```

### `uvx` (no installation)

```bash
uvx --from git+https://github.com/davidw-philips/ctxseven ctxseven --help
```

### `pipx` or `pip`

```bash
pipx install git+https://github.com/davidw-philips/ctxseven.git
pip install git+https://github.com/davidw-philips/ctxseven.git
```

### Local clone

```bash
git clone https://github.com/davidw-philips/ctxseven.git
cd ctxseven
pip install -e .
```

## Usage

Discover live Context7 tools:

```bash
ctxseven --help
```

Inspect a tool before use:

```bash
ctxseven --tool resolve-library-id description
ctxseven --tool query-docs description
```

Call the live tools with JSON arguments:

```bash
# Resolve a Context7 library ID first.
ctxseven call resolve-library-id '{"libraryName":"FastAPI","query":"dependency injection"}'

# Use the selected library ID in a focused documentation query.
ctxseven call query-docs '{"libraryId":"/fastapi/fastapi","query":"dependency injection","language":"Python"}'
```

## Agent Skills

This repository includes portable skill bundles for GitHub Copilot, Claude Code, OpenAI Codex, and generic agents. They guide agents to use Context7 for current, version-specific third-party library documentation before writing integration code.

- GitHub Copilot: `.github/skills/ctxseven/`
- Claude Code: `.claude/skills/ctxseven/`
- OpenAI Codex: `.codex/skills/ctxseven/`
- Generic agents: `.agents/skills/ctxseven/`

## Links

- Repository: [davidw-philips/ctxseven](https://github.com/davidw-philips/ctxseven)
- Context7 MCP: [mcp.context7.com/mcp](https://mcp.context7.com/mcp)

## License

MIT