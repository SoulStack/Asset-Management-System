import socket

host_ip, server_port = "192.168.0.250", 27011

tcp_client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

try:
    # Establish connection to TCP server and exchange data
    tcp_client.connect((host_ip, server_port))

    # Read data from the TCP server and close the connection
    received = tcp_client.recv(8192)
finally:
	print("Bytes Received: {}".format(received.decode()))
	tcp_client.close()
