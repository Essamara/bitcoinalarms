import requests
import time
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

def get_current_block_height(url):
    """Retrieves the current block height."""
    payload = {
        "jsonrpc": "1.0",
        "method": "getblockchaininfo",  # Use getblockchaininfo
        "params": [],
        "id": 1
    }
    headers = {
        "accept": "application/json",
        "content-type": "application/json"
    }

    try:
        response = requests.post(url, json=payload, headers=headers)
        data = response.json()
        if 'result' in data and 'blocks' in data['result']: #check for blocks
            return int(data['result']['blocks'])
        else:
            print(f"Error retrieving block height: Invalid response: {data}")
            return None
    except requests.exceptions.RequestException as e:
        print(f"Request error: {e}")
        return None
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
        return None

def main(url, sound_file, check_interval=10):
    """Checks for block height changes and plays a sound."""
    previous_height = None
    while True:
        current_height = get_current_block_height(url)
        if current_height is not None and current_height != previous_height:
            print(f"Block height changed from {previous_height} to {current_height}")
            play_sound(sound_file)
            previous_height = current_height
        time.sleep(check_interval)

if __name__ == "__main__":
    rpc_user = "user"  # Replace with your RPC username
    rpc_password = "pass"  # Replace with your RPC password
    rpc_port = 7788
    url = f"http://{rpc_user}:{rpc_password}@127.0.0.1:{rpc_port}" # Updated URL

    sound_file = "c:/ohyeah.wav" # Replace with your actual path
    check_interval = 1

    main(url, sound_file, check_interval)