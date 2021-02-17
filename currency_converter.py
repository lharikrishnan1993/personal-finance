
'''
Rather than hard coding the number here, fetch it with Google API
'''

class CurrencyConverter:
    def __init__(self, base_currency='USD'):
        self.base_currency = base_currency
        self.current_currency = base_currency
    
    def set_current_currency(self, currency='USD'):
        self.current_currency = currency

    def convert(self, amount):
        if self.current_currency == 'INR':
            return amount * 0.014
        if self.current_currency == 'EUR':
            return amount * 1.21
        # Reset currency to avoid confusion
        self.current_currency = 'USD'
        return amount
