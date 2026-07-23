import socket

def recv_all(conn, mes_size, recv_size):
    data = bytearray()
    while len(data) < mes_size:
        packet = conn.recv(min(recv_size,mes_size - len(data)))
        if not packet:
            return None
        data.extend(packet)
    return bytes(data)

message_size = 1460
recv_param_size = message_size
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.bind(("127.0.0.1", 9000))
server_socket.listen(1)
while True:
    conn, addr = server_socket.accept()
    while True:
        data = recv_all(conn, message_size, recv_param_size)
        if data is None:
            break
        output_data = bytearray(data)
        for i in range (len(output_data)):
            output_data[i] = (output_data[i] + 1) % 256
        conn.sendall(bytes(output_data))
    conn.close()