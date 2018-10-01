#!/usr/bin/env python3

import sys
from signal import signal, SIGINT
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
    return subtotal - discount

def parse_cart(items):
    if isinstance(items, str):
        if ',' in items:
            items = items.split(',')
        else:
            items = items.split(' ')


    items = [i.strip().replace(',', '') for i in items]

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

def sigint_handler(signal, handler):
    print()
    sys.exit(0)

if __name__ == '__main__':
    signal(SIGINT, sigint_handler)

    while True:    
        cart_string = input('Basket: ')
        cart = parse_cart(cart_string)
        total = checkout(cart)
        print(f'Total: ${total}')