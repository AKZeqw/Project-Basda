import datetime
import psycopg2
import os
from tabulate import tabulate

conn = psycopg2.connect(
    dbname="GaskeunDB",
    user="postgres",
    password="postgres",
    host="localhost",
    port="5432"
)

cur = conn.cursor()

def clear_terminal():
    os.system('cls')

def kembali():
    inputan_kembali = input('Tekan enter untuk kembali...')
    if inputan_kembali == '':
        clear_terminal()
    else:
        kembali()

def format_rupiah(angka):
    return f"Rp. {angka:,.0f}".replace(",", ".")

def menu_pelanggan(username,menu_awal):
    clear_terminal()
    while True:
        print(f'''
====================================
        MENU PELANGGAN
====================================
1. Lihat Daftar Kendaraan
2. Sewa Kendaraan
3. Pilih Jadwal Antar-Jemput
4. Riwayat Penyewaan
5. Lihat Status Antar-Jemput
6. Logout
====================================
''')

        pilihan = input('Pilih menu [1-5]: ')
        clear_terminal()

        if pilihan == '1':
            lihat_daftar_kendaraan()
            kembali()

        elif pilihan == '2':
            cur.execute("""
                SELECT p.id_akun
                FROM pelanggan p
                JOIN akun a ON a.id_akun = p.id_akun
                WHERE a.username = %s
                """, (username,))
            result = cur.fetchone()
            if result:
                id_pelanggan = result[0]
                sewa_kendaraan(id_pelanggan)
            else:
                print("Data pelanggan tidak ditemukan.")
                kembali()

        elif pilihan == '3':
            cur.execute("SELECT id_akun FROM akun WHERE username = %s", (username,))
            hasil = cur.fetchone()
            if not hasil:
                print("User tidak ditemukan.")
                kembali()
                return
            id_pelanggan = hasil[0]
            pilih_jadwal_antar_jemput(id_pelanggan)


        elif pilihan == '4':
            cur.execute("""
                SELECT t.id_transaksi, k.merek, k.model, t.tanggal_transaksi, t.tanggal_pengembalian, t.total_harga
                FROM transaksi t
                JOIN akun a ON t.id_pelanggan = a.id_akun
                JOIN kendaraan k ON t.id_kendaraan = k.id_kendaraan
                WHERE a.username = %s
                ORDER BY t.tanggal_transaksi DESC
            """, (username,))
            data = cur.fetchall()

            if not data:
                print("Anda belum pernah melakukan penyewaan.")
            else:
                data_format = []
                for d in data:
                    row = list(d[:5]) + [f"Rp{d[5]:,.0f}".replace(",", ".")]
                    data_format.append(row)

                headers = ["ID", "Kendaraan", "Model", "Tanggal Sewa", "Tanggal Kembali", "Harga"]
                print(tabulate(data_format, headers=headers, tablefmt="grid"))
            
            kembali()

        elif pilihan == '5':
            cur.execute("SELECT id_akun FROM akun WHERE username = %s", (username,))
            hasil = cur.fetchone()
            if hasil:
                id_pelanggan = hasil[0]
                lihat_status_antar_jemput(id_pelanggan)
            else:
                print("User tidak ditemukan.")
                kembali()


        elif pilihan == '6':
            print("Logout berhasil.")
            menu_awal()
            clear_terminal()
            break

        else:
            print("Pilihan tidak valid.")
            kembali()

def lihat_daftar_kendaraan():
    clear_terminal()
    cur.execute("""
                SELECT id_kendaraan, jenis_kendaraan, merek, model, tahun, plat, warna, cc, kapasitas_bensin, harga_per_hari, harga_per_minggu, harga_per_bulan
                FROM kendaraan
                WHERE status = 'tersedia'
                ORDER BY jenis_kendaraan, merek
            """)
    data = cur.fetchall()
    
    if not data:
        print("Belum ada kendaraan tersedia.")
    else:
        headers = ["ID", "Jenis Kendaraan", "Merek", "Model", "Tahun", "Plat", "Warna", "CC", "Kapasitas Bensin", "Harga/hari", "Harga/minggu", "Harga/bulan"]
        formatted_data = []
        for row in data:
            formatted_row = list(row)
            formatted_row[9] = format_rupiah(row[9])
            formatted_row[10] = format_rupiah(row[10])
            formatted_row[11] = format_rupiah(row[11])
            formatted_data.append(tuple(formatted_row))

        print(tabulate(formatted_data, headers=headers, tablefmt="fancy_grid"))


def sewa_kendaraan(id_pelanggan):
    clear_terminal()
    lihat_daftar_kendaraan()
    id_kendaraan = input("Masukkan ID Kendaraan yang ingin disewa: ")
    
    print("Pilih paket sewa:")
    print("1. Harian")
    print("2. Mingguan")
    print("3. Bulanan")

    try:
        pilihan_paket = int(input("Masukkan nomor paket (1/2/3): "))
    except ValueError:
        print("Input harus berupa angka!")
        kembali()
        return

    if pilihan_paket == 1:
        paket = 'harian'
        harga_query = "harga_per_hari"
    elif pilihan_paket == 2:
        paket = 'mingguan'
        harga_query = "harga_per_minggu"
    elif pilihan_paket == 3:
        paket = 'bulanan'
        harga_query = "harga_per_bulan"
    else:
        print("Pilihan tidak valid.")
        kembali()
        return

    durasi = int(input(f"Masukkan durasi sewa ({paket}): "))

    jaminan = input("Masukkan jenis jaminan (KTP/SIM): ").upper()
    if jaminan not in ['KTP', 'SIM']:
        print("Jaminan tidak valid! Hanya diperbolehkan KTP atau SIM.")
        kembali()
        return

    cur.execute(f"SELECT {harga_query} FROM kendaraan WHERE id_kendaraan = %s", (id_kendaraan,))
    harga = cur.fetchone()
    if not harga:
        print("Kendaraan tidak ditemukan.")
        kembali()
        return

    total_harga = harga[0] * durasi

    cur.execute("SELECT CURRENT_DATE")
    tanggal_sekarang = cur.fetchone()[0]

    if paket == 'harian':
        tanggal_kembali = tanggal_sekarang + datetime.timedelta(days=durasi)
    elif paket == 'mingguan':
        tanggal_kembali = tanggal_sekarang + datetime.timedelta(weeks=durasi)
    elif paket == 'bulanan':
        tanggal_kembali = tanggal_sekarang + datetime.timedelta(days=30 * durasi)

    cur.execute("""
        INSERT INTO transaksi (
            id_pelanggan, id_kendaraan, paket_sewa, tanggal_transaksi,
            tanggal_pengembalian, jaminan, durasi, total_harga
        )
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
    """, (
        id_pelanggan, id_kendaraan, paket, tanggal_sekarang,
        tanggal_kembali, jaminan, durasi, total_harga
    ))

    cur.execute("""
        UPDATE kendaraan
        SET status = 'disewa'
        WHERE id_kendaraan = %s
    """, (id_kendaraan,))

    conn.commit()

    print(f"Transaksi berhasil dibuat.")
    kembali()


def pilih_jadwal_antar_jemput(id_pelanggan):
    clear_terminal()
    cur.execute("""
        SELECT t.id_transaksi
        FROM transaksi t
        LEFT JOIN antar_jemput a ON t.id_transaksi = a.id_transaksi
        join pelanggan p ON t.id_pelanggan = p.id_akun
        WHERE p.id_akun = %s AND a.id_antar_jemput IS NULL
        ORDER BY t.id_transaksi DESC
        LIMIT 1
    """, (id_pelanggan,))
    transaksi = cur.fetchone()
    if not transaksi:
        print("Tidak ada transaksi yang tersedia untuk penjadwalan antar-jemput.")
        kembali()
        return

    id_transaksi = transaksi[0]
    alamat_jemput = input("Masukkan alamat penjemputan: ")
    alamat_antar = input("Masukkan alamat pengantaran: ")
    waktu_jemput = input("Masukkan waktu penjemputan (YYYY-MM-DD HH:MM): ")
    waktu_antar = input("Masukkan waktu pengantaran (YYYY-MM-DD HH:MM): ")

    cur.execute("""
        INSERT INTO antar_jemput (id_transaksi, waktu_antar, waktu_dijemput, alamat_jemput, alamat_antar, status)
        VALUES (%s, %s, %s, %s, %s, 'menunggu')
    """, (id_transaksi, waktu_antar, waktu_jemput, alamat_jemput, alamat_antar))
    conn.commit()

    print("Jadwal antar-jemput berhasil ditambahkan.")
    kembali()

def lihat_riwayat_penyewaan(id_pelanggan):
    clear_terminal()
    cur.execute("""
        SELECT t.id_transaksi, k.merek, k.model, t.paket_sewa, t.durasi, t.total_harga, t.tanggal_transaksi, t.tanggal_pengembalian
        FROM transaksi t
        JOIN kendaraan k ON t.id_kendaraan = k.id_kendaraan
        WHERE t.id_pelanggan = %s
        ORDER BY t.tanggal_transaksi DESC
    """, (id_pelanggan,))
    hasil = cur.fetchall()
    print(tabulate(hasil, headers=["ID", "Merek", "Model", "Paket", "Durasi", "Total Harga", "Tanggal Sewa", "Tanggal Kembali"],tablefmt="fancy_grid"))
    kembali()

def lihat_status_antar_jemput(id_pelanggan):
    clear_terminal()
    cur.execute("""
        SELECT aj.id_antar_jemput, aj.waktu_dijemput, aj.waktu_antar, aj.alamat_jemput,
               aj.alamat_antar, aj.status, t.id_transaksi
        FROM antar_jemput aj
        JOIN transaksi t ON aj.id_transaksi = t.id_transaksi
        WHERE t.id_pelanggan = %s
        ORDER BY aj.waktu_dijemput DESC
    """, (id_pelanggan,))
    data = cur.fetchall()
    if not data:
        print("Belum ada jadwal antar-jemput.")
    else:
        headers = ["ID", "Waktu Jemput", "Waktu Antar", "Alamat Jemput", "Alamat Antar", "Status", "Transaksi"]
        print(tabulate(data, headers=headers, tablefmt="fancy_grid"))
    kembali()
