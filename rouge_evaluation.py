from concurrent.futures import thread
from xmlrpc.client import MAXINT
from rouge import FilesRouge
from app import text_summarizer
from app import os_file
from threading import Thread
import random
import nltk

#------------------------------ Parameters
COMPRESSION_RATE = 0.05
NUMBER_OF_CLUSTERS = 6
FILE_START = 1001
FILE_END = 1001
THREAD_NUM = 1

algorithm_list = [(1, 1), (1, 2), (1, 3), (2, 1), (2, 2), (2, 3), (3, 1), (3, 2), (3, 3), \
    (4, 1), (5, 1), (6, 1), (7, 1), (8, 1), (8, 2), (8, 3), (9, 1), (10, 1)]

algorithm_list1 = [(4, 1)]
algorithm_list2 = [(5, 1)]
algorithm_list3 = [(6, 1)]
algorithm_list4 = [(1, 1), (1, 2), (1, 3), (2, 1), (2, 2), (2, 3), (3, 1), (3, 2), (3, 3), \
    (7, 1), (8, 1), (8, 2), (8, 3), (9, 1), (10, 1)]


def file_not_written(output_file):
    if (os_file.exists_file(output_file) and os_file.read_txt_file(output_file) == '') or (not os_file.exists_file(output_file)):
        return True
    else:
        return False
    
class TextSummarizationThread(Thread):
    def __init__(self, file_start, file_end) -> None:
        super().__init__()
        self.file_start = file_start
        self.file_end = file_end

    def run(self):
        text_summarization(file_start = self.file_start, file_end = self.file_end)


class SummarizeTextThreadOne(Thread):
    def __init__(self, output_file, sentence_list, compression_rate, number_of_clusters) -> None:
        super().__init__()
        self.output_file = output_file
        self.sentence_list = sentence_list
        self.compression_rate = compression_rate
        self.number_of_clusters = number_of_clusters

    def run(self):
        for algorithm_num in algorithm_list1:
            output_file = self.output_file + '-' + str(algorithm_num[0]) + '-' + str(algorithm_num[1]) +'.txt'
            if file_not_written(output_file):
                os_file.create_file(output_file)
                final_summary = generate_summary_through_ml(sentence_list=self.sentence_list, compression_rate=self.compression_rate, \
                    number_of_clusters=self.number_of_clusters, algorithm_num=algorithm_num[0], distance_num = algorithm_num[1])
                os_file.write_txt_file(output_file_name=output_file, text=final_summary, append=False)
            else:
                print('\n\n---------- File Already Exists : {} ----------\n\n'.format(output_file))

class SummarizeTextThreadTwo(Thread):
    def __init__(self, output_file, sentence_list, compression_rate, number_of_clusters) -> None:
        super().__init__()
        self.output_file = output_file
        self.sentence_list = sentence_list
        self.compression_rate = compression_rate
        self.number_of_clusters = number_of_clusters

    def run(self):
        for algorithm_num in algorithm_list2:
            output_file = self.output_file + '-' + str(algorithm_num[0]) + '-' + str(algorithm_num[1]) +'.txt'
            if file_not_written(output_file):
                os_file.create_file(output_file)
                final_summary = generate_summary_through_ml(sentence_list=self.sentence_list, compression_rate=self.compression_rate, \
                    number_of_clusters=self.number_of_clusters, algorithm_num=algorithm_num[0], distance_num = algorithm_num[1])
                os_file.write_txt_file(output_file_name=output_file, text=final_summary, append=False)
            else:
                print('\n\n---------- File Already Exists : {} ----------\n\n'.format(output_file))


class SummarizeTextThreadThree(Thread):
    def __init__(self, output_file, sentence_list, compression_rate, number_of_clusters) -> None:
        super().__init__()
        self.output_file = output_file
        self.sentence_list = sentence_list
        self.compression_rate = compression_rate
        self.number_of_clusters = number_of_clusters

    def run(self):
        for algorithm_num in algorithm_list3:
            output_file = self.output_file + '-' + str(algorithm_num[0]) + '-' + str(algorithm_num[1]) +'.txt'
            if file_not_written(output_file):
                os_file.create_file(output_file)
                final_summary = generate_summary_through_ml(sentence_list=self.sentence_list, compression_rate=self.compression_rate, \
                    number_of_clusters=self.number_of_clusters, algorithm_num=algorithm_num[0], distance_num = algorithm_num[1])
                os_file.write_txt_file(output_file_name=output_file, text=final_summary, append=False)
            else:
                print('\n\n---------- File Already Exists : {} ----------\n\n'.format(output_file))


class SummarizeTextThreadFour(Thread):
    def __init__(self, output_file, sentence_list, compression_rate, number_of_clusters) -> None:
        super().__init__()
        self.output_file = output_file
        self.sentence_list = sentence_list
        self.compression_rate = compression_rate
        self.number_of_clusters = number_of_clusters

    def run(self):
        for algorithm_num in algorithm_list4:
            output_file = self.output_file + '-' + str(algorithm_num[0]) + '-' + str(algorithm_num[1]) +'.txt'
            if file_not_written(output_file):
                os_file.create_file(output_file)
                final_summary = generate_summary_through_ml(sentence_list=self.sentence_list, compression_rate=self.compression_rate, \
                    number_of_clusters=self.number_of_clusters, algorithm_num=algorithm_num[0], distance_num = algorithm_num[1])
                os_file.write_txt_file(output_file_name=output_file, text=final_summary, append=False)


def generate_summary_through_ml(*, sentence_list, compression_rate, number_of_clusters, algorithm_num, distance_num):
    final_summary = ''

    # K-Clustering Algorithm
    if algorithm_num == 1:
        final_summary = text_summarizer.k_center(sentence_list=sentence_list, compression_rate=compression_rate, \
            number_of_clusters=number_of_clusters, distance_num=distance_num)
    elif algorithm_num == 2:
        final_summary = text_summarizer.k_means(sentence_list=sentence_list, compression_rate=compression_rate, \
            number_of_clusters=number_of_clusters, distance_num=distance_num)
    elif algorithm_num == 3:
        final_summary = text_summarizer.bi_k_means(sentence_list=sentence_list, compression_rate=compression_rate, \
            number_of_clusters=number_of_clusters, distance_num=distance_num)
    # Hierarchical-Clustering
    elif algorithm_num == 4:
        final_summary = text_summarizer.single_agglomerative_cluster(sentence_list=sentence_list, compression_rate=compression_rate, \
            number_of_clusters=number_of_clusters, distance_num=distance_num)
    elif algorithm_num == 5:
        final_summary = text_summarizer.complete_agglomerative_cluster(sentence_list=sentence_list, compression_rate=compression_rate, \
            number_of_clusters=number_of_clusters, distance_num=distance_num)
    elif algorithm_num == 6:
        final_summary = text_summarizer.upgma_agglomerative_cluster(sentence_list=sentence_list, compression_rate=compression_rate, \
            number_of_clusters=number_of_clusters, distance_num=distance_num)
    # Density-Clustering
    elif algorithm_num == 7:
        final_summary = text_summarizer.dbscan_clustering(sentence_list=sentence_list, compression_rate=compression_rate)
    elif algorithm_num == 8:
        final_summary = text_summarizer.optics_clustering(sentence_list=sentence_list, compression_rate=compression_rate, \
            distance_num=distance_num)
    elif algorithm_num == 9:
        final_summary = text_summarizer.mean_shift_clustering(sentence_list=sentence_list, compression_rate=compression_rate)
    # Graph-based Algorithms
    elif algorithm_num == 10:
        final_summary = text_summarizer.text_rank(sentence_list=sentence_list, compression_rate=compression_rate)

    else:
        print('\n\nException : Unknown Algorithm. Please reset the algorithm num.\n\n')
        return 1
    
    return final_summary



#------------------------------------------------------ Testing Algorithm
def summarize_text_test(*, input_file, output_file, compression_rate, number_of_clusters):
    print('\n-------------------- Create temp files --------------------\n')

    # Generate a random unused number for temp files
    temp_file_num = 0
    while os_file.exists_file('app/file/temp_input/temp_input_{}.txt'.format(str(temp_file_num))):
        temp_file_num = random.randint(0, MAXINT)

    # Define the name of temp files
    temp_file_address = 'app/file/temp_input/temp_input_{}.txt'.format(str(temp_file_num))
    temp_file_token_address = 'app/file/temp_input_token/temp_input_token_{}.txt'.format(str(temp_file_num))
    temp_file_features_address = 'app/file/temp_features/temp_features_{}.jsonl'.format(str(temp_file_num))

    # Create temp files
    os_file.create_file(temp_file_address)
    os_file.create_file(temp_file_token_address)
    os_file.create_file(temp_file_features_address)


    print('\n-------------------- Preprocessing started --------------------\n')

    sentence_list = text_summarizer.preprocessing(input_file=input_file, temp_file_address=temp_file_address, \
        temp_file_token_address=temp_file_token_address, temp_file_features_address=temp_file_features_address)

    print('-------------- The number of sentences : ', len(sentence_list), '--------------')
    os_file.write_txt_file(output_file_name='app/file/Result/Result.txt', text=str(len(sentence_list)) + '\n', append=True)

    # If too less text : output and exit summarization
    if len(sentence_list) <= number_of_clusters:
        print('\n-------------------- Number of sentence less than number of clusters --------------------\n')
        os_file.write_txt_file(output_file_name=output_file, text=os_file.read_txt_file(filename=input_file), append=False)
        return

    print('\n\n-------------------- Clustering started --------------------\n')

    t1 = SummarizeTextThreadOne(output_file=output_file, sentence_list=sentence_list, \
        compression_rate=compression_rate, number_of_clusters=number_of_clusters)
    t2 = SummarizeTextThreadTwo(output_file=output_file, sentence_list=sentence_list, \
        compression_rate=compression_rate, number_of_clusters=number_of_clusters) 
    t3 = SummarizeTextThreadThree(output_file=output_file, sentence_list=sentence_list, \
        compression_rate=compression_rate, number_of_clusters=number_of_clusters)
    t4 = SummarizeTextThreadFour(output_file=output_file, sentence_list=sentence_list, \
        compression_rate=compression_rate, number_of_clusters=number_of_clusters)

    t1.start()
    t2.start()
    t3.start()
    t4.start()

    print('\n\n-------------------- Delete temp files --------------------\n')

    os_file.delete_file(temp_file_address)
    os_file.delete_file(temp_file_token_address)
    os_file.delete_file(temp_file_features_address)

    return 0


def text_summarization(*, file_start, file_end):
    for i in range(file_start, file_end):
        print('\n----------------- File No.{} ------------------\n'.format(i))
        src_path = 'app/file/FullTexts/FullText-{}.txt'.format(str(i))
        hyp_path = 'app/file/Hypothesis/Hypothesis-{}'.format(str(i))

        summarize_text_test(input_file=src_path, output_file=hyp_path, \
            compression_rate=COMPRESSION_RATE, number_of_clusters=NUMBER_OF_CLUSTERS)


def baseline_evaluation(*, file_start, file_end):
    for i in range(file_start, file_end + 1):
        print('\n----------------- File No.{} ------------------\n'.format(i))
        src_path = 'app/file/FullTexts/FullText-{}.txt'.format(str(i))
        hyp_path = 'app/file/Hypothesis/Hypothesis-{}-0-0.txt'.format(str(i))

        input_text = os_file.read_txt_file(filename=src_path)
        input_sentences = nltk.sent_tokenize(input_text)
        selected_sentence_num = int(len(input_sentences) * COMPRESSION_RATE)

        final_summary = ''
        for i in range(selected_sentence_num):
            final_summary += input_sentences[i] + ' '

        os_file.create_file(hyp_path)
        os_file.write_txt_file(output_file_name=hyp_path, text=final_summary, append=False)

    rouge_evaluation(file_start=file_start, file_end=file_end, algorithm_num=0, distance_num=0)


def rouge_evaluation(*, file_start, file_end, algorithm_num, distance_num):
    #-------------------- Initilize variables
    files_rouge = FilesRouge()
    score = {'rouge-1':{'r':0, 'p':0, 'f':0}, 'rouge-2':{'r':0, 'p':0, 'f':0}}

    for i in range(file_start, file_end + 1):
        iteration = i + 1 - file_start
        print('\n\n----------------- Rouge Evaluation No.{} ------------------\n\n'.format(i))

        ref_path = 'app/file/Abstracts/Abstract-{}.txt'.format(str(i))
        hyp_path = 'app/file/Hypothesis/Hypothesis-{}-{}-{}.txt'.format(str(i), str(algorithm_num), str(distance_num))
        print(hyp_path)

        scores = files_rouge.get_scores(hyp_path=hyp_path, ref_path=ref_path, avg = True)

        score['rouge-1']['r'] += scores['rouge-1']['r']
        score['rouge-1']['p'] += scores['rouge-1']['p']
        score['rouge-1']['f'] += scores['rouge-1']['f']

        score['rouge-2']['r'] += scores['rouge-2']['r']
        score['rouge-2']['p'] += scores['rouge-2']['p']
        score['rouge-2']['f'] += scores['rouge-2']['f']


        Text = '\nIteration : {}    |    File : {}\n\n'.format(str(iteration), str(i))

        Text += 'score[\'rouge-1\'][\'r\'] = {}\n'.format(str(score['rouge-1']['r']/iteration))
        Text += 'score[\'rouge-1\'][\'p\'] = {}\n'.format(str(score['rouge-1']['p']/iteration))
        Text += 'score[\'rouge-1\'][\'f\'] = {}\n'.format(str(score['rouge-1']['f']/iteration))

        Text += 'score[\'rouge-2\'][\'r\'] = {}\n'.format(str(score['rouge-2']['r']/iteration))
        Text += 'score[\'rouge-2\'][\'p\'] = {}\n'.format(str(score['rouge-2']['p']/iteration))
        Text += 'score[\'rouge-2\'][\'f\'] = {}\n'.format(str(score['rouge-2']['f']/iteration))

        output_file = 'app/file/Result/Result-' + str(algorithm_num) + '-' + str(distance_num) +'.txt'
        if file_not_written(output_file=output_file):
            os_file.create_file(output_file)
        os_file.write_txt_file(output_file_name=output_file, text=Text, append=True)



if __name__ == '__main__':
    if (FILE_END - FILE_START + 1) % THREAD_NUM == 0:
        gap = int((FILE_END - FILE_START + 1) / THREAD_NUM)
        thread_list = []

        for i in range(THREAD_NUM):
            thread = TextSummarizationThread(FILE_START + i * gap, FILE_START + (i + 1) * gap)
            thread_list.append(thread)

        for thread in thread_list:
            thread.start()

        for thread in thread_list:
            thread.join()

        for algorithm_num in algorithm_list:
            rouge_evaluation(file_start = FILE_START, file_end = FILE_END, \
                    algorithm_num=algorithm_num[0], distance_num=algorithm_num[1])
    else:
        print('Error Thread Number')

    baseline_evaluation(file_start=FILE_START, file_end=FILE_END)
