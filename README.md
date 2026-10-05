# hello-mcp

Een minimale "hello world" MCP (Model Context Protocol) server in Python, gebouwd met
[FastMCP](https://gofastmcp.com). Draait over stdio en is klaar om te deployen op
[Prefect Horizon](https://horizon.prefect.io).

De server stelt beschikbaar:

- **Tool** `hello(name="world")` — geeft een begroeting terug.
- **Resource** `greeting://hello` — een statische "Hello, world!" tekst.

## Live endpoint

De server draait op **https://greefhorst.fastmcp.app/mcp** (Prefect Horizon).
Horizon-authenticatie staat aan, dus clients loggen in via OAuth (GitHub/Google) voordat ze
de server kunnen aanroepen.

## Draaien

Met [uv](https://docs.astral.sh/uv/) (aanbevolen):

```bash
uv run server.py
```

Of met een eigen virtualenv:

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
python server.py
```

De server praat JSON-RPC over stdin/stdout, dus handmatig starten "hangt" — dat is normaal.
Een MCP-client start hem en stuurt verzoeken.

## Aansluiten op een MCP-client (lokaal)

Voeg toe aan de MCP-configuratie van je client (bijv. `claude_desktop_config.json`):

```json
{
  "mcpServers": {
    "hello": {
      "command": "uv",
      "args": ["--directory", "/Users/dgreefhorst/Documents/GitHub/test", "run", "server.py"]
    }
  }
}
```

## Aansluiten op de live server

Voor de remote (Horizon) endpoint gebruik je een HTTP-configuratie. Bij de eerste verbinding
start de client de OAuth-login:

```json
{
  "mcpServers": {
    "hello": {
      "type": "http",
      "url": "https://greefhorst.fastmcp.app/mcp"
    }
  }
}
```

## Deployen op Prefect Horizon

Horizon bouwt je server uit een GitHub-repo en host hem op een stabiele URL
(`https://<naam>.fastmcp.app/mcp`) met OAuth-authenticatie. Deze repo is daar klaar voor:

- Entrypoint: `server.py` (de FastMCP-instantie heet `mcp`, dus `server.py:mcp` werkt ook).
- Dependencies: `requirements.txt` met `fastmcp` — Horizon installeert die tijdens de build.

Stappen:

1. Push deze repo naar GitHub (`github.com/dgreefhorst/test`).
2. Ga naar jouw workspace: https://horizon.prefect.io/greefhorst/
3. Maak een server aan en koppel de GitHub-repo (`dgreefhorst/test`).
4. Vul in: **Server name** `hello-world`, **Entrypoint** `server.py`.
5. Klik **Deploy Server**. Horizon bouwt en deployt naar `https://<naam>.fastmcp.app/mcp`.

Deze repo is al gedeployed op `https://greefhorst.fastmcp.app/mcp`. Elke push naar de default
branch maakt automatisch een nieuwe build en deployment.

## Zelf testen

```bash
uv run smoke_test.py
```

stuurt een initialize + `tools/call` handshake naar de server en print het antwoord.
