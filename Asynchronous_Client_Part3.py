import xmlrpc.client
import threading
import time

class AsyncRpcClient:
    def __init__(self, server_url="http://localhost:8000"):
        self.server_proxy = xmlrpc.client.ServerProxy(server_url)

    def retrieve_results(self, request_id):
        while True:
            result = self.server_proxy.get_async_result(request_id)
            if result is not None:
                print("Received result for request_id", request_id, ":", result)
                break
            time.sleep(1)

def run_async_client():
    server_url = "http://localhost:8000"
    async_client = AsyncRpcClient(server_url)

    request_id1 = async_client.server_proxy.perform_async_operation("add", 5, 3)
    async_client.retrieve_results(request_id1)

    request_id2 = async_client.server_proxy.perform_async_operation("sort", [5, 3, 3, 1, 2, 1, 1, 2, 8, 4, 7])
    async_client.retrieve_results(request_id2)

if __name__ == "__main__":
    run_async_client()
