from rouge import FilesRouge
from app import text_summarizer
from app import file
import time

#------------------------------ Parameters
COMPRESSION_RATE = 0.1
NUMBER_OF_CLUSTERS = 5
ALGORITHM_NUM = 7
DISTANCE_NUM = 2
ITERATION_NUM = 1
FILE_START = 2502
FILE_END = FILE_START + ITERATION_NUM


#------------------------------ Print algorithm method
if ALGORITHM_NUM == 1:
    TEXT = 'Algorithm : K-Center Clustering\n\n'
elif ALGORITHM_NUM == 2:
    TEXT = 'Algorithm : K-Means Clustering\n\n'
elif ALGORITHM_NUM == 3:
    TEXT = 'Algorithm : Bi-K-Means Clustering\n\n'
elif ALGORITHM_NUM == 4:
    TEXT = 'Algorithm : Single Agglomerative Clustering\n\n'
elif ALGORITHM_NUM == 5:
    TEXT = 'Algorithm : Complete Agglomerative Clustering\n\n'
elif ALGORITHM_NUM == 6:
    TEXT = 'Algorithm : Upgma Agglomerative Clustering\n\n'
elif ALGORITHM_NUM == 7:
    TEXT = 'Algorithm : DBSCAN Clustering\n\n'
    if DISTANCE_NUM != 1:
        print('\n\nException : DBSCAN has no choice of distance method\n\n')
elif ALGORITHM_NUM == 8:
    TEXT = 'Algorithm : OPTICS Clustering\n\n'
elif ALGORITHM_NUM == 9:
    TEXT = 'Algorithm : Mean Shift Clustering\n\n'
    if DISTANCE_NUM != 1:
        print('\n\nException : Mean Shift has no choice of distance method\n\n')
elif ALGORITHM_NUM == 10:
    TEXT = 'Algorithm : Text Rank\n\n'
    if DISTANCE_NUM != 1:
        print('\n\nException : Text Rank has no choice of distance method\n\n')
else:
    print('\n\nException : Unknown Algorithm Num. Please reset the algorithm num.\n\n')

#------------------------------ Print distance method
if DISTANCE_NUM == 1:
    TEXT += 'Metric : Euclidean Distance\n\n\n'
elif DISTANCE_NUM == 2:
    TEXT += 'Metric : Manhattan Distance\n\n\n'
elif DISTANCE_NUM == 3:
    TEXT += 'Metric : Cosine Similarity\n\n\n'
else:
    print('\n\nException : Unknown Distance Num. Please reset the distance num.\n\n')

# Create results file and write headlines
RESULT_FILE = 'Result/Result_{}_{}.txt'.format(str(ALGORITHM_NUM), str(DISTANCE_NUM))
file.create_file(RESULT_FILE)
file.write_txt_file(output_file_name=RESULT_FILE, text=TEXT, append=False)


# Initilize variables
files_rouge = FilesRouge()
score = {'rouge-1':{'r':0, 'p':0, 'f':0}, 'rouge-2':{'r':0, 'p':0, 'f':0}}
time.clock() # Initialize for Windows OS
sum_time = 0

# Main loop for testing
for i in range(FILE_START, FILE_END):
    iteration = i + 1 - FILE_START
    print('\n\n----------------- Rouge Evaluation {} ------------------\n\n'.format(iteration))

    ref_path = 'app/FullTexts/FullText-{}.txt'.format(str(i))
    hyp_path = 'app/Abstracts/Abstract-{}-{}-{}.txt'.format(str(i), str(ALGORITHM_NUM), str(DISTANCE_NUM))

    file.create_file(hyp_path)

    begin_time = time.clock()
    text_summarizer.summarize_text(input_file=ref_path, output_file=hyp_path, \
        compression_rate=COMPRESSION_RATE, number_of_clusters=NUMBER_OF_CLUSTERS, \
            algorithm_num=ALGORITHM_NUM, distance_num=DISTANCE_NUM)
    end_time = time.clock()

    sum_time += end_time - begin_time

    scores = files_rouge.get_scores(hyp_path=hyp_path, ref_path=ref_path, avg = True)

    score['rouge-1']['r'] += scores['rouge-1']['r']
    score['rouge-1']['p'] += scores['rouge-1']['p']
    score['rouge-1']['f'] += scores['rouge-1']['f']

    score['rouge-2']['r'] += scores['rouge-2']['r']
    score['rouge-2']['p'] += scores['rouge-2']['p']
    score['rouge-2']['f'] += scores['rouge-2']['f']


    Text = '\nIteration : {}    |   '.format(str(iteration))
    Text += 'Average Time Cost : {} second\n'.format(str(sum_time/iteration))

    Text += 'score[\'rouge-1\'][\'r\'] = {}\n'.format(str(score['rouge-1']['r']/iteration))
    Text += 'score[\'rouge-1\'][\'p\'] = {}\n'.format(str(score['rouge-1']['p']/iteration))
    Text += 'score[\'rouge-1\'][\'f\'] = {}\n'.format(str(score['rouge-1']['f']/iteration))

    Text += 'score[\'rouge-2\'][\'r\'] = {}\n'.format(str(score['rouge-2']['r']/iteration))
    Text += 'score[\'rouge-2\'][\'p\'] = {}\n'.format(str(score['rouge-2']['p']/iteration))
    Text += 'score[\'rouge-2\'][\'f\'] = {}\n'.format(str(score['rouge-2']['f']/iteration))

    file.write_txt_file(output_file_name=RESULT_FILE, text=Text, append=True)

    file.delete_file(hyp_path)