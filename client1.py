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
    return hex(crc & 0xFFFF).upper()[2:]

def start_client1():
    try:
        client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        client.connect(('127.0.0.1', 5000))
        
        text = input("Enter the text to send: ")
        method = "CRC16"
        control_info = calculate_crc16(text)
        
        packet = f"{text}|{method}|{control_info}"
        client.send(packet.encode())
        print(f"Packet sent: {packet}")
        client.close()
    except ConnectionRefusedError:
        print("Error: Server (server.py) is not running!")

if __name__ == "__main__":
    start_client1()