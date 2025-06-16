from tabulate import tabulate
import datetime
import psycopg2
import time
import art
import os

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

def menu_admin(username,menu_awal):
    while True:
        clear_terminal()
        print(f"=== Selamat datang, Admin {username} ===\n")
        
        cur.execute("SELECT COUNT(*) FROM kendaraan WHERE jenis_kendaraan = 'Mobil'")
        total_mobil = cur.fetchone()[0]
        
        cur.execute("SELECT COUNT(*) FROM kendaraan WHERE jenis_kendaraan = 'Motor'")
        total_motor = cur.fetchone()[0]
        
        cur.execute("SELECT COUNT(*) FROM kendaraan WHERE status = 'disewa'")
        disewa = cur.fetchone()[0]
        
        cur.execute("SELECT COUNT(*) FROM kendaraan WHERE status = 'tersedia'")
        tersedia = cur.fetchone()[0]
        
        cur.execute("SELECT COUNT(*) FROM pelanggan")
        total_pelanggan = cur.fetchone()[0]
        
        cur.execute("""
            SELECT COUNT(*) FROM antar_jemput 
            WHERE DATE(waktu_antar) = CURRENT_DATE
        """)
        permintaan_antar_jemput = cur.fetchone()[0]
        
        cur.execute('SELECT SUM(total_harga) FROM transaksi')
        total_income = cur.fetchone()[0]
        
        print(f"Total Mobil              : {total_mobil}")
        print(f"Total Motor              : {total_motor}")
        print(f"Total Pelanggan          : {total_pelanggan}")
        print(f"Kendaraan Tersedia       : {tersedia}")
        print(f"Kendaraan Disewa         : {disewa}")
        print(f"Antar-Jemput Hari Ini    : {permintaan_antar_jemput}")
        print(f'Total Income             : {format_rupiah(total_income)}')
        
        print("\n=== Menu Admin ===")
        print("1. Manajemen Kendaraan")
        print("2. Manajemen Driver")
        print("3. Manajemen Pengguna")
        print("4. Pengelolaan Jadwal Antar-Jemput")
        print("5. Riwayat & Laporan")
        print("6. Logout")
        
        pilihan = input("Pilih menu [1-6]: ")
        if pilihan == '1':
            clear_terminal()
            manajemen_kendaraan()
        elif pilihan == '2':
            clear_terminal()
            manajemen_driver()
        elif pilihan == '3':
            clear_terminal()
            manajemen_pelanggan()
        elif pilihan == '4':
            clear_terminal()
            menu_antar_jemput()
        elif pilihan == '5':
            clear_terminal()
            menu_riwayat_laporan()
        elif pilihan == '6':
            clear_terminal()
            menu_awal()
        else:
            print("Pilihan tidak valid!")

def manajemen_kendaraan():
    while True:
        clear_terminal()
        print('''
===============================
    MENU MANAJEMEN KENDARAAN
===============================
1. Lihat Daftar Kendaraan
2. Tambah Kendaraan
3. Edit Kendaraan
4. Hapus Kendaraan
5. Kembali
===============================
        ''')
        pilihan = input("Pilih menu [1-5]: ")
        if pilihan == '1':
            lihat_daftar_kendaraan()
        elif pilihan == '2':
            tambah_kendaraan()
        elif pilihan == '3':
            edit_kendaraan()
        elif pilihan == '4':
            hapus_kendaraan()
        elif pilihan == '5':
            break
        else:
            print("Pilihan tidak tersedia")
            time.sleep(1.25)

def daftar_kendaraan():
    cur.execute("SELECT id_kendaraan, plat, jenis_kendaraan, merek, model, tahun, warna, cc, kapasitas_bensin, harga_per_hari, harga_per_minggu, harga_per_bulan, status FROM kendaraan")
    kendaraan = cur.fetchall()
    kendaraan_terformat = []
    
    for row in kendaraan:
        row = list(row)
        for i in range(9, 12):
            if row[i] is not None:
                row[i] = str(int(row[i]))
        kendaraan_terformat.append(row)
    
    headers = ["ID", "Plat", "Jenis", "Merk", "Model", "Tahun", "Warna", "CC", "Kapasitas Bensin", "Harga/Hari", "Harga/Minggu", "Harga/Bulan", "Status"]
    print(tabulate(kendaraan_terformat, headers=headers, tablefmt="fancy_grid"))


def lihat_daftar_kendaraan():
    clear_terminal()
    print("=== DAFTAR KENDARAAN ===")
    daftar_kendaraan()
    kembali()

def tambah_kendaraan():
    while True:
        clear_terminal()
        daftar_kendaraan()
        print("=== TAMBAH KENDARAAN ===")
        pilihan = input("1. Mobil\n2. Motor\n3. Kembali\nPilih menu: ")
        if pilihan == '1' or pilihan == '2':
            try:
                if pilihan == '1':
                    jenis_kendaraan = 'Mobil'
                else:
                    jenis_kendaraan = 'Motor'
                plat = input("Plat Nomor       : ")
                merek = input("Merek            : ")
                model = input("Model            : ")
                tahun = input("Tahun (YYYY)     : ")
                warna = input("Warna            : ")
                cc = input("CC               : ")
                kapasitas_bensin = input("Kapasitas bensin : ")
                harga_hari = input("Harga/hari       : ")
                harga_minggu = input("Harga/minggu     : ")
                harga_bulan = input("Harga/bulan      : ")
                
                cur.execute("""
                    INSERT INTO kendaraan (jenis_kendaraan, merek, model, tahun, plat, warna, cc, kapasitas_bensin, harga_per_hari, harga_per_minggu, harga_per_bulan, status)
                    VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
                """, (jenis_kendaraan, merek, model, tahun, plat, warna, cc, kapasitas_bensin, harga_hari, harga_minggu, harga_bulan, 'tersedia'))
                conn.commit()
                print("Kendaraan berhasil ditambahkan.")
            except Exception as e:
                conn.rollback()
                print("Gagal menambahkan kendaraan:", e)
            kembali()
        elif pilihan == '3':
            return
        else:
            print("Pilihan tidak valid!")
            time.sleep(1.25)

def edit_kendaraan():
    while True:
        try:
            clear_terminal()
            daftar_kendaraan()
            print("=== EDIT KENDARAAN ===")
            id_kendaraan = input("Masukkan ID Kendaraan yang ingin diedit: ")
            cur.execute("SELECT * FROM kendaraan WHERE id_kendaraan = %s", (id_kendaraan,))
            data = cur.fetchone()

            if not data:
                print("Kendaraan tidak ditemukan")
                kembali()
                return

            print("Tekan Enter jika tidak ingin mengubah field")
            plat = input(f"Plat ({data[5]}): ") or data[5]
            merek = input(f"Merek ({data[2]}): ") or data[2]
            model = input(f"Model ({data[3]}): ") or data[3]
            tahun = input(f"Tahun ({data[4]}): ") or data[4]
            warna = input(f"Warna ({data[6]}): ") or data[6]
            cc = input(f"CC ({data[7]}): ") or data[7]
            kapasitas_bensin = input(f"Kapasitas bensin ({data[8]}): ") or data[8]
            harga_hari = input(f"Harga/hari ({data[9]}): ") or data[9]
            harga_minggu = input(f"Harga/minggu ({data[10]}): ") or data[10]
            harga_bulan = input(f"Harga/bulan ({data[11]}): ") or data[11]
            status = input(f"Status ({data[12]}): ") or data[12]

            try:
                cur.execute("""
                    UPDATE kendaraan
                    SET merek = %s, model = %s, tahun = %s, plat = %s, warna = %s, cc = %s, kapasitas_bensin = %s, harga_per_hari = %s, harga_per_minggu = %s, harga_per_bulan = %s, status = %s
                    WHERE id_kendaraan = %s
                """, (merek, model, tahun, plat, warna, cc, kapasitas_bensin, harga_hari, harga_minggu, harga_bulan, status, id_kendaraan))
                conn.commit()
                print("Data kendaraan berhasil diperbarui")
                time.sleep(1.25)
            except Exception as e:
                conn.rollback()
                print("Gagal mengedit data kendaraan:", e)
                time.sleep(1.25)
            return
        except:
            print("Itu bukan ID Kendaraan")
            time.sleep(1.25)
            break

def hapus_kendaraan():
    try:
        clear_terminal()
        daftar_kendaraan()
        print("=== HAPUS KENDARAAN ===")
        id_kendaraan = int(input("Masukkan ID Kendaraan yang akan dihapus: "))

        try:
            cur.execute("DELETE FROM kendaraan WHERE id_kendaraan = %s", (id_kendaraan,))
            if cur.rowcount > 0:
                conn.commit()
                print("Kendaraan berhasil dihapus.")
            else:
                print("Kendaraan tidak ditemukan atau tidak dapat dihapus.")
        except Exception as e:
            conn.rollback()
            print("Gagal menghapus kendaraan:", e)
        kembali()
    except:
        print("Itu bukan ID Kendaraan")
        time.sleep(1.25)
        return

def manajemen_driver():
    while True:
        clear_terminal()
        print('''
===============================
    MENU MANAJEMEN DRIVER
===============================
1. Lihat Daftar Driver
2. Tambah Driver
3. Edit Driver
4. Hapus Driver
5. Kembali
===============================
        ''')
        pilihan = input("Pilih menu [1-5]: ")
        clear_terminal()

        if pilihan == '1':
            lihat_daftar_driver()
        elif pilihan == '2':
            tambah_driver()
        elif pilihan == '3':
            edit_driver()
        elif pilihan == '4':
            hapus_driver()
        elif pilihan == '5':
            return
        else:
            print("Pilihan tidak tersedia")
            time.sleep(1.25)
            continue

def daftar_driver():
    cur.execute("SELECT * FROM driver")
    data = cur.fetchall()
    if not data:
        print("Belum ada driver yang terdaftar")
    else:
        headers = ["ID", "Nama", "No HP", "Status"]
        print(tabulate(data, headers=headers, tablefmt="fancy_grid"))

def lihat_daftar_driver():
    clear_terminal()
    print("=== DAFTAR DRIVER ===")
    daftar_driver()
    kembali()

def tambah_driver():
    while True:
        daftar_driver()
        print("=== TAMBAH DRIVER ===")
        try:
            nama = input("Nama driver: ")
            no_hp = input("No HP: ")
            cur.execute("INSERT INTO driver (nama, no_hp, status) VALUES (%s, %s, %s)", (nama, no_hp, 'aktif'))
            conn.commit()
            print("Driver berhasil ditambahkan")
            time.sleep(1.25)
        except Exception as e:
            conn.rollback()
            print("Gagal menambahkan driver:", e)
            time.sleep(1.25)
        return

def edit_driver():
    while True:
        try:
            clear_terminal()
            daftar_driver()
            print("=== EDIT DRIVER ===")
            id_driver = input("Masukkan ID Driver yang ingin diedit: ")
            cur.execute("SELECT * FROM driver WHERE id_driver = %s", (id_driver,))
            data = cur.fetchone()

            if not data:
                print("Driver tidak ditemukan")
                continue

            print("Tekan Enter jika tidak ingin mengubah field")
            nama = input(f"Nama ({data[1]}): ") or data[1]
            no_hp = input(f"No HP ({data[2]}): ") or data[2]
            status = input(f"Status ({data[3]}): ") or data[3]
            try:
                cur.execute("""
                    UPDATE driver
                    SET nama = %s, no_hp = %s, status = %s
                    WHERE id_driver = %s
                """, (nama, no_hp, status, id_driver))
                conn.commit()
                print("Data driver berhasil diperbarui")
            except Exception as e:
                conn.rollback()
                print("Gagal mengedit data driver:", e)
            kembali()
            return
        except Exception:
            conn.rollback()
            print("Itu bukan ID Driver")
            time.sleep(1.25)
            continue

def hapus_driver():
    try:
        clear_terminal()
        daftar_driver()
        print("=== HAPUS DRIVER ===")
        id_driver = int(input("Masukkan ID Driver yang akan dihapus: "))

        try:
            cur.execute("DELETE FROM driver WHERE id_driver = %s", (id_driver,))
            if cur.rowcount > 0:
                conn.commit()
                print("Driver berhasil dihapus")
            else:
                print("Driver tidak ditemukan atau tidak dapat dihapus")
        except Exception as e:
            conn.rollback()
            print("Gagal menghapus driver:", e)
        kembali()
    except:
        conn.rollback()
        print("Itu bukan ID Driver")
        time.sleep(1.25)
        kembali()

def manajemen_pelanggan():
    while True:
        print('''
===============================
    MANAJEMEN PELANGGAN
===============================
1. Lihat Daftar Pelanggan
2. Hapus Akun Pelanggan
3. Kembali
===============================
        ''')
        pilihan = input("Pilih menu [1-3]: ")
        clear_terminal()

        if pilihan == '1':
            print("=== DAFTAR PELANGGAN ===")
            daftar_pelanggan()
            kembali()

        elif pilihan == '2':
            daftar_pelanggan()
            print("=== HAPUS PELANGGAN ===")
            id_pelanggan = input("Masukkan ID Akun Pelanggan yang ingin dihapus: ")
            cur.execute("SELECT nama FROM pelanggan WHERE id_akun = %s", (id_pelanggan,))
            data = cur.fetchone()
            if data:
                konfirmasi = input(f"Yakin ingin menghapus akun '{data[0]}'? [y/n]: ").lower()
                if konfirmasi == 'y':
                    cur.execute("DELETE FROM akun WHERE id_akun = %s", (id_pelanggan,))
                    conn.commit()
                    print("Akun pelanggan berhasil dihapus")
            else:
                print("Akun tidak ditemukan")
            kembali()

        elif pilihan == '3':
            return
        else:
            print("Pilihan tidak valid.")
            kembali()

def daftar_pelanggan():
    cur.execute("""SELECT a.id_akun, a.username, p.nama, p.email, p.no_hp
                FROM akun a
                JOIN pelanggan p ON p.id_akun = a.id_akun
                WHERE role = 'pelanggan';
    """)
    data = cur.fetchall()
    if not data:
        print("Belum ada pelanggan yang terdaftar")
    else:
        headers = ["ID", "Username", "Nama", "Email", "No HP"]
        print(tabulate(data, headers=headers, tablefmt="fancy_grid"))

def menu_antar_jemput():
    while True:
        print('''
=======================================
        PENGELOLAAN ANTAR-JEMPUT
=======================================
1. Lihat Permintaan Antar-Jemput
2. Update Status Antar-Jemput
3. Kembali
=======================================
        ''')
        pilihan = input("Pilih menu [1-3]: ")
        clear_terminal()

        if pilihan == '1':
            daftar_antar_jemput()
            kembali()

        elif pilihan == '2':
            daftar_antar_jemput()
            id_antar = input("Masukkan ID Antar-Jemput: ")
            cur.execute("SELECT id_antar_jemput, status FROM antar_jemput WHERE id_antar_jemput = %s", (id_antar,))
            hasil = cur.fetchone()
            if hasil:
                print(f"Status saat ini: {hasil[1]}")
                status_baru = input("Masukkan status baru [proses/selesai]: ").lower()
                if status_baru in ['proses', 'selesai']:
                    cur.execute("""
                        UPDATE antar_jemput SET status = %s WHERE id_antar_jemput = %s
                    """, (status_baru, id_antar))
                    conn.commit()
                    print("Status berhasil diperbarui")
                else:
                    print("Status tidak valid")
            else:
                print("ID Antar-Jemput tidak ditemukan")
            kembali()

        elif pilihan == '3':
            return
        else:
            print("Pilihan tidak valid")
            continue

def daftar_antar_jemput():
    cur.execute("""
                SELECT aj.id_antar_jemput, aj.id_transaksi, p.nama, aj.waktu_antar, aj.waktu_dijemput, aj.alamat_antar, aj.alamat_jemput, aj.status
                FROM antar_jemput aj
                JOIN transaksi t ON aj.id_transaksi = t.id_transaksi
                JOIN pelanggan p ON t.id_pelanggan = p.id_akun
                ORDER BY aj.id_antar_jemput
            """)
    data = cur.fetchall()
    if not data:
        print("Belum ada permintaan antar-jemput")
    else:
        print("=== DAFTAR PERMINTAAN ANTAR-JEMPUT ===")
        headers = ["ID Antar-Jemput", "ID Transaksi", "Nama", "Waktu Antar", "Waktu Jemput", 'Alamat Antar', 'Alamat Jemput', 'Status']
        print(tabulate(data, headers=headers, tablefmt="fancy_grid"))

def menu_riwayat_laporan():
    while True:
        print('''
====================================
        RIWAYAT & LAPORAN
====================================
1. Lihat Semua Riwayat Transaksi
2. Laporan Pendapatan
3. Kembali
====================================
        ''')
        pilihan = input('Pilih menu [1-3]: ')
        clear_terminal()

        if pilihan == '1':
            cur.execute("""
                SELECT t.id_transaksi, pe.nama, k.model, t.tanggal_transaksi, t.tanggal_pengembalian, t.durasi, t.paket_sewa, t.jaminan, t.metode_pembayaran, t.total_harga
                FROM transaksi t
                JOIN pelanggan pe ON t.id_pelanggan = pe.id_akun
                JOIN kendaraan k ON t.id_kendaraan = k.id_kendaraan
                ORDER BY t.tanggal_transaksi DESC
            """)
            data = cur.fetchall()
            data_terformat = []
            for row in data:
                row = list(row)
                for i in range(9, 10):
                    if row[i] is not None:
                        row[i] = str(int(row[i]))
                data_terformat.append(row)
            if not data:
                print("Belum ada transaksi")
            else:
                headers = ["ID", "Nama", "Kendaraan", "Tanggal Sewa", "Tanggal Pengembalian", "Durasi", "Paket Sewa", 'Jaminan', 'Metode Pembayaran', "Total Harga"]
                print(tabulate(data_terformat, headers=headers, tablefmt="fancy_grid"))
            kembali()
        elif pilihan == '2':
            laporan_pendapatan()
        elif pilihan == '3':
            return

        else:
            print("Pilihan tidak valid")
            continue

def laporan_pendapatan():
    clear_terminal()
    print("=== LAPORAN PENDAPATAN ===\n")
    print("1. Berdasarkan Hari")
    print("2. Berdasarkan Bulan")
    print("3. Berdasarkan Tahun")
    print("4. Total Keseluruhan")
    pilihan = input("Pilih jenis laporan [1-4]: ")
    
    try:
        if pilihan == '1':
            tanggal = input("Masukkan tanggal (YYYY-MM-DD): ")
            cur.execute("SELECT SUM(total_harga) FROM transaksi WHERE tanggal_transaksi = %s", (tanggal,))
            total = cur.fetchone()[0]

            if total is None:
                print("Tidak ada transaksi pada tanggal tersebut.")
                kembali()
                clear_terminal()
                return
            
            data = [["Tanggal", tanggal], ["Pendapatan", format_rupiah(total)]]

        elif pilihan == '2':
            bulan = input("Masukkan bulan (MM): ")
            tahun = input("Masukkan tahun (YYYY): ")
            cur.execute("""
                SELECT SUM(total_harga) FROM transaksi 
                WHERE EXTRACT(MONTH FROM tanggal_transaksi) = %s 
                    AND EXTRACT(YEAR FROM tanggal_transaksi) = %s
            """, (bulan, tahun))
            total = cur.fetchone()[0]

            if total is None:
                print("Tidak ada transaksi pada bulan dan tahun tersebut.")
                kembali()
                clear_terminal()
                return
            data = [["Bulan", bulan], ["Tahun", tahun], ["Pendapatan", format_rupiah(total)]]

        elif pilihan == '3':
            tahun = input("Masukkan tahun (YYYY): ")
            cur.execute("SELECT SUM(total_harga) FROM transaksi WHERE EXTRACT(YEAR FROM tanggal_transaksi) = %s", (tahun,))
            total = cur.fetchone()[0]

            if total is None:
                print("Tidak ada transaksi pada tahun tersebut.")
                kembali()
                clear_terminal()
                return
            data = [["Tahun", tahun], ["Pendapatan", format_rupiah(total)]]

        elif pilihan == '4':
            cur.execute("SELECT SUM(total_harga) FROM transaksi")
            total = cur.fetchone()[0]

            if total is None:
                print("Belum ada transaksi.")
                kembali()
                clear_terminal()
                return
            data = [["Periode", "Keseluruhan"], ["Pendapatan", format_rupiah(total)]]

        else:
            print("Pilihan tidak valid")
            kembali()
            clear_terminal()

        print("\n=== HASIL LAPORAN ===")
        print(tabulate(data, tablefmt="fancy_grid"))

    except Exception as e:
        print(f"Gagal mengambil laporan pendapatan: {e}")

    kembali()