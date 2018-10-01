from prices import prices

def apply_BOGO(cart):
    """Buy one get one free on coffee (unlimited)
    """
    coffee_code = 'CF1'
    if coffee_code in cart:
        print('apply BOGO')
        free_coffees = cart[coffee_code] // 2
        return -(free_coffees * prices[coffee_code])
    else:
        return 0

def apply_APPL(cart):
    """Price of apples drops to 4.50 when you buy 3 or more
    """
    apples_code = 'AP1'
    if apples_code in cart and cart[apples_code] >= 3:
        print('apply APPL')
        return -cart[apples_code] * (prices[apples_code] - 4.50)
    else:
        return 0

def apply_CHMK(cart):
    """Purchase a box of chai and get milk free (Limit 1)
    """
    chai_code = 'CH1'
    milk_code = 'MK1'
    if chai_code in cart and milk_code in cart:
        print('apply CHMK')
        return -prices[milk_code]
    else:
        return 0

def apply_APOM(cart):
    """Purchase a bag of oatmeal and get 50% off a bag of apples
    """
    oatmeal_code = 'OM1'
    apples_code = 'AP1'
    if oatmeal_code in cart and apples_code in cart:
        print('apply APOM')
        apples_discounted = min(cart[oatmeal_code], cart[apples_code])
        return -(apples_discounted * prices[apples_code] * 0.5)
    else:
        return 0

specials = {
    'BOGO': apply_BOGO,
    'APPL': apply_APPL,
    'CHMK': apply_CHMK,
    'APOM': apply_APOM
}    

# cart is a frequency map of items
def apply_specials(cart):
    print('cart:', cart)
    discount = 0
    for fn in specials.values():
        discount += fn(cart)
    return discount