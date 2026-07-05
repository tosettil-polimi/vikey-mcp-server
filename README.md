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

## Prompt utili

Prompt pronti all'uso da incollare in chat (Cursor/Claude) con il tool `vikey` mcp attivo. Incorporano gli accorgimenti emersi nell'uso reale (es. esclusione delle prenotazioni cancellate).

### Totale prenotazioni Airbnb / Booking per un mese

```
Usa il vikey mcp per calcolare il totale delle prenotazioni con check-in a [MESE] [ANNO] per l'appartamento [NOME APPARTAMENTO], separando i totali per canale Airbnb e Booking.

Regole:
- Recupera le prenotazioni con `list_reservations`.
- Escludi le prenotazioni con `DEL=1` (cancellate). NON fidarti del campo `canc`, che risulta spesso sempre a 0 anche per prenotazioni cancellate: usa `DEL`.
- Se trovi coppie di prenotazioni con stesso ospite, stesse date e stesso importo ma `resv_key` diverso, tienine solo una: verifica `DEL` per capire quale delle due è quella valida (DEL=0) e quale è la cancellata/duplicata (DEL=1).
- Conta come "del mese" le prenotazioni il cui check-in (`date_from`) cade nel mese richiesto.
- Per ciascun canale mostrami: numero di prenotazioni e totale importo (`price`).
- Poi elencami il dettaglio riga per riga (check-in → check-out, canale, ospite, importo), ordinato per data di check-in.
```

### Calcolo tassa di soggiorno per un mese

```
Usa il vikey mcp per calcolare il totale della tassa di soggiorno maturata per i soggiorni di [MESE] [ANNO] nell'appartamento [NOME APPARTAMENTO].

Regole:
- Recupera le prenotazioni con `list_reservations` e leggi la tariffa dal campo `city_tax_params` (es. importo per persona a notte in `perperson_price`, tetto massimo di notti tassabili per singolo soggiorno in `perperson_maxdays`).
- Escludi le prenotazioni con `chk_citytax=0` (tassa non applicabile) e quelle con `DEL=1` (cancellate). NON fidarti del campo `canc`, spesso sempre a 0: usa `DEL`.
- Se trovi coppie di prenotazioni con stesso ospite, stesse date e stesso importo ma `resv_key` diverso, tienine solo una valida (verifica `DEL`: la cancellata ha `DEL=1`).
- Per ogni soggiorno calcola le notti totali (`date_to` - `date_from`), poi applica il tetto (notti tassabili = min(notti totali, `perperson_maxdays`)), contando il tetto a partire dal check-in.
- Se il soggiorno è a cavallo tra due mesi, conta solo le notti tassabili che ricadono nel mese richiesto (es. per un soggiorno a cavallo maggio/giugno, nel calcolo di giugno conta solo le notti di giugno).
- Formula per riga: tassa = tariffa_per_persona × `guests_num` × notti_tassabili_nel_mese.
- Mostrami il dettaglio riga per riga (check-in → check-out, canale, ospite, ospiti, notti tassabili nel mese, importo) e il totale finale del mese.
```

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
