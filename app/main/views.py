from flask import render_template
from . import main

import speech_to_text
import text_summarizer
import file

@main.route('/')
def index():
    return render_template('index.html')

@main.route('/uploadPage', methods=['GET'])
def uploadAudioPage():
    return render_template('uploadPage.html')

@main.route('/upload', methods=['POST'])
def upload():
    file = request.files['inputFile']

    writeFile(file.read(), file.filename)

    speech_to_text.speech_to_text(inputfile='FILE/' + file.filename, outputfile="FILE/temp_input.txt")

    text_summarizer.summarize_text(input_file='FILE/temp_input.txt', output_file="FILE/temp_output.txt", compression_rate=0.3, number_of_clusters=2)

    processedFile = open("FILE/temp_output.txt", "r")
    
    upload = Files(name=file.filename, processedData=processedFile.read().encode())
    processedFile.close()
    
    db.session.add(upload)
    db.session.commit()
    
    return file.filename

@main.route('/download')
def download():
    upload = Files.query.get(12)
    filename = (upload.name)[:-4] + ".txt"
    send_file(BytesIO(upload.processedData), attachment_filename=filename, as_attachment=True)
    return render_template('index.html', form=form)
    
    # return send_file(BytesIO(upload.processedData), attachment_filename=filename, as_attachment=True)
    
    # writeFile(upload.data, upload.name)

    # return upload.name + " written to FILE"


    # return BytesIO(upload.data)

def writeFile(data, filename):
    with open('FILE/' + filename, 'wb') as file:
        file.write(data)

                           
