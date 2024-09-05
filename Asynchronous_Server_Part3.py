import xmlrpc.server
import threading
import queue
import time

class AsyncArithmeticServer:
    def __init__(self):
        self.results_queue = queue.Queue()
        self.current_request_id = 0

    def perform_async_operation(self, operation, *args):
        time.sleep(10)
        if operation == "add":
            result = sum(args)
        elif operation == "sort":
            result = sorted(args[0])
        else:
            raise ValueError("Invalid operation")

        request_id = self.generate_request_id()
        self.results_queue.put((request_id, result))
        return request_id

    def get_async_result(self, request_id):
        try:
            while True:
                queued_request_id, result = self.results_queue.get_nowait()
                if queued_request_id == request_id:
                    return result
        except queue.Empty:
            return None

    def generate_request_id(self):
        self.current_request_id += 1
        return self.current_request_id

def run_async_server():
    server_address = ("localhost", 8000)
    xmlrpc_server = xmlrpc.server.SimpleXMLRPCServer(server_address, logRequests=False)
    arithmetic_server = AsyncArithmeticServer()
    xmlrpc_server.register_instance(arithmetic_server)
    print("Async RPC Server is running on port 8000...")

    server_thread = threading.Thread(target=xmlrpc_server.serve_forever)
    server_thread.daemon = True
    server_thread.start()

    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        print("Server is shutting down...")
        xmlrpc_server.shutdown()
        xmlrpc_server.server_close()

if __name__ == "__main__":
    run_async_server()
