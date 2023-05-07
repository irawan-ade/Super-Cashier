from sqlalchemy import text

# buat fungsi untuk membuat table pada database
def create_table(db_conn):
    """
    Fungsi untuk membuat table baru

    args:
        db_conn : database connection

    return:
        None
    """
    # Query untuk membuat table dengan nama transactions
    query_buat_table = """
    CREATE TABLE transactions(
        ID INTEGER PRIMARY KEY AUTOINCREMENT,
        nama_item STRING,
        jumlah_item INTEGER,
        harga INTEGER,
        total_harga INTEGER,
        diskon INTEGER,
        harga_diskon INTEGER)
    """

    # Eksekusi query
    db_conn.execute(text(query_buat_table))
    
# fungsi untuk memasukkan data ke database
def insert_to_table(data_list, db_conn):
    """
    Fungsi untuk memasukkan data ke table database

    args:
        data_list (list) : nama list dari data order
    return:
        None
    """
  
    # Definisi SQL query untuk memasukkan data ke dalam table
    insert_query = text("""
    INSERT INTO 
        transactions(nama_item,
                  jumlah_item,
                  harga,
                  total_harga,
                  diskon,
                  harga_diskon)
        VALUES(:nama_item,
               :jumlah_item,
               :harga,
               :total_harga,
               :diskon,
               :harga_diskon)
    """)

    # Iterasi untuk memasukkan data per baris dari data list
    for item in data_list:
        # Eksekusi insert query untuk setiap baris data
        db_conn.execute(insert_query, item)
