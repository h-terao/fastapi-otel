"""A script to roll dice using the API deployed at http://localhost:8002."""

import httpx

with httpx.Client(base_url="http://localhost:8002") as client:
    resp = client.get("/dice?sides=6&rolls=3")
    print("6d3:", resp.json())

    resp = client.get("/dice?sides=100&rolls=10")
    print("100d10:", resp.json())
