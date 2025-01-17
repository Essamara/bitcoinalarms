import requests
import time
from playsound import playsound  # Assuming you have playsound installed (pip install playsound)

# API endpoint and threshold values
API_URL = "https://api.coindesk.com/v1/bpi/currentprice.json"
PRICE_THRESHOLD = 2  # Minimum price change (USD) to trigger sound

# Sound file paths (replace with your actual file paths)
UP_SOUND = "C:\sounds\goinup.wav"  # Sound for price increase
DOWN_SOUND = "C:\sounds\goindown.wav"  # Sound for price decrease

def get_current_price():
    """Fetches the current Bitcoin price in USD from the Coindesk API."""
    try:
        response = requests.get(API_URL)
        response.raise_for_status()  # Raise an exception for non-200 status codes
        data = response.json()
        return float(data["bpi"]["USD"]["rate_float"])
    except requests.exceptions.RequestException as e:
        print(f"Error fetching price: {e}")
        return None  # Handle API errors gracefully (optional)

def play_sound(sound_file):
    """Plays a sound using the playsound library."""
    try:
        playsound(sound_file)
    except FileNotFoundError:
        print(f"Sound file '{sound_file}' not found.")

def main():
    """Continuously checks Bitcoin price and plays sounds for significant changes."""
    previous_price = None

    while True:
        current_price = get_current_price()

        if current_price is not None:
            if previous_price is not None:
                price_change = current_price - previous_price
                if price_change > PRICE_THRESHOLD:
                    print(f"Price increased by ${price_change:.2f} - Playing up sound")
                    play_sound(UP_SOUND)
                elif price_change < -PRICE_THRESHOLD:
                    print(f"Price decreased by ${abs(price_change):.2f} - Playing down sound")
                    play_sound(DOWN_SOUND)
            previous_price = current_price
        print (current_price)
        time.sleep(300)  # Check price every minute (adjust as needed)

if __name__ == "__main__":
    main()