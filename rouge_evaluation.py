from concurrent.futures import thread
from xmlrpc.client import MAXINT
from rouge import FilesRouge
from app import text_summarizer
from app import file
from threading import Thread
import random

#------------------------------ Parameters
COMPRESSION_RATE = 0.05
NUMBER_OF_CLUSTERS = 6
FILE_START = 1001
FILE_END = 1080
THREAD_NUM = 8


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
        final_summary_1_1 = text_summarizer.k_center(sentence_list=self.sentence_list, \
                compression_rate=self.compression_rate, number_of_clusters=self.number_of_clusters, distance_num=1)
        file.create_file(self.output_file+'-1-1.txt')
        file.write_txt_file(output_file_name=self.output_file+'-1-1.txt', text=final_summary_1_1, append=False)

        final_summary_1_2 = text_summarizer.k_center(sentence_list=self.sentence_list, \
                compression_rate=self.compression_rate, number_of_clusters=self.number_of_clusters, distance_num=2)
        file.create_file(self.output_file+'-1-2.txt')
        file.write_txt_file(output_file_name=self.output_file+'-1-2.txt', text=final_summary_1_2, append=False)

        final_summary_1_3 = text_summarizer.k_center(sentence_list=self.sentence_list, \
                compression_rate=self.compression_rate, number_of_clusters=self.number_of_clusters, distance_num=3)
        file.create_file(self.output_file+'-1-3.txt')
        file.write_txt_file(output_file_name=self.output_file+'-1-3.txt', text=final_summary_1_3, append=False)


        final_summary_4 = text_summarizer.single_agglomerative_cluster(sentence_list=self.sentence_list, \
                compression_rate=self.compression_rate, number_of_clusters=self.number_of_clusters, distance_num=1)
        file.create_file(self.output_file+'-4.txt')
        file.write_txt_file(output_file_name=self.output_file+'-4.txt', text=final_summary_4, append=False)



class SummarizeTextThreadTwo(Thread):
    def __init__(self, output_file, sentence_list, compression_rate, number_of_clusters) -> None:
        super().__init__()
        self.output_file = output_file
        self.sentence_list = sentence_list
        self.compression_rate = compression_rate
        self.number_of_clusters = number_of_clusters

    def run(self):
        final_summary_2_1 = text_summarizer.k_means(sentence_list=self.sentence_list, \
                compression_rate=self.compression_rate, number_of_clusters=self.number_of_clusters, distance_num=1)
        file.create_file(self.output_file+'-2-1.txt')
        file.write_txt_file(output_file_name=self.output_file+'-2-1.txt', text=final_summary_2_1, append=False)

        final_summary_2_2 = text_summarizer.k_means(sentence_list=self.sentence_list, \
                compression_rate=self.compression_rate, number_of_clusters=self.number_of_clusters, distance_num=2)
        file.create_file(self.output_file+'-2-2.txt')
        file.write_txt_file(output_file_name=self.output_file+'-2-2.txt', text=final_summary_2_2, append=False)

        final_summary_2_3 = text_summarizer.k_means(sentence_list=self.sentence_list, \
                compression_rate=self.compression_rate, number_of_clusters=self.number_of_clusters, distance_num=3)
        file.create_file(self.output_file+'-2-3.txt')
        file.write_txt_file(output_file_name=self.output_file+'-2-3.txt', text=final_summary_2_3, append=False)


        final_summary_5 = text_summarizer.complete_agglomerative_cluster(sentence_list=self.sentence_list, \
                compression_rate=self.compression_rate, number_of_clusters=self.number_of_clusters, distance_num=1)
        file.create_file(self.output_file+'-5.txt')
        file.write_txt_file(output_file_name=self.output_file+'-5.txt', text=final_summary_5, append=False)



class SummarizeTextThreadThree(Thread):
    def __init__(self, output_file, sentence_list, compression_rate, number_of_clusters) -> None:
        super().__init__()
        self.output_file = output_file
        self.sentence_list = sentence_list
        self.compression_rate = compression_rate
        self.number_of_clusters = number_of_clusters

    def run(self):
        final_summary_3_1 = text_summarizer.bi_k_means(sentence_list=self.sentence_list, \
                compression_rate=self.compression_rate, number_of_clusters=self.number_of_clusters, distance_num=1)
        file.create_file(self.output_file+'-3-1.txt')
        file.write_txt_file(output_file_name=self.output_file+'-3-1.txt', text=final_summary_3_1, append=False)

        final_summary_3_2 = text_summarizer.bi_k_means(sentence_list=self.sentence_list, \
                compression_rate=self.compression_rate, number_of_clusters=self.number_of_clusters, distance_num=2)
        file.create_file(self.output_file+'-3-2.txt')
        file.write_txt_file(output_file_name=self.output_file+'-3-2.txt', text=final_summary_3_2, append=False)

        final_summary_3_3 = text_summarizer.bi_k_means(sentence_list=self.sentence_list, \
                compression_rate=self.compression_rate, number_of_clusters=self.number_of_clusters, distance_num=3)
        file.create_file(self.output_file+'-3-3.txt')
        file.write_txt_file(output_file_name=self.output_file+'-3-3.txt', text=final_summary_3_3, append=False)


        final_summary_6 = text_summarizer.upgma_agglomerative_cluster(sentence_list=self.sentence_list, \
                compression_rate=self.compression_rate, number_of_clusters=self.number_of_clusters, distance_num=1)
        file.create_file(self.output_file+'-6.txt')
        file.write_txt_file(output_file_name=self.output_file+'-6.txt', text=final_summary_6, append=False)


class SummarizeTextThreadFour(Thread):
    def __init__(self, output_file, sentence_list, compression_rate, number_of_clusters) -> None:
        super().__init__()
        self.output_file = output_file
        self.sentence_list = sentence_list
        self.compression_rate = compression_rate
        self.number_of_clusters = number_of_clusters

    def run(self):
        final_summary_7 = text_summarizer.dbscan_clustering(sentence_list=self.sentence_list, \
                compression_rate=self.compression_rate)
        file.create_file(self.output_file+'-7.txt')
        file.write_txt_file(output_file_name=self.output_file+'-7.txt',   text=final_summary_7,   append=False)

        final_summary_8_1 = text_summarizer.optics_clustering(sentence_list=self.sentence_list, \
                compression_rate=self.compression_rate, distance_num=1)
        file.create_file(self.output_file+'-8-1.txt')
        file.write_txt_file(output_file_name=self.output_file+'-8-1.txt', text=final_summary_8_1, append=False)

        final_summary_8_2 = text_summarizer.optics_clustering(sentence_list=self.sentence_list, \
                compression_rate=self.compression_rate, distance_num=2)
        file.create_file(self.output_file+'-8-2.txt')
        file.write_txt_file(output_file_name=self.output_file+'-8-2.txt', text=final_summary_8_2, append=False)

        final_summary_8_3 = text_summarizer.optics_clustering(sentence_list=self.sentence_list, \
                compression_rate=self.compression_rate, distance_num=3)
        file.create_file(self.output_file+'-8-3.txt')
        file.write_txt_file(output_file_name=self.output_file+'-8-3.txt', text=final_summary_8_3, append=False)

        final_summary_9 = text_summarizer.mean_shift_clustering(sentence_list=self.sentence_list, \
                compression_rate=self.compression_rate)
        file.create_file(self.output_file+'-9.txt')
        file.write_txt_file(output_file_name=self.output_file+'-9.txt',   text=final_summary_9,   append=False)

        final_summary_10 = text_summarizer.text_rank(sentence_list=self.sentence_list, \
                compression_rate=self.compression_rate)
        file.create_file(self.output_file+'-10.txt')
        file.write_txt_file(output_file_name=self.output_file+'-10.txt',  text=final_summary_10,  append=False)




#------------------------------------------------------ Testing Algorithm
def summarize_text_test(*, input_file, output_file, compression_rate, number_of_clusters):
    print('\n-------------------- Create temp files --------------------\n')

    # Generate a random unused number for temp files
    temp_file_num = 0
    while file.exists_file('app/file/temp_input/temp_input_{}.txt'.format(str(temp_file_num))):
        temp_file_num = random.randint(0, MAXINT)

    # Define the name of temp files
    temp_file_address = 'app/file/temp_input/temp_input_{}.txt'.format(str(temp_file_num))
    temp_file_token_address = 'app/file/temp_input_token/temp_input_token_{}.txt'.format(str(temp_file_num))
    temp_file_features_address = 'app/file/temp_features/temp_features_{}.jsonl'.format(str(temp_file_num))

    # Create temp files
    file.create_file(temp_file_address)
    file.create_file(temp_file_token_address)
    file.create_file(temp_file_features_address)


    print('\n-------------------- Preprocessing started --------------------\n')

    sentence_list = text_summarizer.preprocessing(input_file=input_file, temp_file_address=temp_file_address, \
        temp_file_token_address=temp_file_token_address, temp_file_features_address=temp_file_features_address)

    print('-------------- The number of sentences : ', len(sentence_list), '--------------')
    # If too less text : output and exit summarization
    if len(sentence_list) <= number_of_clusters:
        print('\n-------------------- Number of sentence less than number of clusters --------------------\n')
        file.write_txt_file(output_file_name=output_file, text=file.read_txt_file(filename=input_file), append=False)
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

    file.delete_file(temp_file_address)
    file.delete_file(temp_file_token_address)
    file.delete_file(temp_file_features_address)

    return 0


def rouge_evaluation(*, file_start, file_end, postfix):
    #-------------------- Initilize variables
    files_rouge = FilesRouge()
    score = {'rouge-1':{'r':0, 'p':0, 'f':0}, 'rouge-2':{'r':0, 'p':0, 'f':0}}

    for i in range(file_start, file_end):
        iteration = i + 1 - file_start
        print('\n\n----------------- Rouge Evaluation No.{} ------------------\n\n'.format(iteration))

        ref_path = 'app/file/Abstracts/Abstract-{}.txt'.format(str(i))
        hyp_path = 'app/file/Hypothesis/Hypothesis-{}-{}.txt'.format(str(i), postfix)

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


        file.write_txt_file(output_file_name='file/Result/Result-'+postfix, text=Text, append=True)


def text_summarization(*, file_start, file_end):
    for i in range(file_start, file_end):
        iteration = i - file_start + 1
        print('\n----------------- File No.{} ------------------\n'.format(i))
        src_path = 'app/file/FullTexts/FullText-{}.txt'.format(str(i))
        hyp_path = 'app/file/Hypothesis/Hypothesis-{}'.format(str(i))

        summarize_text_test(input_file=src_path, output_file=hyp_path, \
            compression_rate=COMPRESSION_RATE, number_of_clusters=NUMBER_OF_CLUSTERS)

if __name__ == '__main__':
    if (FILE_END - FILE_START + 1) % THREAD_NUM == 0:
        gap = int((FILE_END - FILE_START + 1) / THREAD_NUM)

        for i in range(THREAD_NUM):
            thread = TextSummarizationThread(FILE_START + i * gap, FILE_START + (i + 1) * gap)
            thread.start()

        postfix_list = ['1-1', '1-2', '1-3', '2-1', '2-2', '2-3', '3-1', '3-2', '3-3', \
                '4', '5', '6', '7', '8-1', '8-2', '8-3', '9', '10']

        for postfix in postfix_list:
                rouge_evaluation(file_start = FILE_START, file_end = FILE_END, postfix=postfix)
    else:
        print('Error Thread Number')