import numpy as np
from flask import Flask, request, render_template, flash, url_for, redirect, jsonify, session, Response
import os
from os.path import join, dirname
import pandas as pd
import matplotlib.pyplot as plt

app= Flask(__name__)

# enable debugging mode
app.config["DEBUG"] = True

# Upload folder
UPLOAD_FOLDER = 'static/files'
app.config['UPLOAD_FOLDER'] =  UPLOAD_FOLDER

app.secret_key = 'dljsaklqk24e21cjn!Ew@@dsa5'  ## Secret key is necessary to use session in Flask, key should be really secure

#csvData= pd.DataFrame()

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/calc', methods=['GET','POST'])
def calculator():
    int_numbers= [int(x) for x in request.form.values()]
    numbers= np.array(int_numbers)
    suma= numbers.sum()
    return render_template('calc.html', suma= suma)

@app.route('/drx', methods=['GET', 'POST'])
def uploadFiles():
    if request.method=='POST':
        if 'file' not in request.files:
            flash('No file part')
            return redirect(request.url)
        uploaded_file= request.files['file']
        if uploaded_file.filename != '':
            file_path = os.path.join(app.config['UPLOAD_FOLDER'], uploaded_file.filename)
            # set the file path
            uploaded_file.save(file_path)
            # save the file
            session['Archivo']= file_path    
            session['Filename']= uploaded_file.filename
        #csvData = pd.read_csv(file_path, on_bad_lines='skip')
        #lista_header= list(csvData.columns.values)
        #plotDrx(csvData, uploaded_file.filename)
        #return jsonify(x= csvData['Angle'].values.tolist(), y= csvData['Intensity'].values.tolist())
        return redirect(url_for('plot_drx'))   
        
    return render_template('drx.html') 

#def plotDrx(df, filename):

#    plt.plot(df['Angle'], df['Intensity'])
#    plt.xlabel('Angulo')
#    plt.ylabel('Intensidad')
#    plt.title('DRX YBCO - '+ filename)
#    plt.xlim([10, 80])
#    plt.ylim([0, 20000])
#    plt.savefig('static/images/plot_drx.png')


@app.route('/drx/api', methods=['GET'])
def returnJSON():
    file_path= session.get('Archivo')
    filename= session.get('Filename')
    #return file_path
    #return jsonify(file_path)
    csvData = pd.read_csv(file_path, on_bad_lines='skip')
    return jsonify(x= csvData['Angle'].values.tolist(), y= csvData['Intensity'].values.tolist(), type= 'scatter', name= filename)


@app.route('/plot_drx', methods=['GET'])
def plot_drx():
    return render_template('plot_drx.html')


@app.route('/stream')
def generate_audio():
    def generate():
        song_folder= 'static/songs'
        song_name= 'song_test.mp3'
        with open(os.path.join(song_folder,song_name), 'rb') as fmp3:
            data= fmp3.read(1024)
            while data:
                yield data
                data= fmp3.read(1024)
    return generate(), {"Content-type": "audio/mp3"}        
    #return Response(generate(), mimetype="audio/mp3")

@app.route('/music', methods=['GET'])
def music_test():
    return render_template('music_test.html')

if (__name__ == "__main__"):
    app.run(port = 5000)
