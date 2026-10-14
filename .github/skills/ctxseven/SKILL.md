---
name: ctxseven
description: Fetch current, version-specific documentation and examples for public third-party libraries through Context7 before writing code against their APIs. Use when library versions, function signatures, supported configuration, or framework patterns may have changed.
---

# Context7 Remote MCP CLI (`ctxseven`)

`ctxseven` is a zero-dependency CLI for the official Context7 remote MCP server (`https://mcp.context7.com/mcp`). It dynamically discovers live tools and retrieves only the version-specific third-party library documentation needed for the current task.

## When to Use

Use `ctxseven` before implementing code against an external public dependency when:
- API signatures or configuration may have changed since the model's training data.
- The library or framework version matters.
- You need current, source-grounded examples or migration guidance.
- You are unsure which official package, library ID, or documentation source applies.

Do not use it for the active local repository: read and search the local files instead.

## Pre-flight Check

```bash
echo "${CONTEXT7_API_KEY:?CONTEXT7_API_KEY is not set. Run: export CONTEXT7_API_KEY='your-key'}"
which ctxseven || command -v ctxseven || Get-Command ctxseven
```

If missing, see [INSTALL.md](INSTALL.md), or install with:

```bash
uv tool install git+https://github.com/davidw-philips/ctxseven
```

## Workflow

1. Discover the server's current tools:

```bash
ctxseven --help
```

2. Inspect a tool's live schema before using it:

```bash
ctxseven --tool resolve-library-id description
ctxseven --tool query-docs description
```

3. Resolve the Context7 library ID, then request one focused documentation topic:

```bash
ctxseven call resolve-library-id '{"libraryName":"FastAPI","query":"dependency injection"}'
ctxseven call query-docs '{"libraryId":"/fastapi/fastapi","query":"dependency injection","language":"Python"}'
```

## Rules

- Resolve the library ID before querying documentation unless the user provided a valid `/organization/project` Context7 ID.
- Use a specific documentation query; split unrelated questions into separate calls.
- Treat Context7 output as third-party dependency context, then apply it to the local project conventions.