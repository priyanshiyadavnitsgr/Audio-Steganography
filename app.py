from flask import Flask, render_template,request,send_file,jsonify
from audio_encrpy import Steganography
from audio_decrpy import Steganaograpy_decryption
import os
from werkzeug.utils import secure_filename


app=Flask(__name__)
app.config['UPLOAD_FOLDER'] = os.path.join(os.getcwd(),'UPLOAD_FOLDER')
app.config['EXTENSIONS'] = {'txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif','wav'}


@app.route('/loader')
def loader():
    return render_template('loader.html')

@app.route('/')
def index():
    return render_template('homepage.html')


@app.route('/encode')
def encode():
    return render_template('audio_encrypt.html')
        

@app.route('/decode')
def decode():
    return render_template('audio_decrypt.html')


@app.route('/encrypt',methods=["POST"])
def stegno_enc():
    msgs=request.form.get("message")
    print("msgs")
    sngs = request.files.get('file')
    file_name = secure_filename(sngs.filename)
    filename=file_name[:file_name.rindex(".")]+" encrypted.wav"
    filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
    sngs.save(filepath)
    print("till")
    file_data = Steganography().lsb(filepath,msgs)
    print("work done", filename)
    return jsonify({"success":" encryption"})
    ##return render_template("encrpy_success.html")

@app.route('/decrypt',methods=['POST'])
def stegno_dec():
    sngs = request.files.get('file')
    filename = secure_filename(sngs.filename)
    filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
    sngs.save(filepath)
    print("till")
    decoded_msg=Steganaograpy_decryption().decoder(filepath)
    print("worked till here")
    print(decoded_msg)
    return render_template("decrpy_success.html",decoded_msg=decoded_msg)

@app.route("/return-file/")
def return_file():
    return send_file("outputs\song_emb.wav")

@app.route('/success/')
def process():
    return render_template("encrpy_success.html")
	

if __name__=="__main__":
    app.run(debug=True,threaded=True)

    
    
    

