import os
from xmlrpc.server import SimpleXMLRPCServer
from socketserver import ThreadingMixIn

FILE_STORAGE_FOLDER = "server_files"

# Create the server files folder if it doesn't exist
os.makedirs(FILE_STORAGE_FOLDER, exist_ok=True)

class FileStorageServer:
    def list_all_files(self):
        return os.listdir(FILE_STORAGE_FOLDER)

    def upload_file(self, file_name, file_data):
        file_path = os.path.join(FILE_STORAGE_FOLDER, file_name)
        with open(file_path, "wb") as file:
            file.write(file_data.data)
        return True

    def download_file(self, file_name):
        file_path = os.path.join(FILE_STORAGE_FOLDER, file_name)
        if os.path.exists(file_path):
            with open(file_path, "rb") as file:
                return file.read()
        else:
            return None

    def delete_file(self, file_name):
        file_path = os.path.join(FILE_STORAGE_FOLDER, file_name)
        if os.path.exists(file_path):
            os.remove(file_path)
            return True
        return False

    def rename_file(self, old_file_name, new_file_name):
        old_file_path = os.path.join(FILE_STORAGE_FOLDER, old_file_name)
        new_file_path = os.path.join(FILE_STORAGE_FOLDER, new_file_name)
        if os.path.exists(old_file_path):
            os.rename(old_file_path, new_file_path)
            return True
        return False

class MultiThreadedXMLRPCServer(ThreadingMixIn, SimpleXMLRPCServer):
    pass

def start_server():
    server_address = ("localhost", 8000)
    xmlrpc_server = MultiThreadedXMLRPCServer(server_address, allow_none=True)
    xmlrpc_server.register_instance(FileStorageServer())
    print("File storage server is running on port 8000...")
    xmlrpc_server.serve_forever()

if __name__ == "__main__":
    start_server()
