"""Module providingFunction printing python version."""
import os

mode = os.getenv("MODE", "grpc")

if mode == "http":
    import http_server
    http_server.run()
else:
    import grpc_server
    grpc_server.run()
