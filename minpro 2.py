import random
import pwinput
from prettytable import PrettyTable

pengguna = {
    "Admin": {"pw": "AdminDatang", "role": "admin"},
    "Budi": {"pw": "BudiSuki", "role": "user"},
    "Siti": {"pw": "SitiSuka", "role": "user"},
    "Dewi": {"pw": "dewdededew", "role": "user"},
    "Asep": {"pw": "AsepGantengNiBozz", "role": "user"}
}

nama_use = ["Budi", "Siti", "Dewi", "Asep"]
acar = ["Wedding", "Rapat", "Diklat", "Seminar"]
nomi = [500000, 1000000, 2500000]

kalender = {
    i: {"status": "Kosong", "nama": "-", "acara": "-", "nominal": 0} 
    for i in range(1, 31)
}

for tgl in random.sample(range(1, 31), 8):
    kalender[tgl] = {
        "status": "Terisi",
        "nama": random.choice(nama_use),
        "acara": random.choice(acar),
        "nominal": random.choice(nomi)
    }

def login():
    print("=== LOGIN ===")
    for percobaan in range(3):
        u = input("Username: ").strip()
        p = pwinput.pwinput("Password: ", mask="*").strip()
        
        if u in pengguna and pengguna[u]["pw"] == p:
            print(f"\nSukses: Selamat datang, {u} ({pengguna[u]['role'].upper()})!")
            input("Tekan Enter untuk melanjutkan...")
            return u
        
        sisa = 2 - percobaan
        if sisa > 0:
            print(f"Salah: Username/Password keliru! Sisa percobaan: {sisa}\n")
            
    print("\nGagal login 3 kali. Kembali ke menu utama.")
    return None

def get_tgl(tangg="Masukkan Tanggal (1-30): "):
    while True:
        tgl_in = input(tangg).strip()
        if tgl_in.isdigit():
            tgl = int(tgl_in)
            if 1 <= tgl <= 30:
                return tgl
            else:
                print("Error: tanggal harus berada di rentang 1-30")
        else:
            print("Error: input harus berupa angka")

def tamp_kal(user):
    t = PrettyTable(["Tgl", "Status", "Nama Penyewa", "Acara", "Pembayaran"])
    t.title = f"KALENDER RESERVASI GEDUNG ({user.upper()})"
    
    role = pengguna[user]["role"]
    
    for tgl, d in kalender.items():
        if d["status"] == "Terisi":
            if role == "admin":
                nama_tampil = d["nama"]
            elif d["nama"].lower() == user.lower():
                nama_tampil = d["nama"]
            else:
                nama_tampil = "*** (YTTA)"
            
            if d["nominal"] >= 2500000:
                bayar = "LUNAS"
            else:
                nom_fmt = f"{d['nominal']:,}".replace(",", ".")
                bayar = f"DP ({nom_fmt})"
            t.add_row([tgl, d["status"], nama_tampil, d["acara"], bayar])
        else:
            t.add_row([tgl, d["status"], "-", "-", "-"])
            
    print(t)

def booking(user):
    print("\n--- BOOKING GEDUNG ---")
    tgl = get_tgl()
    if kalender[tgl]["status"] == "Terisi":
        print(f"Gagal: tanggal {tgl} sudah terisi")
        return

    if pengguna[user]["role"] == "admin":
        while True:
            nama = input("Masukkan Nama Penyewa: ").strip()
            if nama:
                break
            print("Harus ada nama penyewa")
    else:
        nama = user

    acara = input("Jenis Acara: ").strip()
    if not acara:
        acara = "Acara Umum"

    while True:
        dp = input("Nominal DP/Lunas (Min 500.000): ").replace(".", "").strip()
        if dp.isdigit():
            nom = int(dp)
            if nom > 2500000:
                kembalian = nom - 2500000
                nom = 2500000
                kembalian_fmt = f"{kembalian:,}".replace(",", ".")
                print(f"Pembayaran melebihi batas lunas (2.500.000). Kembalian Anda: {kembalian_fmt}")
                break
            elif nom >= 500000:
                break
            else:
                print("Gagal: minimal pembayaran DP adalah 500.000")
        else:
            print("Gagal: nominal harus berupa angka")

    kalender[tgl] = {"status": "Terisi", "nama": nama, "acara": acara, "nominal": nom}
    print(f"Sukses: Booking berhasil disimpan untuk Tanggal {tgl} atas nama {nama}")

def ganti_tgl(user):
    print("\n--- GANTI TANGGAL ---")
    tgl_awl = get_tgl("Masukkan Tanggal Awal (1-30): ")
    d1 = kalender[tgl_awl]

    if d1["status"] == "Kosong":
        print("Gagal: tanggal asal masih kosong")
        return

    if pengguna[user]["role"] != "admin" and d1["nama"].lower() != user.lower():
        print("Akses Ditolak: bukan reservasi milik anda")
        return

    tgl_baru = get_tgl("Masukkan Tanggal Tujuan (1-30): ")
    if kalender[tgl_baru]["status"] == "Terisi":
        print("Gagal: tanggal tujuan sudah terisi")
        return

    # Pindahkan Data
    kalender[tgl_baru] = d1.copy()
    kalender[tgl_awl] = {"status": "Kosong", "nama": "-", "acara": "-", "nominal": 0}
    print(f"Sukses: berhasil memindahkan reservasi dari tanggal {tgl_awl} ke tanggal {tgl_baru}")

def batalkan(user):
    print("\n--- BATAL RESERVASI ---")
    tgl = get_tgl()
    d = kalender[tgl]

    if d["status"] == "Kosong":
        print("Gagal: tanggal tersebut masih kosong")
        return

    if pengguna[user]["role"] != "admin" and d["nama"].lower() != user.lower():
        print("Akses Ditolak: bukan reservasi milik Anda")
        return

    kalender[tgl] = {"status": "Kosong", "nama": "-", "acara": "-", "nominal": 0}
    print(f"Sukses: reservasi tanggal {tgl} berhasil dibatalkan")

def rekap_admin():
    terisi = sum(1 for d in kalender.values() if d["status"] == "Terisi")
    total = sum(d["nominal"] for d in kalender.values())
    
    t = PrettyTable(["Parameter", "Jumlah"])
    t.title = "REKAP GEDUNG"
    t.add_row(["Total Terisi", f"{terisi} Hari"])
    t.add_row(["Total Kosong", f"{30 - terisi} Hari"])
    
    total_fmt = f"{total:,}".replace(",", ".")
    t.add_row(["Total Pendapatan", f"{total_fmt}"])
    print(t)

def main():
    while True:
        print("\n=== SISTEM RESERVASI GEDUNG SERBAGUNA ===")
        print("1. Login\n2. Keluar")
        p = input("Pilih (1-2): ").strip()
        if p == "2":
            print("Terima kasih telah menggunakan sistem reservasi!")
            break
        elif p == "1":
            user = login()
            if not user:
                continue
            
            role = pengguna[user]["role"]
            while True:
                print("\n")
                
                tamp_kal(user)
                print(f"\n--- MENU ({role.upper()}: {user}) ---")
                print("1. Booking Gedung")
                print("2. Ganti Tanggal")
                print("3. Batalkan Reservasi")
                if role == "admin":
                    print("4. Rekap Keuangan")
                    print("5. Logout")
                else:
                    print("4. Logout")

                m = input("\nPilih menu: ").strip()
                if m == "1":
                    booking(user)
                    input("\nTekan Enter untuk kembali ke menu...")
                elif m == "2":
                    ganti_tgl(user)
                    input("\nTekan Enter untuk kembali ke menu...")
                elif m == "3":
                    batalkan(user)
                    input("\nTekan Enter untuk kembali ke menu...")
                elif m == "4" and role == "admin":
                    rekap_admin()
                    input("\nTekan Enter untuk kembali ke menu...")
                elif (m == "4" and role == "user") or (m == "5" and role == "admin"):
                    print("Logout berhasil...")
                    break
                else:
                    print("Pilihan menu tidak valid!")
        else:
            print("Pilihan tidak valid!\n Masukkan angka 1 atau 2.")

if __name__ == "__main__":
    main()