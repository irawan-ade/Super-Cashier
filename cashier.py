import sqlalchemy
from sqlalchemy import create_engine
from dbTools import *
from transaction import Transaction

## ----------------- Database ---------------##
# Konfigurasi database
# buat sqlite sebagai engine
ENGINE = create_engine('sqlite:///db/data.db')
# Koneksi ke database
CONN = ENGINE.connect() 

check = sqlalchemy.inspect(ENGINE)
is_tbl_exist = check.has_table("transactions") 

if not is_tbl_exist:
    # memanggil fungsi create table
    create_table(CONN)    
# --------------------------------------------

trnsct_123 = Transaction()
# trnsct_123.add_item(['buku', 10, 20000], ['pensil', 30, 10000])
# trnsct_123.add_item(['penghapus', 5, 5000])
# trnsct_123.add_item(['BuKu', 5, 5000])
# trnsct_123.add_item(['buku gambar', 20, 100000])

# trnsct_123.update_item_name('buku gambar', 'Drawing book')
# trnsct_123.update_item_price('Drawing book', 120000)
# trnsct_123.update_item_qty('Drawing book', 5)

# trnsct_123.reset_transaction()
# trnsct_123.add_item(['buku', 10, 20000], ['pensil', 30, 10000])
# trnsct_123.add_item(['penghapus', 5, 5000])
# trnsct_123.add_item(['BuKu', 5, 5000])
# trnsct_123.add_item(['buku gambar', 20, 100000])

# trnsct_123.update_item_name('buku gambar', 'Drawing book')
# trnsct_123.update_item_price('Drawing book', 120000)
# trnsct_123.update_item_qty('Drawing book', 5)

# trnsct_123.check_order()
# trnsct_123.delete_item('penghapus')

# trnsct_123.check_out()

## Test 1
trnsct_123.add_item(['Ayam Goreng', 2, 20000], ['Pasta Gigi', 3, 15000])

## Test 2
trnsct_123.delete_item('Pasta Gigi')

## Test 3
trnsct_123.reset_transaction()

## Test 4
trnsct_123.add_item(['Ayam Goreng', 2, 20000], 
                    ['Pasta Gigi', 3, 15000],
                    ['Mainan Mobil', 1, 200000],
                    ['Mi Instan', 5, 3000])

trnsct_123.check_out()