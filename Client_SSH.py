import paramiko

def fake_ssh_client():
    # Kullanıcıdan bilgiler alınır
    host = input("Bağlanılacak IP: ")
    port = int(input("Bağlanılacak Port: "))
    username = input("Kullanıcı Adı: ")
    password = input("Şifre: ")

    try:
        # SSH istemcisi oluştur ve bağlan
        client = paramiko.SSHClient()
        client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        
        # Bağlantıyı kuruyoruz
        print("Bağlantı kuruluyor...")
        client.connect(hostname=host, port=port, username=username, password=password)
        
        # Bağlantı başarılı
        print("[+]Bağlantı Kuruldu!")

    except paramiko.AuthenticationException:
        print("Kimlik doğrulama başarısız. Kullanıcı adı veya şifre hatalı.")
    except Exception as e:
        print(f"Bir hata oluştu: {e}")
    finally:
        client.close()

# Fake SSH istemcisini başlat
fake_ssh_client()
