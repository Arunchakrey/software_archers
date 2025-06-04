class Payment:
    @staticmethod
    def process():
        print("\n--- Simulated Payment Gateway ---")
        input("Enter card number (simulated): ")
        input("Enter expiry date (MM/YY): ")
        input("Enter CVV: ")
        print("Processing payment...")
        print("Payment successful. Thank you for your purchase!\n")
