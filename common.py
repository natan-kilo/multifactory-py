import os


def u8x_bytes_from_int(n, x):
    return n.to_bytes(x, "little")


def int_from_u8x_bytes(b, x):
    r = 0
    for i in range(x):
        r += 256**i * b[i]
    return r


def int_from_u64_bytes(b):
    r = 0
    for i in range(8):
        r += 256**i * b[i]
    return r


def u64_bytes_from_int(n):
    return n.to_bytes(8, "little")


def recv_u64(s):
    x = s.recv(8)
    return int_from_u64_bytes(x)


def send_u64(n, s):
    x = u64_bytes_from_int(n)
    s.send(x)


def recv_u8x(x, s):
    y = s.recv(x)
    return int_from_u8x_bytes(y, x)


def send_u8x(n, x, s):
    y = u8x_bytes_from_int(n, x)
    s.send(y)


def send_file(filename, s):
    # First, get the file size
    size = os.path.getsize(filename)

    # Then send it to the Server
    send_u64(size, s)

    # Then open the file and read
    file_contents = None
    with open(filename, "rb") as file:
        file_contents = file.read(size)

    # Then Send all the contents to the Server
    s.send(file_contents)


def recv_file(filename, s):
    # Get the file size
    size = recv_u64(s)

    # Then get the file contents and write them to the desired filename
    file_contents = s.recv(size)
    with open(filename, "wb") as file:
        file.write(file_contents)


def send_str(o, s):
    x = o.encode()
    send_u64(len(x), s)
    s.send(x)


def recv_str(s):
    size = recv_u64(s)
    return s.recv(size).decode()


def get_latest_save_filename():
    saves = [f for f in os.listdir() if os.path.isfile(f) and f.endswith(".sav")]
    if len(saves) == 0:
        return ""

    latest_save_time = os.path.getmtime(saves[0])
    latest_save_index = 0

    for i in range(1, len(saves), 1):
        current_save_time = os.path.getmtime(saves[i])
        if current_save_time > latest_save_time:
            latest_save_time = current_save_time
            latest_save_index = i

    return saves[latest_save_index]
