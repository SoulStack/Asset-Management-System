import socket

s = socket.socket()

print("Socket Succesfully Create")

port =1881

s.bind(("127.0.0.1",port))
print("socket binded to %s" %(port))

s.listen(5)
print("Socket is listning")


while True :
   c,addr = s.accept()
   print("Got connection from ", addr)
  
   c.send("Thank You For Connecting".encode())
   c. close()

   break
