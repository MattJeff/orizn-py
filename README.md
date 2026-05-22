# orizn

Official Python SDK for the [Orizn Visa API](https://visa.orizn.app).

Check visa requirements for **39,585 passport-destination pairs** in **15 languages**.

## Install

```bash
pip install orizn
```

## Quick start

```python
from orizn import Orizn

# No API key needed for quick checks
client = Orizn()
result = client.check("FRA", "JPN")
print(result.requirement)    # "visa_free"
print(result.visa_free_days) # 90

# Full details (get free key at visa.orizn.app)
client = Orizn(api_key="your-key")
visa = client.get_visa("USA", "CHN", lang="fr")
print(visa.documents_required)
print(visa.process)
print(visa.tips)
```

## Methods

| Method | Auth | Description |
|--------|------|-------------|
| `check(passport, destination)` | None | Quick visa check |
| `get_visa(passport, destination, lang?)` | Key | Full details |
| `bulk(passport, lang?)` | Key (Pro) | All destinations |
| `changes(passport?, destination?)` | Key (Starter) | Policy changes |
| `stats()` | None | Coverage stats |

## Links

- [Get free API key](https://visa.orizn.app)
- [API Docs](https://visa.orizn.app/visa-api/dashboard/docs)
- [MCP Server](https://github.com/MattJeff/orizn-mcp-server)
- [npm SDK](https://www.npmjs.com/package/orizn)
