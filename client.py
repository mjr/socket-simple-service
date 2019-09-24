import socket

soc = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
soc.connect(("127.0.0.1", 3001))


while True:
    result_bytes = soc.recv(4096)
    result_string = result_bytes.decode("utf8")

    clients_input = input(f"{result_string}\n")
    soc.send(clients_input.encode("utf8"))

    if not result_string:
        break
