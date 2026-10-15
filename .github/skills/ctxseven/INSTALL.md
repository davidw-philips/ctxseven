
## Enterprise TLS certificates

The CLI verifies HTTPS certificates. For networks that use TLS inspection, set a trusted enterprise CA bundle before running it:

```powershell
$env:SSL_CERT_FILE = 'C:\path\to\corporate-ca-bundle.pem'
# Or use a directory containing hashed CA certificates:
$env:SSL_CERT_DIR = 'C:\path\to\corporate-ca-directory'
ctxseven --help
```

Keep certificate verification enabled. The variables are passed through automatically when `ctxseven` is launched from an MCP host.
# Install `ctxseven`

```bash
uv tool install git+https://github.com/davidw-philips/ctxseven
export CONTEXT7_API_KEY="your-context7-api-key"
ctxseven --help
```

Alternatives:

```bash
uvx --from git+https://github.com/davidw-philips/ctxseven ctxseven --help
pipx install git+https://github.com/davidw-philips/ctxseven.git
pip install git+https://github.com/davidw-philips/ctxseven.git
```