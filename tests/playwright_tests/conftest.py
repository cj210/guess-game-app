import os
import socket
import pytest
import subprocess
import time
from playwright.sync_api import sync_playwright


def find_free_port():
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
        sock.bind(("",0))
        port = sock.getsockname()[1]
    return port


@pytest.fixture(scope="session")
def api_url():
    env_vars = os.environ.copy()
    base = env_vars.get("test_base", "127.0.0.1").rstrip("/:")
    port = find_free_port()

    server_process = Popen(
            ["uvicorn", "src.guess_number.app:forest", "--host", base, "--port", str(port),],
            stdout = subprocess.PIPE,
            stderr = subprocess.PIPE,
            env=env_vars,
            )

    current_time = time.time()
    time_out = 5
    
    while time.time() - current_time < time_out:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
            if sock.connect_ex((base,port)) == 0:
                break
            time.sleep(0.05)
    else:
        server_process.terminate()
        server_process.wait()
        raise RuntimeError(f"Application couldn't start on port: {port}")

    url = f"http://{base}:{port}"

    yield url

    server_process.terminate()
    server_process.wait()


@pytest.fixture(scope="function")
def api_client(api_url):
    with sync_playwright() as playwright:
        context = playwright.request.new_context(base_url=api_url)
        yield context
        context.dispose()
    


