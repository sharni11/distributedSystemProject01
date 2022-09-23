import xmlrpc.client
import sys
import os


ClientPath = "./ClientFolder/"


def Main():
    rpccall = xmlrpc.client.ServerProxy("http://localhost:8000/", allow_none=True)

    choice = input("Press numbers to perform operation:\n 1. UPLOAD \n 2.DOWNLOAD\n 3.RENAME \n 4. DELETE\n KEY = ")

    if choice == "1":
        uploadfile = input("Enter the file you want to upload = ")
        if not os.path.exists(os.path.join(ClientPath, uploadfile)):
            print("The file you're looking for does not exist")
            sys.exit(1)
        else:
            print("Uploading File to the Server")

        with open(os.path.join(ClientPath, uploadfile), "rb") as file:
            file_data = xmlrpc.client.Binary(file.read())
            rpccall.uploadOperation(uploadfile, file_data)
            print("Updation is done")

    elif choice == "2":
        downloadfile = input("Enter the file you want to download = ")
        print("Downloading is in Process")
        with open(os.path.join(ClientPath, downloadfile), "wb") as file:
            file.write(rpccall.downloadOperation(downloadfile).data)

    elif choice == "3":
        print("Enter Existing and new name for the file you want to rename : ")
        old_name = input("Existing File Name = ")
        new_name = input("New Name = ")
        print("Renaming the file is in process")
        rpccall.renameOperation(old_name, new_name)
        print("Renaming is done ")

    elif choice == "4":
        deletefile = input("Enter the file you want to delete : ")
        print("Deleting Operation in process")
        rpccall.deleteOperation(deletefile)
        print("Deleting is done")

    else:
        print("Option Not Found")


if __name__ == '__main__':
    Main()
