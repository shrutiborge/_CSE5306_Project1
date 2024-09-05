import xmlrpc.server

class ArithmeticServer:
    def add_numbers(self, num1, num2):
        return num1 + num2

    def sort_list(self, number_list):
        return sorted(number_list)

class RpcServer:
    def __init__(self, host="localhost", port=8000):
        self.xmlrpc_server = xmlrpc.server.SimpleXMLRPCServer((host, port))
        self.xmlrpc_server.register_instance(ArithmeticServer())

    def start_server(self):
        print("Synchronous RPC Server is running on port 8000...")
        self.xmlrpc_server.serve_forever()

if __name__ == "__main__":
    rpc_server = RpcServer()
    rpc_server.start_server()
