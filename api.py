from flask import Flask, jsonify
import os

app = Flask(__name__)
HASH_FILE_PATH = "hash.txt"

@app.route('/get_hash', methods=['GET'])
def get_hash():
    if os.path.exists(HASH_FILE_PATH):
        with open(HASH_FILE_PATH, 'r') as f:
            hash_value = f.read().strip()
        return jsonify({"sha256": hash_value})
    else:
        return jsonify({"error": "Hash file not found"}), 404

