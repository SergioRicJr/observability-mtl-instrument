import random
import uvicorn
import httpx
from fastapi import FastAPI
from  middleware.ObservabilityMiddleware import ObservabilityMiddleware
from observability_config.log_config import LogConfig
from starlette_prometheus import metrics, PrometheusMiddleware
from observability_config.trace_config import TraceConfig
from opentelemetry.instrumentation.fastapi import FastAPIInstrumentor
from opentelemetry.propagate import inject
import logging

trace_config = TraceConfig(service_name="fastapi-module", tempo_url="http://nginx:80/tempo/v1/traces")
trace = trace_config.get_trace()

log_config = LogConfig(
    service_name='fastapi-app',
    log_level=logging.DEBUG,
    loki_url='http://nginx:80/loki/api/v1/push',
    extra_labels={'esse': 'adge'}
)

logger = log_config.get_logger()

app = FastAPI()

app.add_middleware(ObservabilityMiddleware)
app.add_middleware(PrometheusMiddleware)
app.add_route("/metrics", metrics)

@app.get("/")
def welcome():
    logger.info('hello message was sent')
    return {"message": "Hello, welcome to the application!"}

@app.get("/random")
def get_random_number():
    random_number = random.randint(0, 100)
    print("random")
    logger.info('random number between 0 and 100 was calculated')
    return {"message": f"The random number was created", "number": random_number}

def calc_factorial(number):
    factorial = 1
    for i in range(1, number + 1):
        factorial *= i
    return factorial

@app.get("/factorial")
async def get_factorial():
    headers = {}
    inject(headers)  # inject trace info to header
    logger.critical(headers)

    async with httpx.AsyncClient() as client:
        random_number = await client.get('http://localhost:8000/random', headers=headers)
    random_number = random_number.json()
    random_number = random_number['number']
    factorial = calc_factorial(random_number)
    logger.info('factorial was calculated successfully')
    return {"message": f"The factorial of number {random_number} is {factorial}"}
    
@app.get("/requests")
async def multiple_requests():
    headers = {}
    inject(headers)  # inject trace info to header
    logger.critical(headers)

    async with httpx.AsyncClient() as client:
        await client.get("http://localhost:8000/", headers=headers)
    async with httpx.AsyncClient() as client:
        await client.get("http://localhost:8000/random", headers=headers)
    async with httpx.AsyncClient() as client:
        await client.get("http://localhost:8000/factorial", headers=headers)
    logger.info('multiple requests were made successfully')
    return {"message": "Multiple requests are sent"}

FastAPIInstrumentor.instrument_app(app, tracer_provider=trace.get_tracer_provider())

if __name__ == "__main__":
    uvicorn.run(
        app,
        host="0.0.0.0",
        port=8000
    )