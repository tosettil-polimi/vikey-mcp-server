import os
from typing import Optional

import httpx
from fastmcp import FastMCP

BASE_URL = "https://api.vikey.it/api"

mcp = FastMCP(
    "vikey-mcp-server",
    instructions=(
        "MCP server for the Vikey API. "
        "Requires the VIKEY_API_KEY environment variable to be set. "
        "All dates use the format YYYY-MM-DD."
    ),
)


def _client() -> httpx.Client:
    api_key = os.environ.get("VIKEY_API_KEY", "")
    if not api_key:
        raise RuntimeError("VIKEY_API_KEY environment variable is not set.")
    return httpx.Client(
        base_url=BASE_URL,
        headers={"Apitoken": api_key},
        timeout=30.0,
    )


def _get(path: str, params: dict) -> dict | list:
    clean = {k: v for k, v in params.items() if v is not None}
    with _client() as client:
        response = client.get(path, params=clean)
        response.raise_for_status()
        return response.json()


# ---------------------------------------------------------------------------
# External endpoints
# ---------------------------------------------------------------------------


@mcp.tool()
def list_external_reservations(
    last_updated: Optional[str] = None,
    checkin_status: Optional[str] = None,
) -> dict | list:
    """Retrieve all reservations via the external API endpoint.

    Args:
        last_updated: Return only reservations updated after this date (YYYY-MM-DD).
        checkin_status: Filter by check-in status. Allowed values: NONEED, WAIT, PEND, OK.
    """
    return _get("/ext/reservations", {"last_updated": last_updated, "checkin_status": checkin_status})


# ---------------------------------------------------------------------------
# Basic endpoints
# ---------------------------------------------------------------------------


@mcp.tool()
def list_reservations(
    checkin_status: Optional[str] = None,
    last_updated: Optional[str] = None,
    external_key: Optional[str] = None,
    integr_ref: Optional[str] = None,
) -> dict | list:
    """Retrieve all reservations.

    Args:
        checkin_status: Filter by check-in status. Allowed values: NONEED, WAIT, PEND, OK.
        last_updated: Return only reservations updated after this date (YYYY-MM-DD).
        external_key: External key identifying the apartment.
        integr_ref: Reservation external key if it comes from a Vikey integration.
    """
    return _get(
        "/reservations",
        {
            "checkin_status": checkin_status,
            "last_updated": last_updated,
            "external_key": external_key,
            "integr_ref": integr_ref,
        },
    )


@mcp.tool()
def list_locals(
    date_from: Optional[str] = None,
    date_to: Optional[str] = None,
    installed: Optional[int] = None,
    local_key: Optional[str] = None,
) -> dict | list:
    """List properties (locals/apartments).

    Args:
        date_from: Filter apartments created from this date (YYYY-MM-DD).
        date_to: Filter apartments created up to this date (YYYY-MM-DD).
        installed: 1 to return only installed apartments, 0 for not installed.
        local_key: Unique identifier of a specific apartment.
    """
    return _get(
        "/locals",
        {
            "date_from": date_from,
            "date_to": date_to,
            "installed": installed,
            "local_key": local_key,
        },
    )


@mcp.tool()
def get_reservation_detail(resv_key: str) -> dict | list:
    """Retrieve the detail of a single reservation.

    Args:
        resv_key: Mandatory reservation identifier (e.g. 29FG3DI6).
    """
    return _get("/v3/resv/resv", {"resv_key": resv_key})


@mcp.tool()
def get_reservation_services(resv_key: str) -> dict | list:
    """Retrieve services (payment details) associated with a reservation.

    Args:
        resv_key: Reservation identifier (e.g. 29FG3DI6).
    """
    return _get("/v3/pay/services", {"resv_key": resv_key})


# ---------------------------------------------------------------------------
# Entry point
# ---------------------------------------------------------------------------


def main() -> None:
    mcp.run()


if __name__ == "__main__":
    main()
