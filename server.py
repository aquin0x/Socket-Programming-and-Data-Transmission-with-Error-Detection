import socket
import random
import string

def substitute_error(data):
    if not data:
        return data
    chars = list(data)
    idx = random.randint(0, len(chars) - 1)

    chars[idx] = random.choice(string.ascii_uppercase)
    return "".join(chars)

def start_server():
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server.bind(('127.0.0.1', 5000))
    server.listen(1)
    print("Server: Listening for Client 1...")
    
    conn1, addr1 = server.accept()
    print(f"Connected to: {addr1}")
    packet = conn1.recv(1024).decode()
    

    try:
        data, method, control = packet.split("|")
 
        corrupted_data = substitute_error(data)
        print(f"Original Data: {data} -> Corrupted Data: {corrupted_data}")
        
        """corrupted_data = data
        # print(f"Original Data: {data} -> Transmitted Data: {corrupted_data} (No Error Found.)")"""

        client2_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        client2_sock.connect(('127.0.0.1', 6000))
        new_packet = f"{corrupted_data}|{method}|{control}"
        client2_sock.send(new_packet.encode())
        client2_sock.close()
    except ValueError:
        print("Error: Invalid packet format!")
    
    conn1.close()
    server.close()

if __name__ == "__main__":
    start_server()