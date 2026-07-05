# vikey-mcp-server

An [MCP (Model Context Protocol)](https://modelcontextprotocol.io) server that exposes the [Vikey](https://www.vikey.it) API to any MCP-compatible AI client (Cursor, Claude Desktop, etc.).

## Tools

| Tool | Description |
|---|---|
| `list_external_reservations` | Retrieve reservations via the external endpoint (`/ext/reservations`) |
| `list_reservations` | Retrieve all reservations with optional filters (`/reservations`) |
| `list_locals` | List properties / apartments (`/locals`) |
| `get_reservation_detail` | Get full detail of a single reservation (`/v3/resv/resv`) |
| `get_reservation_services` | Get services / payment info for a reservation (`/v3/pay/services`) |

## Requirements

- Python ≥ 3.10
- A valid Vikey API key

## Installation

### Via `uvx` (recommended – no install needed)

```bash
uvx vikey-mcp-server
```

### Via `pip`

```bash
pip install vikey-mcp-server
vikey-mcp-server
```

## Configuration

Set the `VIKEY_API_KEY` environment variable before starting the server:

```bash
export VIKEY_API_KEY=your_api_key_here
```

## Cursor / Claude Desktop integration

Add the following block to your MCP client configuration file.

**Cursor** (`~/.cursor/mcp.json` or `.cursor/mcp.json` in the project):

```json
{
  "mcpServers": {
    "vikey": {
      "command": "uvx",
      "args": ["vikey-mcp-server"],
      "env": {
        "VIKEY_API_KEY": "your_api_key_here"
      }
    }
  }
}
```

**Claude Desktop** (`~/Library/Application Support/Claude/claude_desktop_config.json`):

```json
{
  "mcpServers": {
    "vikey": {
      "command": "uvx",
      "args": ["vikey-mcp-server"],
      "env": {
        "VIKEY_API_KEY": "your_api_key_here"
      }
    }
  }
}
```

## Tool reference

### `list_external_reservations`

| Parameter | Type | Required | Description |
|---|---|---|---|
| `last_updated` | `string` | No | Return reservations updated after this date (`YYYY-MM-DD`) |
| `checkin_status` | `string` | No | `NONEED` · `WAIT` · `PEND` · `OK` |

### `list_reservations`

| Parameter | Type | Required | Description |
|---|---|---|---|
| `checkin_status` | `string` | No | `NONEED` · `WAIT` · `PEND` · `OK` |
| `last_updated` | `string` | No | Return reservations updated after this date (`YYYY-MM-DD`) |
| `external_key` | `string` | No | External key identifying the apartment |
| `integr_ref` | `string` | No | Reservation external key from a Vikey integration |

### `list_locals`

| Parameter | Type | Required | Description |
|---|---|---|---|
| `date_from` | `string` | No | Apartments created from this date (`YYYY-MM-DD`) |
| `date_to` | `string` | No | Apartments created up to this date (`YYYY-MM-DD`) |
| `installed` | `integer` | No | `1` = installed only · `0` = not installed only |
| `local_key` | `string` | No | Unique identifier of a specific apartment |

### `get_reservation_detail`

| Parameter | Type | Required | Description |
|---|---|---|---|
| `resv_key` | `string` | **Yes** | Reservation identifier (e.g. `29FG3DI6`) |

### `get_reservation_services`

| Parameter | Type | Required | Description |
|---|---|---|---|
| `resv_key` | `string` | **Yes** | Reservation identifier (e.g. `29FG3DI6`) |

## Development

```bash
# Clone and install
git clone https://github.com/tosettil/vikey-mcp-server.git
cd vikey-mcp-server
uv sync

# Run locally
VIKEY_API_KEY=your_key uv run vikey-mcp-server
```

## Release workflow

Releases are automated via GitHub Actions. Use the **Bump version** workflow from the Actions tab to choose `patch`, `minor`, or `major`. The workflow will:

1. Bump the version in `pyproject.toml`
2. Create and push the corresponding `vX.Y.Z` tag
3. The tag push triggers the **Publish** workflow, which builds and pushes the package to PyPI

### One-time setup

- **PyPI Trusted Publisher**: on [pypi.org](https://pypi.org), configure a trusted publisher for this project pointing at `tosettil-polimi/vikey-mcp-server`, workflow `publish.yml`. No `PYPI_API_TOKEN` is required.
- **`RELEASE_PAT` repository secret**: create a fine-grained Personal Access Token with `contents: write` permission on this repo and add it as the `RELEASE_PAT` secret. This is required because pushes made with the default `GITHUB_TOKEN` do **not** trigger other workflows (GitHub's anti-loop protection), so without a PAT the tag pushed by `bump-version.yml` would never trigger `publish.yml`.

## License

MIT
