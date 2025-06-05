import re

class Payment:
    @staticmethod
    def process():
        print("\n--- Simulated Payment Gateway ---")

        while True:
            try:
                card = card_format()
                date = date_format()
                ccv = ccv_format()
                print("Processing payment...")
                print("Payment successful. Thank you for your purchase!\n")
                break
            except Exception as e:
                print(f"Invalid Payment Details: {e}")
                

def card_format():
    while True:
        card_num = input("Enter card number (simulated): ")
        card_form = r'^\d{4}-\d{4}-\d{4}-\d{4}'

        if re.fullmatch(card_form, card_num):
            return card_num
            
        else:
            raise Exception("Invalid card format. It must follow: xxxx-xxxx-xxxx-xxxx")

def date_format():
    while True:
        date = input("Enter expiry date (MM/YY): ")
        date_form = r'(0[1-9]|1[0-2])/\d{2}'

        if re.fullmatch(date_form, date):
            return date
            
        else:
            raise Exception("Invalid date. It must follow: MM/YY")

def ccv_format():
    while True:
        ccv = input("Enter CCV: ")
        ccv_form = r'^\d{3}$'
            
        if re.fullmatch(ccv_form, ccv):
            return ccv
            
        else:
            raise Exception("Invalid CCV. It must: xxx")
        
