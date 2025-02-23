from flask import Flask, render_template, request, redirect, url_for, send_from_directory, flash
import os
import socket
from werkzeug.utils import secure_filename
from image_converter import ImageConverter
from  display import Display
script_dir = os.path.dirname(os.path.abspath(__file__))
upload_path = lib_path = os.path.join(script_dir, 'pic')
os.makedirs(upload_path, exist_ok=True)

display = Display()
app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = upload_path
app.config['ALLOWED_EXTENSIONS'] = {'png', 'jpg', 'jpeg'}
app.secret_key = 'setsecretkey'

def get_pi_ip():
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    try:
        s.connect(("8.8.8.8", 80))
        ip = s.getsockname()[0]
    finally:
        s.close()
    return ip

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        # Handle file upload
        file = request.files['file']
        if file:
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            imageConverter = ImageConverter()
            imageConverter.process_image(filename)
        return redirect('/')

    # List existing images
    images = [img for img in os.listdir(app.config['UPLOAD_FOLDER'])]
    return render_template('index.html', images=images)

@app.route('/start-display')
def start_display():
    display.display_image()
    return redirect('/')

@app.route('/reset-display')
def reset_display():
    display.clear_display()
    return redirect('/')

@app.route('/flip-orientation')
def flip_orientation():
    # Flip orientation logic TO DO
    return redirect('/')

@app.route('/delete-image/<filename>', methods=['POST'])
def delete_image(filename):
    os.remove(os.path.join(app.config['UPLOAD_FOLDER'], filename))
    return redirect('/')
    
@app.route('/images/<filename>')
def uploaded_file(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)

@app.route('/select-image')
def select_image():
    image_name = request.args.get('image')
    display.display_image(image_name)
    return '', 204  # No content response

if __name__ == '__main__':
    ip_address = get_pi_ip()
    display.display_qrcode(ip_address)
    app.run(host='0.0.0.0', port=5000)
    
    
