import socket               # Import socket module


class Client:
    def __init__(self):
                # Create a socket object
        self.host = socket.gethostname() # Get local machine name
        self.port = 12345                # Reserve a port for your service.

    def connection_to_server(self):
        self.s = socket.socket()
        self.s.connect(('localhost', self.port))

    def send_message_to_client(self, alpha, beta):
        message = str(alpha) + ':' + str(beta)
        self.s.sendto(message.encode(), ('localhost', self.port))

    def close_connection(self):
        self.s.close()                # Close the connection