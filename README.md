# IXN-Team-9

Project Keyword : Remote consultations analysis / Automatic Speech Recognition (ASR) / Natural Language Processing (NLP) / Medical database

Project Description : Use natural language processing or understanding to allow audio individualised records - a set of smart documents with a common infrastructure but individually populated using the NLP captured from remote consultation. The aim is for near real-time electronic documents to be created for the clinical team - clinical documentation -, the patient or parents, to improve patient understanding and experience, and for the laboratory diagnostics, to ensure the correct test with the necessary clinical history.


# User Manual

## Step 1: Install Python 3.7 and configure enviroument on your server
Python3.7 is the only version of Python we used to compile our server app. All our following guidelines are based on Python3.7.

Step 1.A: Install the python3.7 package
Linux (Ubuntu 20.04): Install python3.7 through terminal 
                      `sudo apt-get install python3.7`
                      `sudo apt-get install python3.7-dev`

Step 1.B: Configure the python interpreter

Linux (Ubuntu 20.04): Add `alias python3=‘/bin/usr/python3.7’` to the .bashrc file under your user directory. (You may need to open a new terminal or use ‘. .bashrc’ to apply the new rule)

Step 1.C: Install pip in python 3.7 directory
Linux (Ubuntu 20.04): `curl https://bootstrap.pypa.io/get-pip.py -o get-pip.py`
                      `python3.7 get-pip.py`


## Step 2: Install the mysql server



## Step 4: Download the source code of the server
`git clone `
Then enter the package directory 'cd IXN-Team-9'

## Step 5: Install the required Python Library using Pip
Linux (Ubuntu 20.04): `python3 -m pip install -r requirements.txt`


## Step 6: Download the bert package
1. Download the BERT repository from https://github.com/google-research/bert, 
    and copy the files to the BERT directory.
1. Download a BioBERT pretrained model from https://github.com/naver/biobert-pretrained, 
    change the name of 'model.ckpt_100001.\*' to 'bert_model.ckpt.\*',
    and copy the files to the BERT directory.

## Step 7: Run the web application.py
`python3 application.py`
