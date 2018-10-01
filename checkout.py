import sys
from prices import prices
from specials import apply_specials

# cart is a frequency map of items
def calculate_subtotal(cart):
    subtotal = 0
    for item, amt in cart.items():
        subtotal += prices[item] * amt
    return subtotal

# cart is a frequency map of items
def checkout(cart):
    subtotal = calculate_subtotal(cart)
    discount = apply_specials(cart)
    return subtotal + discount

def gather_cart(items):
    items = [i.replace(',', '') for i in items]
    catalog = prices.keys()
    cart = {}
 
    # count the items
    for item in items:
        if item not in catalog:
            raise ValueError(f'Unrecognized item {item}. Aborting...')
        
        if cart.get(item, None):
            cart[item] += 1
        else:
            cart[item] = 1

    return cart

if __name__ == '__main__':
    cart = gather_cart(sys.argv[1:])
    total = checkout(cart)
    print(total)