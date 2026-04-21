# Python web stack

To prepare the Python env, in the terminal, `cd` into this folder and run:

```shell
uv python install 3.14t
```

## How to run the app

Different ways to serve the app:

1. `Flask`:
   - Use case: development server
   - Single-process development server by default, and lacks the robustness and performance
   optimizations expected from production servers

    ```shell
    uv run --extra=flask \
      flask --app src/my_flask_app run --port 8000 --reload
    ```

2. `FastAPI`:
    - Use case: development server
    - `fastapi dev` is equivalent to `fastapi run`, but with reload enabled and listening on the
    `127.0.0.1` address
    - Under the hood, `fastapi run|dev` uses `uvicorn`
    - Can use a single process or, with `fastapi run`, multiple processes (workers) for parallelism

    ```shell
    uv run --with 'fastapi[standard]' \
      fastapi dev src/my_fastapi_app.py
    ```

    ```shell
    uv run --with 'fastapi[standard]' \
      fastapi run src/my_fastapi_app.py
    ```

    ```shell
    uv run --with 'fastapi[standard]' \
      fastapi run src/my_fastapi_app.py --workers=4
    ```

3. `FastAPI` + `uvicorn`:
   - Can use a single process, or multiple processes (workers) for parallelism
   - Each process runs async, enabling high concurrency and throughput for IO-bound endpoints; for
   CPU-bound endpoints, concurrency is limited by the number of processes (workers).

    ```shell
    uv run \
      --extra=fastapi \
      --extra=uvicorn \
      uvicorn my_fastapi_app:app --app-dir src
    ```

    ```shell
    uv run \
      --extra=fastapi \
      --extra=uvicorn \
      uvicorn my_fastapi_app:app --app-dir src --workers 4
    ```

4. `FastAPI` + `gunicorn` + `uvicorn` workers:
   - Use case: production `FastAPI` setup

    ```shell
    uv run \
      --extra=fastapi \
      --extra=gunicorn \
      --extra=uvicorn \
      gunicorn --chdir src my_fastapi_app:app \
      -k uvicorn.workers.UvicornWorker \
      -w 4 \
      -b 0.0.0.0:8000
    ```

5. `Flask` + `gunicorn` (sync)

    ```shell
    uv run \
      --extra=flask \
      --extra=gunicorn \
      gunicorn --chdir src my_flask_app:app \
      -w 4 \
      -b 0.0.0.0:8000
    ```

6. Other options:
   - `FastAPI` with `gunicorn` (sync worker): not recommended, as `FastAPI` is async and should use
    an ASGI worker like `uvicorn` or `hypercorn`.
   - `Flask` with `uvicorn`: technically possible (since `Flask` is WSGI and `uvicorn` is ASGI, but
   `uvicorn` can run WSGI apps via `asgiref`), but not common or recommended for production.
   - `Flask` with `gunicorn` + `uvicorn` worker: not standard, as `Flask` is WSGI and should use
   `gunicorn`'s default sync worker.
   - To use pure WSGI (only `gunicorn` without `flask`):

     `uv run --extra=gunicorn gunicorn --chdir src my_wsgi_asgi_app:gunicorn_app`

   - To use pure ASGI (only `uvicorn` without `FastAPI`):

     `uv run --extra=uvicorn uvicorn --app-dir src my_wsgi_asgi_app:uvicorn_app`

## Testing

1. Start the server
2. In another terminal, run:

    ```shell
    curl -X GET http://127.0.0.1:8000
    curl -X GET http://127.0.0.1:8000/hello/some-name
    curl -X GET http://127.0.0.1:8000/compute
    curl -X GET http://127.0.0.1:8000/io
    curl -X GET http://127.0.0.1:8000/sync
    curl -X GET http://127.0.0.1:8000/async # only available for FastAPI; higher throughput than `sync`
    ```

3. Performance testing (latency and throughput): `wrk http://127.0.0.1:8000` (add parameters to `wrk`,
   such as `-t20 -c100`)
   - Add `--log-level critical` to `uvicorn` and `gunicorn` commands to avoid logging all test requests

## Notes

- For production, always use a WSGI server like `gunicorn` for Flask, or an ASGI server like
  `uvicorn` (or `gunicorn` with `uvicorn` workers) for FastAPI.
  - For a production server using the full WSGI stack, add `nginx`:

    Internet --> `nginx` --> `gunicorn` --> `FastAPI` (with `uvicorn` workers) or `Flask`

- The number of workers should generally be set to `(2 × CPU cores) + 1` for optimal CPU utilization
  - Throughput generally increases with the number of workers, up to the point where system resources
  (CPU, memory) are saturated; beyond that, adding more workers yields diminishing or even negative
  returns.
- Async servers (like FastAPI with `uvicorn`) excel at IO-bound workloads, while multiple workers are
  needed for CPU-bound tasks
- For Flask, concurrency is achieved by increasing the number of `gunicorn` workers, since each
  worker handles one request at a time.
- For FastAPI, async endpoints can handle many concurrent IO-bound requests per worker, but CPU-bound
  endpoints still require multiple workers for parallelism.
- Benefits of using `gunicorn`:
  - it provides advanced process management: automatic worker restarts, graceful shutdowns,
  pre-forking, and better handling of worker crashes;
  - it supports more robust logging, monitoring, and configuration options for production deployments;
  - it can manage multiple types of workers (sync, async, threaded) and is widely used and battle-tested
  in production environments;
  - if a worker dies, `gunicorn` will automatically restart it, improving reliability and uptime;
  - it can handle signals and graceful reloads, making zero-downtime deployments easier.
- Benefits of using `nginx`:
  - it can serve static files (images, CSS, JS) efficiently, offloading this work from `gunicorn`;
  - it acts as a reverse proxy, handling client connections, buffering, and load balancing before
  passing requests to `gunicorn`;
  - it can handle HTTPS (TLS termination), security headers, and request filtering;
  - it provides better protection against denial-of-service attacks;
  - it can gracefully handle client disconnects and retries, improving reliability.
