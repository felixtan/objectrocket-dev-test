from prices import prices

specials_rules = {
    'APOM': lambda cart, specials_applied: 1 if 'OM1' in cart and 'AP1' in cart else 0,
    'CHMK': lambda cart, specials_applied: 1 if 'CH1' in cart and 'MK1' in cart else 0,
    'BOGO': lambda cart, specials_applied: cart['CF1'] // 2 if 'CF1' in cart else 0,
    'APPL': lambda cart, specials_applied: (cart['AP1'] - specials_applied['APOM']) if 'AP1' in cart and cart['AP1'] >= 3 else 0
}

specials_value = {
    'BOGO': prices['CF1'],
    'APPL': prices['AP1'] - 4.5,
    'CHMK': prices['MK1'],
    'APOM': prices['AP1'] * 0.5
}

# cart is a frequency map of items
def apply_specials(cart):
    specials_applied = {}
    for special, rule in specials_rules.items():
        specials_applied[special] = rule(cart, specials_applied)

    discount = 0
    for special, times_applied in specials_applied.items():
        discount += times_applied * specials_value[special]
        
    return discount