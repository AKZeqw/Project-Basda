import psycopg2
import os
from admin import menu_admin
from pelanggan import menu_pelanggan

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

def clear_terminal():
    os.system('cls')

def kembali():
    inputan_kembali = input('Tekan enter untuk kembali...')
    if inputan_kembali == '':
        clear_terminal()
    else:
        kembali()

def login(menu_awal):
    username = input('Masukkan Username: ')
    cur.execute("SELECT id_akun, username, password, role FROM akun WHERE username = %s", (username,))
    akun = cur.fetchone()

    if akun:
        password_input = input('Masukkan Password: ')
        if password_input == akun[2]:
            if akun[3].lower() == 'admin':
                menu_admin(username,menu_awal)
            else:
                menu_pelanggan(username,menu_awal)
        else:
            print('Password salah!')
            kembali()
            menu_awal()
    else:
        print("Username tidak ditemukan!")
        kembali()
        menu_awal()

def register(menu_awal):
    nama = input("Nama Lengkap: ")
    username = input("Username: ").lower()
    email = input("Email: ")
    if not email.endswith('@gmail.com'):
        print("Email harus menggunakan domain @gmail.com.")
        kembali()
        menu_awal()
        return
    password = input("Password: ")
    konfirmasi_password = input("Konfirmasi Password: ")
    if konfirmasi_password == password:
        no_hp = input("No HP: ")
        cur.execute("SELECT no_hp FROM pelanggan WHERE no_hp = %s", (no_hp,))
        cek_no_hp = cur.fetchone()
        if len(no_hp) > 9 and no_hp.isdigit() and cek_no_hp is None:
            cur.execute("SELECT 1 FROM akun WHERE email = %s OR username = %s", (email, username))
            if cur.fetchone():
                print("Email atau username sudah terdaftar.")
                kembali()
                menu_awal()
                return
            
            cur.execute("""
                INSERT INTO akun (username, password, role)
                VALUES (%s, %s, %s)
                RETURNING id_akun
            """, (username, password, 'pelanggan'))
            id_akun_baru = cur.fetchone()[0]

            cur.execute("""
                INSERT INTO pelanggan (id_akun, nama, email, no_hp)
                VALUES (%s, %s, %s, %s)
            """, (id_akun_baru, nama, email, no_hp))

            conn.commit()
            print("Registrasi berhasil! Akun pelanggan telah dibuat.")
        else:
            print("Nomer HP harus angka dan harus lebih dari 9 digit atau sudah terdaftar!")
            kembali()
            menu_awal()
    else:
        print("Password dan Konfirmasi Password tidak sama!")
        kembali()
        menu_awal()