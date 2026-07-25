import socket

class Network:
    def __init__(self):
        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server = "127.0.0.1"
        self.port = 5555
        self.addr = (self.server, self.port)
        self.color = self.connect()

    def connect(self):
        try:
            self.client.connect(self.addr)
            return self.client.recv(2048).decode()
        except Exception as e:
            print("Failed to connect:", e)
            return None

    def send(self, data):
        try:
            self.client.sendall(str.encode(data))
        except socket.error as e:
            print("Send error:", e)
            
    def receive(self):
        try:
            # Non-blocking receive so it doesn't freeze the Pygame loop
            self.client.settimeout(0.01)
            data = self.client.recv(2048)
            if not data:
                return None
            return data.decode("utf-8")
        except:
            return None
