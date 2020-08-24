import socket
import common
import os
from threading import Thread

server_passwd = None
is_hosted = False
host_name = "-"
blocked_ips = []
tries = {}


def generate_server_password(length):
    import random

    password = bytearray(length)
    for i in range(length):
        password[i] = random.randint(33, 126)

    return password.decode("ascii")


def get_password():
    if not os.path.exists("server"):
        print("--- First Time Setup ---")
        password = generate_server_password(32)
        print(f"\nServer Password: {password}\n")
        print("------------------------")
        with open("server", "w") as file:
            file.write(password)
        return password

    with open("server", "r") as file:
        return file.read()


def process_connection(client, client_addr):
    global server_passwd, is_hosted, host_name, blocked_ips, tries

    client_passwd = common.recv_str(client)

    # If the client's ip is blocked, ignore the connection
    if client_addr[0] in blocked_ips:
        client.close()
        return

    # If the password is incorrect, respond with code 2 and
    #  close the connection
    if client_passwd != server_passwd:
        common.send_u8x(2, 1, client)
        if client_addr[0] not in tries:
            tries[client_addr[0]] = 1
        else:
            if tries[client_addr[0]] == 3:
                blocked_ips.append(client_addr[0])
            else:
                tries[client_addr[0]] += 1
        client.close()
        return

    # If someone is hosting, respond with code 1, tell them who
    #  is hosting, close the connection and move on to the next
    if is_hosted:
        common.send_u8x(1, 1, client)
        common.send_str(host_name, client)
        client.close()
        return

    # - If nobody is hosting and there is a save, respond with
    #    code 0 and send them the latest world save
    # - If there is no save, respond with code 3
    # - In both cases, receive their name and wait until
    #    they are done playing
    latest = common.get_latest_save_filename()
    if not latest.endswith(".sav"):
        common.send_u8x(3, 1, client)
    else:
        common.send_u8x(0, 1, client)
        common.send_file(latest, client)

    is_hosted = True
    host_name = common.recv_str(client)

    # Now, we just wait for the host to finish playing and save
    #  their latest save

    # Firstly, we determine the file name for the next save (to
    #  have the pattern: "save_[save_num]_[save_host].sav")
    next_save_filename = ""
    if latest == "":
        next_save_filename = f"save_0_{host_name}.sav"
    else:
        _, last_save_num, _ = latest[0:-4].split("_")
        next_save_filename = f"save_{int(last_save_num)+1}_{host_name}.sav"

    common.recv_file(next_save_filename, client)

    # After the client has stopped playing and uploaded the file,
    #  the next client to connect will become the host
    is_hosted = False
    host_name = "-"
    client.close()
    return


if __name__ == '__main__':
    # Some vars
    server_passwd = get_password()

    # Create a TCP socket
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    ip = ("localhost", 10000)

    # Bind the Socket and handle incoming connections
    s.bind(ip)
    s.listen(5)

    while True:
        client_sock, client_address = s.accept()
        p = Thread(target=process_connection, args=(client_sock, client_address,))
        p.start()
