import xmlrpc.client

class RpcClient:
    def __init__(self, server_url="http://localhost:8000"):
        self.server_proxy = xmlrpc.client.ServerProxy(server_url)

    def execute_operations(self):
        add_result = self.server_proxy.add_numbers(5, 3)
        sort_result = self.server_proxy.sort_list([5, 3, 3, 1, 2, 1, 1, 2, 8, 4, 7])
        print("Synchronous RPC Results:")
        print("add_numbers(5, 3) =", add_result)
        print("sort_list([5, 3, 3, 1, 2, 1, 1, 2, 8, 4, 7]) =", sort_result)

if __name__ == "__main__":
    rpc_client = RpcClient()
    rpc_client.execute_operations()
