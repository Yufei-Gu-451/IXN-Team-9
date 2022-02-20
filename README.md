# IXN-Team-9

Project Keyword : Remote consultations analysis / Automatic Speech Recognition (ASR) / Natural Language Processing (NLP) / Medical database

Project Description : Use natural language processing or understanding to allow audio individualised records - a set of smart documents with a common infrastructure but individually populated using the NLP captured from remote consultation. The aim is for near real-time electronic documents to be created for the clinical team - clinical documentation -, the patient or parents, to improve patient understanding and experience, and for the laboratory diagnostics, to ensure the correct test with the necessary clinical history.

1. Download the BERT repository from https://github.com/google-research/bert, 
    and copy the files to the BERT directory.
2. Download a BioBERT pretrained model from https://github.com/naver/biobert-pretrained, 
    change the name of 'model.ckpt_100001.\*' to 'bert_model.ckpt.\*',
    and copy the files to the BERT directory.
3. Create a virtual enviroument of Python 3.7 using command 'conda create -n env python==3.7'
4. Activate the virtual enviroument using command 'conda activate env'
5. Install all dependencys using command 'pip install -r requirements.txt'