# -*- coding: utf-8 -*-

from copy import deepcopy
import json
import os
import secrets

from fastapi import FastAPI, Request, Query, Path
from fastapi.responses import HTMLResponse, JSONResponse
from loguru import logger

from cloudflare_error_page import render

IATA_FILE = os.getenv("IATA_FILE", "iata.json")
CONFIG_FILE = os.getenv("CONFIG_FILE", "config.json")

app = FastAPI()

iata_codes: dict
if os.path.exists(IATA_FILE):
    try:
        with open(IATA_FILE, "r", encoding="utf-8") as fp:
            iata_codes = json.load(fp)
    except Exception:
        logger.exception("Error loading iata.json")
        iata_codes = {}
else:
    logger.error("IATA_FILE not found")
    iata_codes = {}

config: dict
if os.path.exists(CONFIG_FILE):
    try:
        with open(CONFIG_FILE) as f:
            config = json.load(f)
    except Exception:
        logger.exception("Error loading config.json")
        config = {}
else:
    logger.error("CONFIG_FILE not found")
    config = {}


def get_region(code: str):
    city: str = iata_codes.get(code.upper(), "Unknown, Unknown")
    region, _ = city.split(",", 2)
    return region.strip()


@app.get("/debug")
async def debug(request: Request, code: int = Query(200)):
    return JSONResponse(
        content={k:v for k, v in request.headers.items()},
        status_code=code,
    )


@app.route("/{full_path:path}")
def index(request: Request, full_path: str = Path(...)):
    cf_connecting_ip = request.headers.get("CF-Connecting-IP")
    x_forwarded_for = request.headers.get("X-Forwarded-For")
    client_ip = cf_connecting_ip or x_forwarded_for or request.client.host

    cf_ray = request.headers.get("CF-Ray")
    if not (cf_ray and "-" in cf_ray):
        cf_ray = f"{secrets.token_hex(8)}-UNK"
    ray_id, code = cf_ray.split("-", 1)

    params = deepcopy(config)
    if "cloudflare_status" in params and isinstance(params["cloudflare_status"], dict):
        params["cloudflare_status"]["location"] = get_region(code)
    else:
        params["cloudflare_status"] = {"location": get_region(code)}
    
    params["ray_id"] = ray_id
    params["client_ip"] = client_ip

    return HTMLResponse(render(params))


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000, access_log=False)
