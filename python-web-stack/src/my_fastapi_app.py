import asyncio
import time

from fastapi import FastAPI

app = FastAPI()


@app.get("/")
def hello() -> str:
    return "Hello, World!"


@app.get("/sync")
def sync() -> dict[str, str]:
    time.sleep(1)
    return {"type": "sync"}


@app.get("/async")
async def async_() -> dict[str, str]:
    await asyncio.sleep(1)
    return {"type": "async"}


@app.get("/hello/{name}")
def hello_name(name: str) -> str:
    return f"Your name is: {name}"


@app.get("/compute")
def cpu_bound() -> dict[str, int]:
    # Simulate CPU-bound work (e.g., calculate Fibonacci)
    def fib(n: int) -> int:
        if n <= 1:
            return n
        return fib(n - 1) + fib(n - 2)

    result = fib(30)  # Adjust n for desired intensity
    return {"result": result}


@app.get("/io")
def io_bound() -> dict[str, str]:
    time.sleep(0.2)  # Simulate IO wait
    return {"type": "io-bound"}
