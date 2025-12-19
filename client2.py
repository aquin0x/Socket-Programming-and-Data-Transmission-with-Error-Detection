import socket

def calculate_crc16(data):
    crc = 0xFFFF
    for char in data:
        crc ^= ord(char)
        for _ in range(8):
            if crc & 1:
                crc = (crc >> 1) ^ 0xA001
            else:
                crc >>= 1
    # Sonucu hex formatında (örn: 87AF) döndürür
    return hex(crc & 0xFFFF).upper()[2:]

def start_client2():
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    
    try:
        server.bind(('127.0.0.1', 6000))
        server.listen(1)
        print("Client 2: Listening for incoming data...")
        
        conn, addr = server.accept()
        print(f"Connected to: {addr}")
        
        packet = conn.recv(1024).decode()
        
        if "|" in packet:
            parts = packet.split("|")
            if len(parts) == 3:
                data, method, incoming_control = parts
                
                computed_control = calculate_crc16(data)
                
                status = "Data Correct." if computed_control == incoming_control else "Data Corrupted."
                
                print("\n" + "="*30)
                print(f"Received Data: {data}") 
                print(f"Method: {method}") 
                print(f"Sent Check Bits: {incoming_control}") 
                print(f"Computed Check Bits: {computed_control}") 
                print(f"Status: {status}") 
                print("="*30)
            else:
                print("Error: Invalid packet format.")
        
        conn.close()
    except Exception as e:
        print(f"An error occurred: {e}")
    finally:
        server.close()

if __name__ == "__main__":
    start_client2()