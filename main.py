from typing import Annotated
import sys
import logging
import time
import random

from fastapi import FastAPI, Query
from pydantic import BaseModel

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
logger.addHandler(logging.StreamHandler(sys.stdout))

random_seed = int(time.time())
random.seed(random_seed)
logger.info(f"Random seed set to: {random_seed}")

app = FastAPI(
    title="Dice Roller API",
    description="An API to roll dice with customizable sides and number of rolls.",
    version="1.0.0",
)


class DiceRequest(BaseModel):
    sides: int = 6
    rolls: int = 1


class DiceResponse(BaseModel):
    rolls: list[int]
    total: int


@app.get("/dice")
def dice_roll(request: Annotated[DiceRequest, Query()]) -> DiceResponse:
    rolls = [random.randint(1, request.sides) for _ in range(request.rolls)]
    total = sum(rolls)
    logger.info(f"Rolled {request.rolls} dice with {request.sides} sides: {rolls}, Total: {total}")
    return DiceResponse(rolls=rolls, total=total)


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8002)
