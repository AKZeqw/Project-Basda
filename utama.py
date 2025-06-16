import psycopg2
import os
from auth import login,register

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

def menu_awal():
    clear_terminal()
    print(r'''
============================================================
 __  __                                                  _ 
|  \/  |                         /\                     | |
| \  / |  ___  _ __   _   _     /  \   __      __  __ _ | |
| |\/| | / _ \| '_ \ | | | |   / /\ \  \ \ /\ / / / _` || |
| |  | ||  __/| | | || |_| |  / ____ \  \ V  V / | (_| || |
|_|  |_| \___||_| |_| \__,_| /_/    \_\  \_/\_/   \__,_||_|
============================================================
1. Register
2. Login
3. Keluar
============================================================
''')
    inputan = input('Silahkan pilih menu [1-3]: ')
    if inputan == '1':
        clear_terminal()
        register(menu_awal)
    elif inputan == '2':
        clear_terminal()
        login(menu_awal)
    elif inputan == '3':
        clear_terminal()
    else:
        print('Pilihan menu tidak ditemukan!')
        kembali()
        menu_awal()

menu_awal()