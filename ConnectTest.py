import socket

a_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
location = ("182.23.82.22", 1880)
result_of_check = a_socket.connect_ex(location)

if result_of_check == 0:
   print("Port is open")
else:
   print("Port is not open")