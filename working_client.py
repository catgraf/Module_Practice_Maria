import socket, time, random

def recv_all(conn, size):
    data = bytearray()
    while len(data) < size:
        packet = conn.recv(size - len(data))
        if not packet:
            return None
        data.extend(packet)
    return bytes(data)


#параметры
wind_size = [1024, 1050, 2048, 2100, 3072, 4096, 5120, 6144]
testing = True
mess_size = 1460

# упаковка массива данных
pack_of_data = []
for i in range(mess_size):
    pack_of_data.append(random.randint(0, 255))

#подготовка данных для проверки
data_input = bytearray(pack_of_data)
expected_data = data_input.copy()
for j in range(len(expected_data)):
    expected_data[j] = (expected_data[j] + 1 ) % 256

#цикл для перебора и выяления влияния размера буфера recv на скорость передачи
for k in range(len(wind_size)):
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect(("127.0.0.1", 9000))
    #client_socket.connect(("192.168.1.10", 7))
    error = False
    data_lenegth = 0
    start_time = time.perf_counter()
    for i in range (0, 2):
        client_socket.sendall(data_input)
        data_lenegth += len(data_input)
        #data_lenegth += mess_size

        data = bytearray()
        while len(data) < len(data_input):
            packet = client_socket.recv(min(wind_size[k], len(data_input) - len(data)))
            if not packet:
                break;
            data.extend(packet)
        if testing:
            print(len(expected_data), len(data))
            if data != expected_data:
                error = True
                break
    end_time = time.perf_counter()
    client_socket.close()
    time_to_take = end_time - start_time
    if error:
        print("Something went wrong.")
    else:
        print(f"Recv size is {wind_size[k]}")
        print(f"Скорость в Мбайт в секунду: {data_lenegth/time_to_take/1024/1024:.4f} MB/s")
        #print(f"{data_lenegth/time_to_take/1024/1024:.4f}")