import socket
import paramiko
import threading

# RSA anahtarı oluştur (sunucu için)
host_key = paramiko.RSAKey.generate(2048)

def handle_client(client_socket):
    try:
        transport = paramiko.Transport(client_socket)
        transport.add_server_key(host_key)
        
        # Sunucu simülasyonu oluştur
        class CustomServer(paramiko.ServerInterface):
            def check_auth_password(self, username, password):
                # Sadece "admin" ve "password" ile kimlik doğrulama sağlar
                if username == "admin" and password == "password":
                    return paramiko.AUTH_SUCCESSFUL
                return paramiko.AUTH_FAILED

        server = CustomServer()
        transport.start_server(server=server)
        
        channel = transport.accept()
        if channel is not None:
            channel.send("SSH bağlantısı başarılı!\n")
            while True:
                command = channel.recv(1024).decode("utf-8").strip()
                if command.lower() == "exit":
                    channel.send("Bağlantı kapatılıyor...\n")
                    break
                else:
                    response = f"Komut alındı: {command}\n"
                    channel.send(response)
            channel.close()
    except Exception as e:
        print(f"Bir hata oluştu: {e}")
    finally:
        client_socket.close()

def start_real_ssh_server():
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server_socket.bind(("192.168.1.11", 4444))
    server_socket.listen(5)
    print("SSH sunucusu başlatıldı. Bağlantılar bekleniyor...")

    while True:
        client, addr = server_socket.accept()
        print(f"[+]Yeni bağlantı: {addr}")
        client_handler = threading.Thread(target=handle_client, args=(client,))
        client_handler.start()

# SSH sunucusunu başlat
start_real_ssh_server()
