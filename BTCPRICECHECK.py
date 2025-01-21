import requests
import time
from playsound import playsound

# API endpoint and threshold values
API_URL = "https://api.coindesk.com/v1/bpi/currentprice.json"
SMALL_PRICE_THRESHOLD = 50
LARGE_PRICE_THRESHOLD = 1000

# Sound file paths (replace with your actual file paths)
BIG_UP_SOUND = r"C:\sounds\bigup.wav"
SMALL_UP_SOUND = r"C:\sounds\upsound.wav"
BIG_DOWN_SOUND = r"C:\sounds\bigdown.wav"
SMALL_DOWN_SOUND = r"C:\sounds\down.wav"

def get_current_price():
    """Fetches the current Bitcoin price."""
    try:
        response = requests.get(API_URL)
        response.raise_for_status()
        data = response.json()
        return float(data["bpi"]["USD"]["rate_float"])
    except requests.exceptions.RequestException as e:
        print(f"Error fetching price: {e}")
        return None

def play_sound(sound_file):
    """Plays a sound."""
    try:
        playsound(sound_file)
    except FileNotFoundError:
        print(f"Sound file '{sound_file}' not found.")

def main():
    """Checks Bitcoin price and plays sounds for changes."""
    previous_price = None

    while True:
        current_price = get_current_price()

        if current_price is not None:
            if previous_price is not None:
                price_change = current_price - previous_price

                if price_change > LARGE_PRICE_THRESHOLD:
                    print(f"Large price increase by ${price_change:.2f}")
                    play_sound(BIG_UP_SOUND)
                elif price_change > SMALL_PRICE_THRESHOLD:
                    print(f"Small price increase by ${price_change:.2f}")
                    play_sound(SMALL_UP_SOUND)
                elif price_change < -LARGE_PRICE_THRESHOLD:
                    print(f"Large price decrease by ${abs(price_change):.2f}")
                    play_sound(BIG_DOWN_SOUND)
                elif price_change < -SMALL_PRICE_THRESHOLD:
                    print(f"Small price decrease by ${abs(price_change):.2f}")
                    play_sound(SMALL_DOWN_SOUND)

            previous_price = current_price
        print(f"Current Price: {current_price}") # added current price output
        time.sleep(300)

if __name__ == "__main__":
    main()