order = []

def add_item(name, qty, price_per_qty):
    '''
    Make list of items including quantity 
        and the price per quantity
    add_item(name, qty, price_per_qty)    
    Input parameters:
        name <string>
        qty <int>
        price_per_qty <int>
    '''
    order.append([name, qty, price_per_qty])

add_item('buku', 2, 10000)
add_item('pensil', 5, 2000)
print(order)