import os
import sys
import time
import requests

URL = "https://mcauleylab.ucsd.edu/public_datasets/data/googlelocal/places.clean.json.gz"
DEST = os.path.join("data", "raw", "places.clean.json.gz")

def download_file(url, dest):
    os.makedirs(os.path.dirname(dest), exist_ok=True)
    if os.path.exists(dest):
        print(f"File already exists: {dest} ({os.path.getsize(dest)} bytes)")
        return
    print(f"Downloading from {url} to {dest}...")
    start_time = time.time()
    response = requests.get(url, stream=True, timeout=60)
    response.raise_for_status()
    total_size = int(response.headers.get('content-length', 0))
    downloaded = 0
    with open(dest, 'wb') as f:
        for chunk in response.iter_content(chunk_size=1024 * 1024):
            if chunk:
                f.write(chunk)
                downloaded += len(chunk)
                elapsed = time.time() - start_time
                mb = downloaded / (1024 * 1024)
                total_mb = total_size / (1024 * 1024)
                speed = mb / elapsed if elapsed > 0 else 0
                if int(mb) % 25 == 0 or downloaded == total_size:
                    print(f"Downloaded: {mb:.1f}/{total_mb:.1f} MB ({downloaded*100/total_size:.1f}%) at {speed:.2f} MB/s")
    print(f"Finished downloading in {time.time() - start_time:.2f} seconds.")

if __name__ == "__main__":
    download_file(URL, DEST)
