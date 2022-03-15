from tkinter import W
from xmlrpc.client import MAXINT
import nltk
import json_lines
import math
import numpy as np
import networkx as nx
from . import file

# Change this variable to your python3.7 directory
#PYTHON_DIRECTORY = '/Library/Frameworks/Python.framework/Versions/3.7/bin/python3.7'
PYTHON_DIRECTORY = '/usr/bin/python3.7'

#-------------------- CLASSES --------------------

class Feature:
    def __init__(self, word):
        self.token = word
        self.weight_list = []

class Sentence:
    def __init__(self, num, txt):
        self.sentence_number = num
        self.sentence_text = txt
        self.avg_similarity = 0
        self.feature_list = []
        self.representation = []
        self.cluster_index = 0

    def distance(self, second_vector, distance_num):
        if distance_num == 1:
            return self.eucl_distance(second_vector=second_vector)
        elif distance_num == 2:
            return self.manh_distance(second_vector=second_vector)
        elif distance_num == 3:
            return 1 / self.cosine_similarity(second_vector=second_vector)
        else:
            print('\n\nException : Unknown Distance Method. Please reset the distance num.\n\n')

    # Euclidean Distance
    def eucl_distance(self, second_vector):
        eucl_dist = 0
        first_vector = self.representation

        for i in range(len(first_vector)):
            eucl_dist += (first_vector[i] - second_vector[i]) ** 2

        eucl_dist = math.sqrt(eucl_dist)
        return eucl_dist

    # Manhattan Distance
    def manh_distance(self, second_vector):
        manh_dist = 0
        first_vector = self.representation

        for i in range(len(first_vector)):
            manh_dist += abs(first_vector[i] - second_vector[i])

        return manh_dist

    # Cosine Similarity
    def cosine_similarity(self, second_vector):
        numerator, term1, term2 = 0, 0, 0

        first_vector = self.representation
        for i in range(len(first_vector)):
            numerator += first_vector[i] * second_vector[i]
            term1 += first_vector[i] ** 2
            term2 += second_vector[i] ** 2

        denominator = math.sqrt(term1) * math.sqrt(term2)
        cosine_sim = numerator / denominator
        return cosine_sim

    def set_token_list(self, tkn_list):
        self.feature_list = tkn_list

    def get_token_list(self):
        return self.feature_list;


class Cluster:
    def __init__(self, sentence_num):
        self.center = sentence_num
        self.mean = []
        self.members = []
        self.summary_members = 0

    def add_member(self, sentence_index):
        self.members.append(sentence_index)

    def remove_member(self, sentence_index):
        self.members.remove(sentence_index)

    # Select the new center of the cluster
    def update_center(self, sentence_list, distance_num):
        # Computer the average distance of every sentence in the cluster to all other senetences
        distance_dict = {}
        for i in self.members:
            distance_dict[i] = 0
            for j in self.members:
                distance_dict[i] += sentence_list[i].distance(sentence_list[j].representation, distance_num)
            
            distance_dict[i] = distance_dict[i]/len(self.members)

        # Sort the distance list and update the cluster with its newest center
        #print('Update center : distance dict : ', similiarity_dict, '\n')
        sorted_list = sorted(distance_dict.items(), key = lambda item:item[1])
        #print('The new center point : ', sorted_list[0], '\n\n')
        self.center = sorted_list[0][0]
        return self.center

'''
    def update_mean(self, sentence_list):
        if len(sentence_list) < 1:
            self.mean = []
        else:
            self.

        for sentence in self.members:
            vector = sentence
'''



#-------------------- MAIN BODY OF SUMMARIZER
def summarize_text(*, input_file, output_file, compression_rate, number_of_clusters, algorithm_num, distance_num):
    print('\n-------------------- Preprocessing started --------------------\n')


    print('\n-------------------- Split sentences and get tokens --------------------\n')

    input_text = file.read_txt_file(filename=input_file)
    input_sentences = nltk.sent_tokenize(input_text)
    sentence_split_text, preprocessed_text = '', ''
    sentence_num = 1
    
    for sentence in input_sentences:
        tokenized_sentence = nltk.word_tokenize(sentence)

        if sentence_num > 1:
            sentence_split_text += '\n'
            preprocessed_text += '\n'

        sentence_split_text += sentence
        preprocessed_text += str(tokenized_sentence)
        sentence_num += 1


    print('\n-------------------- Prepare text files --------------------\n')

    # Define the temporal files used
    temp_file_address = 'app/file/temp_input/temp_input_{}_{}.txt'.format(str(algorithm_num), str(distance_num))
    temp_file_token_address = 'app/file/temp_input_token/temp_input_token_{}_{}.txt'.format(str(algorithm_num), str(distance_num))
    temp_file_features_address = 'app/file/temp_features/temp_features_{}_{}.jsonl'.format(str(algorithm_num), str(distance_num))

    # Write sentences and tokens
    file.write_txt_file(output_file_name=temp_file_address, text=sentence_split_text, append=False)
    file.write_txt_file(output_file_name=temp_file_token_address, text=preprocessed_text, append=False)


    print('\n-------------------- Feature extraction --------------------\n')

    import os
    os.system(PYTHON_DIRECTORY + ' app/bert/extract_features.py'\
            ' --input_file=' + temp_file_address +' --output_file=' + temp_file_features_address + \
                ' --vocab_file=app/bert/vocab.txt --bert_config_file=app/bert/bert_config.json'\
                    ' --init_checkpoint=app/bert/bert_model.ckpt --layers=-1 --max_seq_length=128 --batch_size=8')


    print('\n-------------------- Initialize Sentences --------------------\n')

    sentence_list, sentence_num = [], 0

    for sentence in input_sentences:
        sentence_num += 1
        temp_sentence = Sentence(sentence_num, sentence)
        sentence_list.append(temp_sentence)


    print('\n-------------------- Get features for every sentence --------------------\n')

    sentence_num = 0
    with open(temp_file_features_address) as input_file:
        for line in json_lines.reader(input_file):
            feature_set = line['features']

            for feature in feature_set:
                if feature['token'] in ['[CLS]', '[SEP]']:
                    continue;

                temp_feature = Feature(feature['token'])
            
                for layer in feature['layers']:
                    temp_feature.weight_list = layer['values']

                if sentence_num < len(sentence_list):
                    sentence_list[sentence_num].feature_list.append(temp_feature)

            sentence_num += 1


    print('\n-------------------- Compute a representation for every sentence --------------------\n')

    for sentence in sentence_list:
        if len(sentence.feature_list) > 0:
            for weight in sentence.feature_list[0].weight_list:
                sentence.representation.append(0.0)
        
        for feature in sentence.feature_list:
            i = 0
            for weight in feature.weight_list:
                sentence.representation[i] += weight
                i += 1

        for weight in sentence.representation:
            weight /= len(sentence.feature_list)


    print('\n\n-------------------- Clustering started --------------------\n')

    if algorithm_num == 1:
        final_summary = k_cluster(sentence_list=sentence_list, compression_rate=compression_rate, \
            number_of_clusters=number_of_clusters, distance_num=distance_num)
    elif algorithm_num == 2:
        final_summary = agglomerative_cluster(sentence_list=sentence_list, compression_rate=compression_rate, \
            number_of_clusters=number_of_clusters, distance_num=distance_num)
    elif algorithm_num == 3:
        final_summary = text_rank(sentence_list=sentence_list, compression_rate=compression_rate)
    else:
        print('\n\nException : Unknown Algorithm. Please reset the algorithm num.\n\n')

    file.write_txt_file(output_file_name=output_file, text=final_summary, append=False)



# K-Clustering Algorithm - Algorithm No. 1
def k_cluster(*, sentence_list, compression_rate, number_of_clusters, distance_num):
    print('The number of sentences : ', len(sentence_list), '\n')

    if number_of_clusters >= len(sentence_list):
        final_summary = ''
        for sentence in sentence_list:
            final_summary += sentence + ' '
            return final_summary

    #-------------------- Initialize the initial cluster with random centers
    cluster_list, center_list = [], [] # Stored center of all Clusters

    for i in range(number_of_clusters):
        temp_cluster = Cluster(i)
        #print(sentence_list[i].sentence_text)
        cluster_list.append(temp_cluster)
        center_list.append(i)

    center_list.sort()
    print(center_list)

    #-------------------- Starting clustering algorithm
    for iteration in range(1, 51):
        print('\n\n-------------------- Iteration: ', iteration, '--------------------\n')
        
        #-------------------- Allocate each sentence to a cluster with a lowest distance
        for i in range(len(sentence_list)):
            temp_distance_dict = {}
            for center in center_list:  # Compute its distance to each centers
                temp_distance_dict[center] = sentence_list[i].distance(sentence_list[center].representation, distance_num)

            sorted_list = sorted(temp_distance_dict.items(), key = lambda item:item[1])
            #print(sorted_list)

            for cluster in cluster_list: # Allocate the sentence to the cloest center
                if cluster.center == sorted_list[0][0]:
                    cluster.add_member(i)

        #-------------------- For each cluster, find a new center
        temp_center_list = []
        for cluster in cluster_list:
            temp_center_list.append(cluster.update_center(sentence_list, distance_num))
        temp_center_list.sort()
        print('New center list : ', temp_center_list, '\n')

        #-------------------- If the clustering doesn't change, exit the loop
        if center_list != temp_center_list:
            center_list = temp_center_list

            # Re-intialize each cluster
            for cluster in cluster_list:
                cluster.members = []
        else:
            print("\n-------------------- Exit Loop --------------------\n")
            break

    print("\n-------------------- Final Summary --------------------\n")
    final_summary = produce_summary_for_clustering(cluster_list=cluster_list, \
        sentence_list=sentence_list, compression_rate=compression_rate, distance_num=distance_num)

    print("\n-------------------- Finished --------------------\n")
    return final_summary

# Agglomerative-Clustering Algorithm - Algorithm No. 2
def agglomerative_cluster(*, sentence_list, compression_rate, number_of_clusters, distance_num):
    clusters = []
    for i in range(len(sentence_list)):
        temp_cluster = Cluster(i)
        temp_cluster.members.append(i)
        clusters.append(temp_cluster)

    #-------------------- Starting clustering algorithm
    end_of_clustering = False

    iteration = 1
    while (end_of_clustering != True):
        print('\n---------- Iteration: {} ----------\n'.format(iteration))

        min_distance = MAXINT
        similar_cluster1 = -1
        similar_cluster2 = -1

        for i in range(0, len(clusters)-1):
            for j in range(i, len(clusters)):
                #----------Compute the distance between two clusters
                temp_distance = 0
                for index1 in clusters[i].members:
                    for index2 in clusters[j].members:
                        temp_distance += sentence_list[index1]\
                            .distance(sentence_list[index2].representation, distance_num) / len(clusters[j].members)

                if temp_distance < min_distance:
                    min_distance = temp_distance
                    similar_cluster1 = i
                    similar_cluster2 = j

        #---------- Merge two most similar clusters
        clusters[similar_cluster1].members = clusters[similar_cluster1].members + clusters[similar_cluster2].members
        clusters.remove(clusters[similar_cluster2])
        print(similar_cluster1, 'and', similar_cluster2, 'merged')
        print('\n---------- Number of clusters: {} ----------\n'.format(str(len(clusters))))

        iteration += 1
        if len(clusters) <= number_of_clusters:
            end_of_clustering = True

    #----------- Produce final summary
    print("\n-------------------- Final Summary --------------------\n")
    final_summary = produce_summary_for_clustering(cluster_list=clusters, \
        sentence_list=sentence_list, compression_rate=compression_rate, distance_num=distance_num)

    print("\n-------------------- Finished --------------------\n")
    return final_summary


# Select sentences in clustering algorithms and produce a final summary
def produce_summary_for_clustering(*, cluster_list, sentence_list, compression_rate, distance_num):

    print("\n\n-------------------- Produce the final summary --------------------\n\n")

    selected_sentences = [] #select the top sentences in each cluster
    for cluster in cluster_list:
        print('\n\nCenter of cluster : ', cluster.center)
        distance_dict = {}

        for i in cluster.members: # i is the no of sentences in sentence_list
            #print(i, sentence_list[i].distance(sentence_list[cluster.center].representation))
            distance_dict[i] = sentence_list[i].distance(sentence_list[cluster.center].representation, distance_num)

        # Sort the sentences according to their distance to center
        sorted_list = sorted(distance_dict.items(), key = lambda item:item[1])
        print('Sorted similiarity dict : ', sorted_list)

        # Calculate the number of sentences to be selected in this cluster
        num_sentence_selected = int(len(cluster.members)*compression_rate) + 1
        print('Number of sentence selected in this cluster : ', num_sentence_selected)

        # Select the best sentences in this cluster
        print('Sentence selected : ', end = '')
        for i in range(num_sentence_selected):
            selected_sentences.append(sorted_list[i][0])
            print(sorted_list[i][0], end = ' ')

    # Restore the original order
    selected_sentences.sort()
    print('\n\nAll sentence selected : ', selected_sentences, '\n\n')

    # Find the corresponding sentence text and add them to final summary
    final_summary = ''
    for i in selected_sentences:
        print(sentence_list[i].sentence_text)
        final_summary += sentence_list[i].sentence_text + ' '

    return final_summary


# TextRank / PageRank Algorithm - Algorithm No. 3
def text_rank(*, sentence_list, compression_rate):
    similarity_matrix = np.zeros([len(sentence_list), len(sentence_list)])

    for i in range(len(sentence_list)):
        for j in range(len(sentence_list)):
            similarity_matrix[i][j] = sentence_list[i].cosine_similarity(sentence_list[j].representation)
            #print(i, j, end=' ')
        #print('\n')

    print('\n---------------------- Constructing nx graph ----------------------\n')
    nx_graph = nx.from_numpy_array(similarity_matrix)

    print('\n------------------------ Ranking sentences ------------------------\n')
    scores = nx.pagerank(nx_graph)
    print(scores)

    print('\n------------------------ Sort sentences -------------------------\n')
    sorted_list = sorted(scores.items(), key = lambda item:item[1], reverse=True)
    print(sorted_list)

    print("\n-------------------- Select sentences --------------------\n")
    selected_sentences = []
    for i in range(int(len(sentence_list)*compression_rate)):
        selected_sentences.append(sorted_list[i][0])
    selected_sentences.sort()
    print('All sentence selected : ', selected_sentences, '\n')

    print("\n-------------------- Produce final summary --------------------\n")
    final_summary = ''
    for i in selected_sentences:
        print(sentence_list[i].sentence_text)
        final_summary += sentence_list[i].sentence_text + ' '
    
    print("\n---------------------- Finished ----------------------\n")
    return final_summary