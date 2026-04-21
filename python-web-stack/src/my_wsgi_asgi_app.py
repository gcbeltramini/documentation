def gunicorn_app(environ, start_response):
    """
    Simplest possible WSGI application.

    Parameters
    ----------
    environ : dict
        A dictionary containing CGI-style environment variables.
    start_response : callable
        A callable accepting a status string and a list of (header_name, header_value) tuples.

    References
    ----------
    - https://gunicorn.org/quickstart/?h=start_response
    """
    data: bytes = b"Hello from WSGI!"
    response_headers = [
        ("Content-Type", "text/plain"),
        ("Content-Length", str(len(data))),
    ]
    start_response("200 OK", response_headers)
    return [data]


async def uvicorn_app(scope, receive, send):
    """
    Simplest possible ASGI application.

    Parameters
    ----------
    scope : dict
        A dictionary containing connection scope information.
    receive : callable
        A callable to receive events.
    send : callable
        A callable to send events.

    References
    ----------
    - https://uvicorn.dev/#quickstart
    - https://uvicorn.dev/concepts/lifespan/#usage
    """
    if scope["type"] == "lifespan":
        while True:
            message = await receive()
            if message["type"] == "lifespan.startup":
                print("Application is starting up...")
                await send({"type": "lifespan.startup.complete"})
            elif message["type"] == "lifespan.shutdown":
                print("Application is shutting down...")
                await send({"type": "lifespan.shutdown.complete"})
                return
            else:
                raise RuntimeError(f"Unsupported ASGI lifespan message type: {message['type']}")
    elif scope["type"] == "http":
        content: bytes = b"Hello from ASGI!"
        await send(
            {
                "type": "http.response.start",
                "status": 200,
                "headers": [
                    (b"Content-Type", b"text/plain"),
                    (b"Content-Length", str(len(content)).encode("utf-8")),
                ],
            }
        )
        await send(
            {
                "type": "http.response.body",
                "body": content,
            }
        )
    else:
        # Example: "websocket"
        raise RuntimeError(f"Unsupported ASGI scope type: {scope['type']}")
