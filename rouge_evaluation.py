from rouge import FilesRouge
from app import text_summarizer
from app import file

COMPRESSION_RATE = 0.1
NUMBER_OF_CLUSTERS = 4
ALGORITHM_NUM = 1
FILE_START = 2501
FILE_END = 4000
RESULT_FILE = 'Result.txt'

files_rouge = FilesRouge()

score = {'rouge-1':{'r':0, 'p':0, 'f':0}, 'rouge-2':{'r':0, 'p':0, 'f':0}}

file.write_txt_file(output_file_name=RESULT_FILE, text='Algorithm type : {}\n\n'.format(str(ALGORITHM_NUM)), append=False)

for i in range(FILE_START, FILE_END + 1):
    ref_path = 'app/FullTexts/FullText-{}.txt'.format(str(i))
    hyp_path = 'app/Abstracts/Abstract-{}.txt'.format(str(i))

    text_summarizer.summarize_text(input_file=ref_path, output_file=hyp_path, \
        compression_rate=COMPRESSION_RATE, number_of_clusters=NUMBER_OF_CLUSTERS, \
            algorithm_num=ALGORITHM_NUM)

    scores = files_rouge.get_scores(hyp_path=hyp_path, ref_path=ref_path, avg = True)
    print('\n\n----------------- Rouge Evaluation {} ------------------\n\n'.format(i))

    score['rouge-1']['r'] += scores['rouge-1']['r']
    score['rouge-1']['p'] += scores['rouge-1']['p']
    score['rouge-1']['f'] += scores['rouge-1']['f']

    score['rouge-2']['r'] += scores['rouge-2']['r']
    score['rouge-2']['p'] += scores['rouge-2']['p']
    score['rouge-2']['f'] += scores['rouge-2']['f']

    iteration = i + 1 - FILE_START
    Text = 'Iteration : {}\n'.format(str(iteration))

    Text += 'score[\'rouge-1\'][\'r\'] = {}\n'.format(str(score['rouge-1']['r']/iteration))
    Text += 'score[\'rouge-1\'][\'p\'] = {}\n'.format(str(score['rouge-1']['p']/iteration))
    Text += 'score[\'rouge-1\'][\'f\'] = {}\n'.format(str(score['rouge-1']['f']/iteration))

    Text += 'score[\'rouge-2\'][\'r\'] = {}\n'.format(str(score['rouge-2']['r']/iteration))
    Text += 'score[\'rouge-2\'][\'p\'] = {}\n'.format(str(score['rouge-2']['p']/iteration))
    Text += 'score[\'rouge-2\'][\'f\'] = {}\n'.format(str(score['rouge-2']['f']/iteration))

    file.write_txt_file(output_file_name=RESULT_FILE, text=Text, append=True)

'''
Merge Cluster
score['rouge-1']['r'] = 0.06713925647564942
score['rouge-1']['p'] = 0.8004642481168254
score['rouge-1']['f'] = 0.12040021094700251
score['rouge-2']['r'] = 0.02408601014709728
score['rouge-2']['p'] = 0.44519501600899747
score['rouge-2']['f'] = 0.0445483952247947
'''