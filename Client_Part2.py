import os
import time
import threading
import xmlrpc.client
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

CLIENT_DIRECTORY = "client_files"
SERVER_URL = "http://localhost:8000/"

# Create the client files directory if it doesn't exist
os.makedirs(CLIENT_DIRECTORY, exist_ok=True)

xmlrpc_client = xmlrpc.client.ServerProxy(SERVER_URL, allow_none=True)

class ClientFileEventHandler(FileSystemEventHandler):
    def on_any_event(self, event):
        if event.is_directory:
            return
        file_name = os.path.basename(event.src_path)
        if event.event_type == "created":
            print(f"{file_name} was created. Synchronizing...")
        elif event.event_type == "modified":
            print(f"{file_name} was modified. Synchronizing...")
        elif event.event_type == "deleted":
            print(f"{file_name} was deleted. Synchronizing...")
        synchronize_file_with_server(file_name)

def synchronize_with_server():
    observer = Observer()
    event_handler = ClientFileEventHandler()
    observer.schedule(event_handler, CLIENT_DIRECTORY, recursive=False)
    observer.start()

    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()
    observer.join()

def synchronize_file_with_server(file_name):
    file_path = os.path.join(CLIENT_DIRECTORY, file_name)
    if os.path.exists(file_path):
        with open(file_path, "rb") as file:
            file_data = xmlrpc.client.Binary(file.read())
            xmlrpc_client.upload_file(file_name, file_data)
            print(f"{file_name} synchronized with the server.")
    else:
        xmlrpc_client.delete_file(file_name)
        print(f"{file_name} deleted from the server (synchronized).")

def start_client():
    sync_thread = threading.Thread(target=synchronize_with_server)
    sync_thread.start()

    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        sync_thread.join()

if __name__ == "__main__":
    start_client()
