import time

from flask import Flask

app = Flask(__name__)


@app.route("/")
def hello() -> str:
    return "Hello, World!"


@app.route("/sync")
def sync() -> dict[str, str]:
    time.sleep(1)
    return {"type": "sync"}


@app.route("/hello/<name>")
def print_name(name: str) -> str:
    return f"Your name is: {name:s}"


@app.route("/compute")
def cpu_bound() -> dict[str, int]:
    # Simulate CPU-bound work (e.g., calculate Fibonacci)
    def fib(n: int) -> int:
        if n <= 1:
            return n
        return fib(n - 1) + fib(n - 2)

    result = fib(30)  # Adjust n for desired intensity
    return {"result": result}


@app.route("/io")
def io_bound() -> dict[str, str]:
    time.sleep(0.2)  # Simulate IO wait
    return {"type": "io-bound"}


# # Flask development server
# if __name__ == "__main__":
#     app.run()
