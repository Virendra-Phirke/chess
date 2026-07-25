import socket
from _thread import *

server = "127.0.0.1"
port = 5555

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

try:
    s.bind((server, port))
except socket.error as e:
    print(str(e))

s.listen(2)
print("Waiting for a connection, Server Started")

clients = []

def threaded_client(conn, player_id):
    # Send the player their color (0 is w, 1 is b)
    color = "w" if player_id == 0 else "b"
    conn.send(str.encode(color))
    
    while True:
        try:
            data = conn.recv(2048)
            
            if not data:
                print(f"Player {color} disconnected")
                break
            else:
                reply = data.decode("utf-8")
                # print(f"Received from {color}:", reply)
                
                # Send the data to the OTHER client
                other_client_id = 1 if player_id == 0 else 0
                if other_client_id < len(clients):
                    clients[other_client_id].sendall(data)
                
        except Exception as e:
            break

    print("Lost connection")
    if conn in clients:
        clients.remove(conn)
    conn.close()

currentPlayer = 0
while True:
    conn, addr = s.accept()
    print("Connected to:", addr)
    clients.append(conn)
    
    start_new_thread(threaded_client, (conn, currentPlayer))
    currentPlayer += 1
