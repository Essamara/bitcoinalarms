import requests
import json
import time

def get_current_block_height(rpc_url, username, password):
    """Retrieves the current block height using JSON HTTP request."""
    headers = {'content-type': 'application/json'}
    payload = {
        "method": "getblockcount",
        "params": [],
        "jsonrpc": "1.0",
        "id": "curltest"  # Can be any string
    }

    try:
        response = requests.post(
            rpc_url,
            data=json.dumps(payload),
            headers=headers,
            auth=(username, password)
        )
        response.raise_for_status()  # Raise an exception for bad status codes (4xx or 5xx)
        data = response.json()
        if "result" in data:
            return data["result"]
        elif "error" in data:
            print(f"RPC Error: {data['error']}")  # Print RPC error details
            return None
        else:
            print("Unexpected RPC response format:", data)
            return None
    except requests.exceptions.RequestException as e:
        print(f"Request error: {e}")
        return None
    except json.JSONDecodeError as e:
        print(f"JSON decode error: {e}. Response text: {response.text}")
        return None
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
        return None

# Replace with your actual RPC credentials
rpc_url = "http://localhost:port"  # Default Bitcoin Core RPC port
username = "user"
password = "pass"
sound_file = "C:/ohyeah.wav"  # Replace with actual path

# Function to play sound remains unchanged (assuming sound libraries are installed)
import sounddevice as sd
import soundfile as sf

def play_sound(sound_file):
    """Plays the specified sound file."""
    try:
        data, fs = sf.read(sound_file)
        sd.play(data, fs)
        sd.wait()
    except Exception as e:
        print(f"Error playing sound: {e}")

def main(check_interval=1):
    """Checks for block height changes and plays a sound."""
    previous_height = None
    while True:
        current_height = get_current_block_height(rpc_url, username, password)
        if current_height is not None and current_height != previous_height:
            print(f"Block height changed from {previous_height} to {current_height}")
            play_sound(sound_file)
            previous_height = current_height
        time.sleep(check_interval)

if __name__ == "__main__":
    main()