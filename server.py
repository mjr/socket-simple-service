import socket
import signal
import sys
import time
import threading


class WebServer(object):
    def __init__(self, port=8000):
        self.host = "localhost"
        self.port = port
        self.content_dir = "pages"

    def start(self):
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        try:
            print(f"Starting server on {self.host}:{self.port}")
            self.socket.bind((self.host, self.port))
            print(f"Server started on port {self.port}.")

        except Exception as e:
            print(f"Error: Could not bind to port {self.port}")
            self.shutdown()
            sys.exit(1)

        self._listen()

    def shutdown(self):
        try:
            print("Shutting down server")
            s.socket.shutdown(socket.SHUT_RDWR)

        except Exception as e:
            pass

    def _generate_headers(self, response_code):
        header = ""
        if response_code == 200:
            header += "HTTP/1.1 200 OK\n"
        elif response_code == 404:
            header += "HTTP/1.1 404 Not Found\n"

        time_now = time.strftime("%a, %d %b %Y %H:%M:%S", time.localtime())
        header += f"Date: {time_now}\n"
        header += "Server: Tiny-Python-Server\n"
        header += "Connection: close\n\n"
        return header

    def _listen(self):
        self.socket.listen(5)
        while True:
            (client, address) = self.socket.accept()
            client.settimeout(60)
            print(f"Recieved connection from {address}")
            threading.Thread(target=self._handle_client, args=(client, address)).start()

    def _handle_client(self, client, address):
        PACKET_SIZE = 1024
        while True:
            print("CLIENT", client)
            data = client.recv(PACKET_SIZE).decode()

            if not data:
                break

            request_method = data.split(" ")[0]
            print(f"Method: {request_method}")
            print(f"Request Body: {data}")

            if request_method == "GET" or request_method == "HEAD":
                file_requested = data.split(" ")[1]

                file_requested = file_requested.split("?")[0]

                if file_requested == "/":
                    file_requested = "/index.html"

                filepath_to_serve = self.content_dir + file_requested
                print(f"Serving web page [{filepath_to_serve}]")

                try:
                    f = open(filepath_to_serve, "rb")
                    if request_method == "GET":
                        response_data = f.read()
                    f.close()
                    response_header = self._generate_headers(200)

                except Exception as e:
                    print("File not found. Serving 404 page.")
                    response_header = self._generate_headers(404)

                    if request_method == "GET":
                        response_data = b"<!DOCTYPE html><html><head><title>404: This page could not be found</title></head><body><div><h1>404</h1><h2>This page could not be found.</h2></div></body></html>"

                response = response_header.encode()
                if request_method == "GET":
                    response += response_data

                client.send(response)
                client.close()
                break
            else:
                print(f"Unknown HTTP request method: {request_method}")


def shutdown_server(sig, unused):
    server.shutdown()
    sys.exit(1)


signal.signal(signal.SIGINT, shutdown_server)
server = WebServer(3002)
server.start()
print("Press Ctrl+C to shut down server.")
