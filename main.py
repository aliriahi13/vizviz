from flask import Flask, render_template, request, jsonify
import hmac
import hashlib
from urllib.parse import unquote
from config import Token

token: str = Token 

def validate_init_data(init_data: str, bot_token: str):
    vals = {k: unquote(v) for k, v in [s.split('=', 1) for s in init_data.split('&')]}
    data_check_string = '\n'.join(f"{k}={v}" for k, v in sorted(vals.items()) if k != 'hash')

    secret_key = hmac.new("WebAppData".encode(),bot_token.encode(),hashlib.sha256).digest()
    h = hmac.new(secret_key, data_check_string.encode(), hashlib.sha256)
    return h.hexdigest() == vals['hash']


app = Flask(__name__)

@app.route('/')
def main_page():
    return render_template('index.html')

@app.route('/process', methods=['GET', 'POST'])
def validate_user():
    data = request.get_json()
    if data and 'value' in data:
        print(data['value'])
        isvalid = validate_init_data(data['value'],token)
        print(isvalid)
        return jsonify(isvalid=isvalid)
    return jsonify(isvalid=False)

if __name__ == '__main__':
    app.run(port=8080)

