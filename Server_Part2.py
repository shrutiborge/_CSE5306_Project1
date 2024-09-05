import os
from xmlrpc.server import SimpleXMLRPCServer
from socketserver import ThreadingMixIn
import threading

SERVER_DIRECTORY = "server_files"

# Create the server files directory if it doesn't exist
os.makedirs(SERVER_DIRECTORY, exist_ok=True)

class FileStorageHandler:
    def list_files(self):
        print("Listing files")
        return os.listdir(SERVER_DIRECTORY)

    def upload_file(self, file_name, file_data):
        print("Uploading", file_name)
        file_path = os.path.join(SERVER_DIRECTORY, file_name)
        with open(file_path, "wb") as file:
            file.write(file_data.data)
        return True

    def download_file(self, file_name):
        print("Downloading", file_name)
        file_path = os.path.join(SERVER_DIRECTORY, file_name)
        if os.path.exists(file_path):
            with open(file_path, "rb") as file:
                return file.read()
        else:
            return None

    def delete_file(self, file_name):
        print("Deleting", file_name)
        file_path = os.path.join(SERVER_DIRECTORY, file_name)
        if os.path.exists(file_path):
            os.remove(file_path)
            return True
        return False

    def rename_file(self, old_file_name, new_file_name):
        print("Renaming", old_file_name, "to", new_file_name)
        old_file_path = os.path.join(SERVER_DIRECTORY, old_file_name)
        new_file_path = os.path.join(SERVER_DIRECTORY, new_file_name)
        if os.path.exists(old_file_path):
            os.rename(old_file_path, new_file_path)
            return True
        return False

class ThreadedFileStorageServer(ThreadingMixIn, SimpleXMLRPCServer):
    pass

def start_file_storage_server():
    server_address = ("localhost", 8000)
    xmlrpc_server = ThreadedFileStorageServer(server_address, allow_none=True, logRequests=False)
    xmlrpc_server.register_instance(FileStorageHandler())
    print("File storage server is running on port 8000...")

    try:
        xmlrpc_server.serve_forever()
    except KeyboardInterrupt:
        print("Server is shutting down...")
        xmlrpc_server.shutdown()
        xmlrpc_server.server_close()

if __name__ == "__main__":
    start_file_storage_server()
