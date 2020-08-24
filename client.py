import socket
import common
import os
import pickle


def get_config():
    if not os.path.exists("config"):
        raw_ip = input("Server IP: ")
        if len(raw_ip.split(":")) != 2:
            print("Please enter a valid IP!")
            quit()
        (ip, port) = raw_ip.split(":")
        passwd = input("Server Password: ")
        name = input("Your Name: ")

        with open("config", "wb") as file:
            pickle.dump([(ip, int(port)), passwd, name], file)

        return (ip, int(port)), passwd, name

    with open("config", "rb") as file:
        x = pickle.load(file)
        return x[0], x[1], x[2]


if __name__ == '__main__':
    # Get the config
    server_ip, server_passwd, name = get_config()

    # Create a TCP socket
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    # Connect to the Server
    s.connect(server_ip)

    # Send the server the saved password
    common.send_str(server_passwd, s)

    # Wait for the Server Response
    server_response = common.recv_u8x(1, s)
    if server_response == 2:
        print("Invalid Password!")
        quit()

    if server_response == 1:
        host_name = common.recv_str(s)
        print(f"Server is being hosted by {host_name}.")
        quit()

    if server_response == 0:
        print("Downloading latest save...")
        common.recv_file("latest.sav", s)

    common.send_str(name, s)
    print("You are now hosting the Server.")

    print("When you are done playing or want to stop hosting, \n"
          "type 'exit' to upload the latest save to the server")
    while True:
        command = input("> ")
        if command == "exit":
            break

    # Send the latest save to the server
    latest = common.get_latest_save_filename()
    common.send_file(latest, s)


