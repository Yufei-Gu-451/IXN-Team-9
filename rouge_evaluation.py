from rouge import FilesRouge
from app import text_summarizer
from app import file
import time

COMPRESSION_RATE = 0.1
NUMBER_OF_CLUSTERS = 4
ALGORITHM_NUM = 1
DISTANCE_NUM = 1
FILE_START = 2501
FILE_END = 3000
RESULT_FILE = 'Result/Result_{}_{}.txt'.format(str(ALGORITHM_NUM), str(DISTANCE_NUM))

files_rouge = FilesRouge()

score = {'rouge-1':{'r':0, 'p':0, 'f':0}, 'rouge-2':{'r':0, 'p':0, 'f':0}}

TEXT = 'Algorithm Type : {}    |    Distance Type : {}\n\n'.format(str(ALGORITHM_NUM), str(DISTANCE_NUM))
file.write_txt_file(output_file_name=RESULT_FILE, text=TEXT, append=False)

time.clock() # Initialize for Windows OS
sum_time = 0

for i in range(FILE_START, FILE_END + 1):
    ref_path = 'app/FullTexts/FullText-{}.txt'.format(str(i))
    hyp_path = 'app/Abstracts/Abstract-{}.txt'.format(str(i))

    begin_time = time.clock()

    text_summarizer.summarize_text(input_file=ref_path, output_file=hyp_path, \
        compression_rate=COMPRESSION_RATE, number_of_clusters=NUMBER_OF_CLUSTERS, \
            algorithm_num=ALGORITHM_NUM, distance_num=DISTANCE_NUM)
    end_time = time.clock()

    sum_time += end_time - begin_time

    scores = files_rouge.get_scores(hyp_path=hyp_path, ref_path=ref_path, avg = True)
    print('\n\n----------------- Rouge Evaluation {} ------------------\n\n'.format(i))

    score['rouge-1']['r'] += scores['rouge-1']['r']
    score['rouge-1']['p'] += scores['rouge-1']['p']
    score['rouge-1']['f'] += scores['rouge-1']['f']

    score['rouge-2']['r'] += scores['rouge-2']['r']
    score['rouge-2']['p'] += scores['rouge-2']['p']
    score['rouge-2']['f'] += scores['rouge-2']['f']

    iteration = i + 1 - FILE_START

    Text = '\nIteration : {}    |   '.format(str(iteration))
    Text += 'Average Time Cost : {} second\n'.format(str(sum_time/iteration))

    Text += '\nBegin Time : {}    |    End Time : {}\n'.format(str(begin_time), str(end_time))

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


K-Cluster       Distance : 1
Iteration : 50    |   Average Time Cost : 10.859030840000003 second
Begin Time : 638.085975    |    End Time : 655.868262

score['rouge-1']['r'] = 0.17496245517407158
score['rouge-1']['p'] = 1.0
score['rouge-1']['f'] = 0.297098147025459
score['rouge-2']['r'] = 0.11982774714161382
score['rouge-2']['p'] = 0.9625161757780231
score['rouge-2']['f'] = 0.2128433293073943
'''