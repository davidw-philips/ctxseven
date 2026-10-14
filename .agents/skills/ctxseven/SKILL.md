---
name: ctxseven
description: Fetch current, version-specific documentation and examples for public third-party libraries through Context7 before writing code against their APIs. Use when library versions, function signatures, supported configuration, or framework patterns may have changed.
---

# Context7 Remote MCP CLI (`ctxseven`)

Use `ctxseven` to fetch live, version-specific documentation for public third-party dependencies. Use it before implementing an unfamiliar or version-sensitive library API; use local files instead for the active repository.

## Pre-flight Check

```bash
echo "${CONTEXT7_API_KEY:?CONTEXT7_API_KEY is not set. Run: export CONTEXT7_API_KEY='your-key'}"
which ctxseven || command -v ctxseven || Get-Command ctxseven
```

Install it if needed:

```bash
uv tool install git+https://github.com/davidw-philips/ctxseven
```

## Workflow

```bash
# Discover current live tool names.
ctxseven --help

# Read a tool's description and schema before calling it.
ctxseven --tool resolve-library-id description
ctxseven --tool query-docs description

# Resolve a library ID, then request one specific topic.
ctxseven call resolve-library-id '{"libraryName":"FastAPI","query":"dependency injection"}'
ctxseven call query-docs '{"libraryId":"/fastapi/fastapi","query":"dependency injection","language":"Python"}'
```

See [INSTALL.md](INSTALL.md) for installation options.