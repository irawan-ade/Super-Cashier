from tabulate import tabulate
import copy
from sqlalchemy import create_engine, text
from dbTools import insert_to_table

def is_in_cart(item_name, cart):
    '''
    cek apakah barang sudah ada dalam lis pembelian
    
    Parameters:
        item_name (str)  : nama barang
        cart (dict) : lis pembelian
    Returns:
        True/False (Bool): ada/tidak ada di lis
    '''    
    
    for key, val in cart.items():
        if item_name.lower() == key.lower():
            return True, key
            break
    return False, -1 # -1 is just a dummy

def promo(harga):
    '''
    hitung besarnya potongan dari diskon
    serta harga total setelah diskon
    
    Parameters:
        harga (int) : harga awal sebelum diskon
    Returns:
        besar_potongan (int): besarnya potongan karena diskon
        harga_setelah_diskon (int): harga setelah diskon
    '''     
    diskon = 0
    if harga > 500000:
        diskon = 0.07
    elif harga > 300000:    
        diskon = 0.06
    elif harga > 200000:
        diskon = 0.05
        
    besar_potongan = int(harga * diskon)
    harga_setelah_diskon = int(harga - besar_potongan)
    
    return besar_potongan, harga_setelah_diskon

def show_table(cart, 
               headers=["No","Nama Item", "Jumlah Item", 
                        "Harga/item", "Total Harga",
                        "Besar Potongan", "Harga Setelah Diskon"],
               table_format = "outline"):
    '''
    menampilkan tabel lis pembelian
    
    Parameters:
        cart (dict)         : lis pembelian
        header (list)       : lis nama kolom
        table_format (str)  : tabulate table format
                              https://pypi.org/project/tabulate/
    Returns:
        -
    '''
    # ubah data dictionary ke bentuk list
    order_list = []
    for key, val in cart.items():
        temp = [key]
        for item in val:
            temp.append(item)
        order_list.append(temp)
    
    # untuk menambahkan nomor pada kolom nomor
    number_id = range(1, len(order_list)+1)
    print(tabulate(order_list, headers=headers, tablefmt=table_format, 
                   showindex=number_id)) 

class Transaction: 
    def __init__(self):
        self.order = {}
        self.final_order = {}
   
    def add_item(self, *item_list):
        '''
        menambah barang pembelanjaan

        Parameters:
            item_list (list) : lis dari lis item yang berisikan: 
                                nama, jumlah item, harga per item
        Returns:
            -
        '''
        for item in item_list:
            if len(item) != 3:
                print('Masukkan secara terurut dalam format list: \
                      [nama barang, jumlah, harga per item]')
                break
            else:
                # extract name, quantity, and price per qty in the list
                name          = item[0]
                qty           = item[1]
                price_per_qty = item[2]

                available, item_name = is_in_cart(name, self.order)

                if available:
                    print('Barang dengan nama', 
                          item_name, 'sudah ada dalam keranjang! \
                          \nSilahkan update jumlah atau harganya.')
                    notif = False
                else:
                    self.order[name] = [qty, price_per_qty]
                    # print(qty, name, 
                    #       'berhasil ditambahkan ke keranjang.')
                    notif = True
        if notif:            
            print('Item yang dibeli adalah:', self.order)

    def check_order(self):
        '''
        lihat semua pembelian

        Parameters:
            -
        Returns:
            -
        '''
        # check kesalahan input data
        valid_entry = True
        for key, val in self.order.items():
            if not isinstance(key, str) or \
               not isinstance(val[0], int) or \
               not isinstance(val[1], int):
               valid_entry = False
               break

        show_table(self.order)

        if valid_entry:    
            print('Pemesanan sudah benar')
        else:
            print("Terdapat kesalahan dalam input data")
            
    def check_out(self):
        '''
        Hitung dan cetak total belanja setelah diskon

        Parameters:
            -
        Returns:
            final_order (dict): list belanja yang dilengkapi
                                    besar potongan dan
                                    harga setelah diskon
        '''     
        final_order = copy.deepcopy(self.order)
        total_harga_sebelum_diskon = 0
        total_harga_setelah_diskon = 0
        total_potongan = 0

        for key, val in final_order.items():
            # tambahkan kolom total harga
            total_harga = final_order[key][0] * final_order[key][1]
            final_order[key].append(total_harga)

            # tambahkan kolom potongan dan harga setelah diskon
            besar_potongan, harga_setelah_diskon = promo(total_harga)
            final_order[key].append(besar_potongan)
            final_order[key].append(harga_setelah_diskon)        

            # hitung total
            total_harga_sebelum_diskon += total_harga 
            total_potongan += besar_potongan
            total_harga_setelah_diskon += harga_setelah_diskon

        # Cetak tabel berisikan info potongan dan harga setelah diskon
        show_table(final_order)

        # Cetak notifikasi
        print('Total belanja Anda sebelum potongan:', 
              total_harga_sebelum_diskon, 'rupiah')
        print('Anda telah berhemat', total_potongan, 'rupiah')
        print('Item yang dibeli adalah',self.order)
        print('Total belanja yang harus dibayarkan adalah Rp.', 
              total_harga_setelah_diskon)

        data_list = [{'nama_item': key, 
                      'jumlah_item': value[0], 
                      'harga': value[1], 
                      'total_harga': value[2],
                      'diskon': value[3],
                      'harga_diskon': value[4]} 
                     for key, value in final_order.items()]
        
        # run database
        ENGINE = create_engine('sqlite:///db/data.db')
        # Koneksi ke database
        CONN = ENGINE.connect() 
        # masukkan data transaksi ke database
        insert_to_table(data_list, CONN)   
        
        # Check the database
        # result = CONN.execute(text("SELECT * FROM transactions"))
        # for res in result:
        #     print(res.ID,
        #           res.nama_item,
        #           res.jumlah_item, 
        #           res.harga, 
        #           res.diskon, 
        #           res.harga_diskon)        
    
    def delete_item(self, item_name):
        '''
        hapus suatu barang tertentu dari lis pembelian

        Parameters:
            item_name (str) : nama barang
        Returns:
            -
        '''      
        available, item_name_in_cart = is_in_cart(item_name, self.order)
        if available:
            del self.order[item_name_in_cart]
            # print(item_name_in_cart, 'berhasil dihapus dari keranjang.')
            print(self.order)
        else:
            print('Barang tidak ada di keranjang. Periksa lagi !')

    def reset_transaction(self):
        '''
        hapus semua transaksi

        Parameters:
            -
        Returns:
            -
        '''      
        self.order = {}
        print('Semua item berhasil di delete !')         
            
    def update_item_name(self, item_name, new_name):
        '''
        update nama barang

        Parameters:
            item_name (str) : nama lama dari barang
            new_name (str)  : nama baru dari barang
        Returns:
            -
        '''          
        available, item_name_in_cart = is_in_cart(item_name, self.order)
        if available:
            self.order[new_name] = self.order[item_name_in_cart]
            del self.order[item_name_in_cart]
            print('Nama barang berhasil diperbaharui.')
        else:
            print('Barang tidak ada di keranjang. \
                   Periksa lagi !')           
       
    def update_item_price(self, item_name, new_price):
        '''
        update harga barang

        Parameters:
            item_name (str) : nama barang
            new_price (int) : harga barang  
        Returns:
            -
        '''      
        available, item_name_in_cart = is_in_cart(item_name, self.order)
        if available:
            # update harga barang
            self.order[item_name_in_cart][1] = new_price     
            print('Harga', item_name_in_cart, 
                  'berhasil diperbaharui menjadi', 
                   new_price, 'per item')
        else:
            print('Barang tidak ada di keranjang. Periksa lagi !')
            
    def update_item_qty(self, item_name, new_qty):
        '''
        update jumlah barang

        Parameters:
            item_name (str) : nama barang
            new_qty (int)   : jumlah barang  
        Returns:
            -
        '''          
        available, item_name_in_cart = is_in_cart(item_name, self.order)
        if available:
            # update jumlah barang
            self.order[item_name_in_cart][0] = new_qty
            print('Jumlah', item_name_in_cart, 
                  'berhasil diperbaharui menjadi', new_qty)
        else:
            print('Barang tidak ada di keranjang. Periksa lagi !')                
# Test  
if __name__ == '__main__':
    
    from dbTools import *
    
    tran1 = Transaction()
    tran1.add_item(['buku', 10, 20000], ['pensil', 30, 10000])
    tran1.add_item(['penghapus', 5, 5000])
    tran1.add_item(['BuKu', 5, 5000])
    tran1.add_item(['buku gambar', 20, 100000])
    
    tran1.update_item_name('buku gambar', 'Drawing book')
    tran1.update_item_price('Drawing book', 120000)
    tran1.update_item_qty('Drawing book', 5)
    
    # tran1.reset_transaction()
    
    tran1.check_order()
    tran1.delete_item('penghapus')
        
    tran1.check_out()