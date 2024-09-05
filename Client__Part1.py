import os
import xmlrpc.client

SERVER_URL = "http://localhost:8000"
CLIENT_STORAGE_FOLDER = "client_files"

# Create the client files folder if it doesn't exist
os.makedirs(CLIENT_STORAGE_FOLDER, exist_ok=True)

xmlrpc_client = xmlrpc.client.ServerProxy(SERVER_URL)

def list_files_on_server():
    files = xmlrpc_client.list_all_files()
    print("Files on server:")
    for file in files:
        print(f" - {file}")

def upload_file_to_server():
    file_path = input("Enter the path of the file to upload: ")
    if os.path.exists(file_path):
        with open(file_path, "rb") as file:
            file_data = xmlrpc.client.Binary(file.read())
        xmlrpc_client.upload_file(os.path.basename(file_path), file_data)
        print(f"{file_path} uploaded successfully.")
    else:
        print(f"{file_path} not found.")

def download_file_from_server():
    file_name = input("Enter the name of the file to download: ")
    file_data = xmlrpc_client.download_file(file_name)
    if file_data:
        with open(os.path.join(CLIENT_STORAGE_FOLDER, file_name), "wb") as file:
            file.write(file_data.data)
        print(f"{file_name} downloaded successfully.")
    else:
        print(f"{file_name} not found on the server.")

def delete_file_on_server():
    file_name = input("Enter the name of the file to delete: ")
    if xmlrpc_client.delete_file(file_name):
        print(f"{file_name} deleted successfully.")
    else:
        print(f"{file_name} not found on the server.")

def rename_file_on_server():
    old_file_name = input("Enter the current name of the file: ")
    new_file_name = input("Enter the new name of the file: ")
    if xmlrpc_client.rename_file(old_file_name, new_file_name):
        print(f"{old_file_name} renamed to {new_file_name} successfully.")
    else:
        print(f"{old_file_name} not found on the server.")

def display_menu():
    while True:
        print("\nEnter your choice: ")
        print("1. List Files")
        print("2. Upload File")
        print("3. Download File")
        print("4. Delete File")
        print("5. Rename File")
        print("6. Quit")

        user_choice = input("Enter your choice: ")

        if user_choice == "1":
            list_files_on_server()
        elif user_choice == "2":
            upload_file_to_server()
        elif user_choice == "3":
            download_file_from_server()
        elif user_choice == "4":
            delete_file_on_server()
        elif user_choice == "5":
            rename_file_on_server()
        elif user_choice == "6":
            break
        else:
            print("Invalid choice. Please try again.")

if __name__ == "__main__":
    display_menu()
