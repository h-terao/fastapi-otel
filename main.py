from typing import Annotated
import os
import sys
import logging
import time
import random

from fastapi import FastAPI, Query
from pydantic import BaseModel
from opentelemetry import trace
from opentelemetry.sdk.resources import Resource
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import BatchSpanProcessor
from opentelemetry.exporter.otlp.proto.http.trace_exporter import OTLPSpanExporter
from opentelemetry.instrumentation.fastapi import FastAPIInstrumentor
from opentelemetry.instrumentation.logging import LoggingInstrumentor

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

random_seed = int(time.time())
random.seed(random_seed)
logger.info(f"Random seed set to: {random_seed}")

resource = Resource(attributes={"service.name": os.getenv("OTEL_SERVICE_NAME", "dice_roller")})
provider = TracerProvider(resource=resource)
otlp_endpoint = os.getenv("OTEL_EXPORTER_OTLP_ENDPOINT", "http://localhost:4318/v1/traces")
otlp_exporter = OTLPSpanExporter(endpoint=otlp_endpoint)
provider.add_span_processor(BatchSpanProcessor(otlp_exporter))
trace.set_tracer_provider(provider)

LoggingInstrumentor().instrument(set_logging_format=True)

app = FastAPI(
    title="Dice Roller API",
    description="An API to roll dice with customizable sides and number of rolls.",
    version="1.0.0",
)

FastAPIInstrumentor.instrument_app(app, tracer_provider=provider)


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
