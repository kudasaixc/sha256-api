import requests
import hashlib
import os
import logging

HASH_FILE_PATH = "/root/api/hash.txt"
GITHUB_API_URL = "https://api.github.com/repos/{TheRepoOwner}/{TheProject}/releases/latest"
LOG_FILE_PATH = "/root/api/update_check.log"

# Set up logging
logging.basicConfig(filename=LOG_FILE_PATH, level=logging.DEBUG,
                    format='%(asctime)s %(message)s')

def download_latest_release():
    logging.debug("Downloading latest release.")
    response = requests.get(GITHUB_API_URL)
    response.raise_for_status()
    data = response.json()
    zip_url = data["zipball_url"]

    response = requests.get(zip_url)
    response.raise_for_status()

    with open("/root/api/file.zip", "wb") as file:
        file.write(response.content)
    
    return "/root/api/file.zip"

def compute_sha256(file_path):
    logging.debug("Computing SHA256.")
    sha256_hash = hashlib.sha256()
    with open(file_path, "rb") as f:
        for byte_block in iter(lambda: f.read(4096), b""):
            sha256_hash.update(byte_block)
    return sha256_hash.hexdigest()

def update_hash_file(hash_value):
    logging.debug("Updating hash file.")
    with open(HASH_FILE_PATH, "w") as hash_file:
        hash_file.write(hash_value)

if __name__ == "__main__":
    try:
        logging.debug("Script started.")
        zip_path = download_latest_release()
        hash_value = compute_sha256(zip_path)
        update_hash_file(hash_value)
        logging.debug(f"Hash updated: {hash_value}")
    except Exception as e:
        logging.error(f"Error occurred: {e}")

