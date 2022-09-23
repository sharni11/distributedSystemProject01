import os
import threading
import xmlrpc.client
from xmlrpc.server import SimpleXMLRPCServer

PORT = 8000
SERVER_IP = "localhost"

ServerPath = "./ServerFolder/"


def renameOperation(old_name, new_name):
    thread = threading.Thread(target=_handle_rename, args=(old_name, new_name,))
    thread.start()
    return True


def _handle_rename(old_name, new_name):
    newPath = os.path.join(ServerPath, new_name)
    existingPath = os.path.join(ServerPath, old_name)
    if not os.path.exists(existingPath):
        print("The file you're looking, does not exist")
    else:
        os.rename(existingPath, newPath)
        print("Filename = " + str(old_name) + " renamed as " + str(new_name) + " ")


def deleteOperation(deletefile):
    thread = threading.Thread(target=_handle_delete, args=(deletefile,))
    thread.start()
    return True


def _handle_delete(deletefile):
    if not os.path.exists(os.path.join(ServerPath, deletefile)):
        print("The file you're looking, does not exist")
    else:
        os.remove(os.path.join(ServerPath, deletefile))
        print("File = " + str(deletefile) + " deleted")


def _handle_upload(uploadfile, file_data):
    destination = os.path.join(ServerPath, uploadfile)

    with open(destination, "wb") as file:
        file.write(file_data.data)

    print("File = " + str(uploadfile) + " uploaded")


def uploadOperation(uploadfile, file_data):
    print("Upload in process")
    thread = threading.Thread(target=_handle_upload, args=(uploadfile, file_data,))
    thread.start()
    return True


def downloadOperation(downloadfile):
    thread = ThreadValues(target=_handle_download, args=(downloadfile,))
    thread.start()
    thread.join(timeout=400)
    if not thread.is_alive():
        return thread.join(timeout=400)


def _handle_download(downloadfile):
    if not os.path.exists(os.path.join(ServerPath, downloadfile)):
        print("The file you're looking, does not exist")
    else:
        print("Download in process")
        with open(os.path.join(ServerPath, downloadfile), "rb") as file:
            file_data = xmlrpc.client.Binary(file.read())
            print("File = " + str(downloadfile) + " downloaded")
            return file_data
    return True


class ThreadValues(threading.Thread):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.result = None

    def join(self, *args, **kwargs):
        super().join(*args, **kwargs)
        return self.result

    def run(self):
        if self._target is None:
            return
        try:
            self.result = self._target(*self._args, **self._kwargs)
        except Exception as exc:
            pass


def Main():
    server = SimpleXMLRPCServer((SERVER_IP, PORT))
    server.register_function(uploadOperation, 'uploadOperation')
    server.register_function(downloadOperation, 'downloadOperation')
    server.register_function(renameOperation, 'renameOperation')
    server.register_function(deleteOperation, 'deleteOperation')
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print("SERVER TERMINATED")


if __name__ == '__main__':
    Main()
