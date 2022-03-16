# IXN-Team-9

Project Keyword : Remote consultations analysis / Automatic Speech Recognition (ASR) / Natural Language Processing (NLP) / Medical database

Project Description : Use natural language processing or understanding to allow audio individualised records - a set of smart documents with a common infrastructure but individually populated using the NLP captured from remote consultation. The aim is for near real-time electronic documents to be created for the clinical team - clinical documentation -, the patient or parents, to improve patient understanding and experience, and for the laboratory diagnostics, to ensure the correct test with the necessary clinical history.


###User Manual

##Step 1: Install Python 3.7 on your server
Python3.7 is the only version of Python we used to compile our server app. All our following guidelines are based on Python3.7.

Linux (Ubuntu 20.04): Install python3.7 through terminal `sudo apt-get install python3.7-dev`

Step 1. A: Configure the python interpreter

Linux (Ubuntu 20.04): Add ‘alias python3=‘/bin/usr/python3.7’’ to the .bashrc file under your user directory. (You may need to open a new terminal or use ‘. .bashrc’ to apply the new rule)


Step 1. B: Install pip in python 3.7 directory
	
Pip is a package management system that simplifies the installation and management of software packages written in Python such as those found in the Python Package Index (PyPI).


Step 3: Enter the 


1. Download and Install python 3.7 on your computer
2. Download the BERT repository from https://github.com/google-research/bert, 
    and copy the files to the BERT directory.
3. Download a BioBERT pretrained model from https://github.com/naver/biobert-pretrained, 
    change the name of 'model.ckpt_100001.\*' to 'bert_model.ckpt.\*',
    and copy the files to the BERT directory.
4. Install all dependencys using command 'pip install -r requirements.txt'
5. Run the web app 'python3 application.py'
