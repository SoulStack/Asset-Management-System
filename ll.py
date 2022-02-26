import socket

host_ip, server_port = "192.168.0.250", 27011
data = " Hello how are you?\n"

tcp_client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

try:
    # Establish connection to TCP server and exchange data
    tcp_client.connect((host_ip, server_port))
    tcp_client.sendall(data.encode())

    # Read data from the TCP server and close the connection
    received = tcp_client.recv(1024)
finally:
    tcp_client.close()
print ("Bytes Sent:     {}".format(data))
print ("Bytes Received: {}".format(received.decode()))
