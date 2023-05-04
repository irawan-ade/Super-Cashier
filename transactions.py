import re

def is_in_cart(item_name, order_list):
    '''
    cek apakah barang sudah ada dalam lis pembelian

    Parameters:
        item_name (str)  : nama barang
        order_list (list) : lis pembelian
    Returns:
        True/False (Bool): ada/tidak ada di lis
        idx        (int) : ada di lis pada urutan ke idx+1
    '''    
    for idx, item in enumerate(order_list):
        if re.match("^"+item_name.lower()+"$", item[0].lower()):
            return True, idx
            break
    return False, -1 # -1 is just a dummy number
    
class Transaction:    
    def __init__(self):
        self.order = []
   
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
            # extract name, quantity, and price per qty in the list
            name          = item[0]
            qty           = item[1]
            price_per_qty = item[2]

            if is_in_cart(name, self.order)[0]:
                print(name, 'sudah ada dalam lis urutan ke', 
                      is_in_cart(name, self.order)[1]+1,
                      '! Silahkan update jumlah atau harganya.')
            else:
                self.order.append([name, qty, 
                                   price_per_qty, qty*price_per_qty])
                print(qty, name, 'berhasil ditambahkan ke keranjang.')
 
tran1 = Transaction()
tran1.add_item(['buku', 10, 20000], ['pensil', 30, 10000])
print(tran1.order)