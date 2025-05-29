import requests
from pprint import PrettyPrinter

BASE_URL = "https://fixer.io/"
API_KEY = "54008584d3808dbe7bcc72920d28bbc3"  # Replace with your own if needed

printer = PrettyPrinter()

def get_currencies():
    url = f"{BASE_URL}symbols?access_key={API_KEY}"
    response = requests.get(url)
    data = response.json()

    if not data.get("success", False):
        print("Failed to fetch currency symbols.")
        return []

    symbols = data["symbols"]
    return list(symbols.items())

def print_currencies(currencies):
    for code, name in sorted(currencies):
        print(f"{code} - {name}")

def get_rates():
    url = f"{BASE_URL}latest?access_key={API_KEY}"
    response = requests.get(url)
    data = response.json()

    if not data.get("success", False):
        print("Failed to fetch exchange rates.")
        return None

    return data["rates"]

def exchange_rate(currency1, currency2):
    rates = get_rates()
    if rates is None:
        return

    if currency1 not in rates or currency2 not in rates:
        print("Invalid currency code.")
        return

    # Convert via EUR as base (Fixer.io free plan limitation)
    rate = rates[currency2] / rates[currency1]
    print(f"{currency1} -> {currency2} = {rate}")
    return rate

def convert(currency1, currency2, amount):
    rate = exchange_rate(currency1, currency2)
    if rate is None:
        return

    try:
        amount = float(amount)
    except ValueError:
        print("Invalid amount.")
        return

    converted_amount = rate * amount
    print(f"{amount} {currency1} is equal to {converted_amount:.2f} {currency2}")
    return converted_amount

def main():
    currencies = get_currencies()
    if not currencies:
        return

    print("Welcome to the Fixer.io Currency Converter!")
    print("Commands:")
    print("  list    - List available currencies")
    print("  convert - Convert from one currency to another")
    print("  rate    - Get exchange rate between two currencies")
    print("  q       - Quit the program")
    print()

    while True:
        command = input("Enter a command (q to quit): ").lower()

        if command == "q":
            break
        elif command == "list":
            print_currencies(currencies)
        elif command == "convert":
            currency1 = input("Enter base currency: ").upper()
            amount = input(f"Enter amount in {currency1}: ")
            currency2 = input("Enter target currency: ").upper()
            convert(currency1, currency2, amount)
        elif command == "rate":
            currency1 = input("Enter base currency: ").upper()
            currency2 = input("Enter target currency: ").upper()
            exchange_rate(currency1, currency2)
        else:
            print("Unknown command. Try 'list', 'convert', 'rate', or 'q'.")

main()
