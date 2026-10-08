# Graph Report - or-EXWU7U  (2026-10-07)

## Corpus Check
- 4 files · ~1,793 words
- Verdict: corpus is large enough that graph structure adds value.
- Unclassified: 3 file(s) not represented in the graph (top: (none) 2, .lock 1)

## Summary
- 44 nodes · 62 edges · 9 communities (5 shown, 4 thin omitted)
- Extraction: 84% EXTRACTED · 16% INFERRED · 0% AMBIGUOUS · INFERRED: 10 edges (avg confidence: 0.95)
- Token cost: 0 input · 0 output

## Graph Freshness
- Built from commit: `c1a6751e`
- Run `git rev-parse HEAD` and compare to check if the graph is stale.
- Run `graphify update .` after code changes (no API cost).

## Community Hubs (Navigation)
- _get
- main.py
- vikey-mcp-server
- Tool reference
- Prompt utili
- Installation
- list_reservations
- Release workflow
- vikey-mcp-server

## God Nodes (most connected - your core abstractions)
1. `vikey-mcp-server` - 11 edges
2. `_get()` - 7 edges
3. `list_external_reservations()` - 6 edges
4. `list_reservations()` - 6 edges
5. `list_locals()` - 6 edges
6. `get_reservation_detail()` - 6 edges
7. `get_reservation_services()` - 6 edges
8. `Tools` - 6 edges
9. `Tool reference` - 6 edges
10. `Installation` - 3 edges

## Surprising Connections (you probably didn't know these)
- ``get_reservation_detail`` --references--> `get_reservation_detail()`  [INFERRED]
  README.md → src/vikey_mcp_server/main.py
- ``get_reservation_services`` --references--> `get_reservation_services()`  [INFERRED]
  README.md → src/vikey_mcp_server/main.py
- ``list_external_reservations`` --references--> `list_external_reservations()`  [INFERRED]
  README.md → src/vikey_mcp_server/main.py
- `Tools` --references--> `list_external_reservations()`  [INFERRED]
  README.md → src/vikey_mcp_server/main.py
- ``list_reservations`` --references--> `list_reservations()`  [INFERRED]
  README.md → src/vikey_mcp_server/main.py

## Import Cycles
- None detected.

## Communities (9 total, 4 thin omitted)

### Community 0 - "_get"
Cohesion: 0.25
Nodes (7): `list_locals`, Tools, _client(), _get(), get_reservation_detail(), get_reservation_services(), list_locals()

### Community 2 - "vikey-mcp-server"
Cohesion: 0.29
Nodes (6): Configuration, Cursor / Claude Desktop integration, Development, License, Requirements, vikey-mcp-server

### Community 3 - "Tool reference"
Cohesion: 0.33
Nodes (5): `get_reservation_detail`, `get_reservation_services`, `list_external_reservations`, Tool reference, list_external_reservations()

### Community 4 - "Prompt utili"
Cohesion: 0.67
Nodes (3): Calcolo tassa di soggiorno per un mese, Prompt utili, Totale prenotazioni Airbnb / Booking per un mese

### Community 5 - "Installation"
Cohesion: 0.67
Nodes (3): Installation, Via `pip`, Via `uvx` (recommended – no install needed)

## Knowledge Gaps
- **11 isolated node(s):** `vikey-mcp-server`, `Requirements`, `Via `uvx` (recommended – no install needed)`, `Via `pip``, `Configuration` (+6 more)
  These have ≤1 connection - possible missing edges or undocumented components. (Counts symbols only; 22 node(s) total have ≤1 connection when file, concept and rationale nodes are included.)
- **4 thin communities (<3 nodes) omitted from report** — run `graphify query` to explore isolated nodes.

## Suggested Questions
_Questions this graph is uniquely positioned to answer:_

- **Why does `vikey-mcp-server` connect `vikey-mcp-server` to `_get`, `Tool reference`, `Prompt utili`, `Installation`, `Release workflow`?**
  _High betweenness centrality (0.528) - this node is a cross-community bridge._
- **Why does `Tools` connect `_get` to `vikey-mcp-server`, `Tool reference`, `list_reservations`?**
  _High betweenness centrality (0.369) - this node is a cross-community bridge._
- **Why does `list_external_reservations()` connect `Tool reference` to `_get`, `main.py`?**
  _High betweenness centrality (0.109) - this node is a cross-community bridge._
- **Are the 2 inferred relationships involving `list_external_reservations()` (e.g. with ``list_external_reservations`` and `Tools`) actually correct?**
  _`list_external_reservations()` has 2 INFERRED edges - model-reasoned connections that need verification._
- **Are the 2 inferred relationships involving `list_reservations()` (e.g. with ``list_reservations`` and `Tools`) actually correct?**
  _`list_reservations()` has 2 INFERRED edges - model-reasoned connections that need verification._
- **Are the 2 inferred relationships involving `list_locals()` (e.g. with ``list_locals`` and `Tools`) actually correct?**
  _`list_locals()` has 2 INFERRED edges - model-reasoned connections that need verification._
- **What connects `vikey-mcp-server`, `Requirements`, `Via `uvx` (recommended – no install needed)` to the rest of the system?**
  _11 weakly-connected nodes found - possible documentation gaps or missing edges._