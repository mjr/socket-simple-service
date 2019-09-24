MESSAGES = {0: "Permissão negada!", 1: "Usuário autenticado!"}

users = [
    {"username": "admin", "password": "1234"},
    {"username": "admin", "password": "admin"},
    {"username": "admin", "password": "pass"},
    {"username": "root", "password": "admin"},
    {"username": "root", "password": "1234"},
]


def check(username, password):
    for user in users:
        if user["username"] == username and user["password"] == password:
            return True

    return False


def connect_server():
    import socket

    HOST = "127.0.0.1"
    PORT = 3002

    serv = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    serv.connect((HOST, PORT))

    request = "GET / HTTP/1.1\r\nHost:%s\r\n\r\n" % HOST
    serv.send(request.encode())
    response = serv.recv(4096)
    serv.close()

    return response


def client_thread(conn, ip, port, MAX_BUFFER_SIZE=4096):
    vysl = "username: ".encode("utf8")
    conn.sendall(vysl)
    username = conn.recv(MAX_BUFFER_SIZE).decode("utf8")

    vysl_p = "password: ".encode("utf8")
    conn.sendall(vysl_p)
    password = conn.recv(MAX_BUFFER_SIZE).decode("utf8")

    # print(f"{username} | {password}")
    # print(f"CHECK -> {check(username, password)}")

    message = MESSAGES[check(username, password)].encode("utf8")
    conn.sendall(message)

    if check(username, password):
        res = connect_server()

        # print(res)
        conn.sendall(res)

    conn.close()
    print(f"Connection {ip}:{port} ended")


def start_server():
    import socket

    soc = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    soc.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    print("Socket created")

    try:
        soc.bind(("127.0.0.1", 3001))
        print("Socket bind complete")
    except socket.error as msg:
        import sys

        print("Bind failed. Error : " + str(sys.exc_info()))
        sys.exit()

    soc.listen(10)
    print(f"Socket now listening on port 3001")

    from threading import Thread

    while True:
        conn, addr = soc.accept()
        ip, port = str(addr[0]), str(addr[1])
        print("Accepting connection from " + ip + ":" + port)
        try:
            Thread(target=client_thread, args=(conn, ip, port)).start()
        except:
            print("Terrible error!")
            import traceback

            traceback.print_exc()
    soc.close()


start_server()
