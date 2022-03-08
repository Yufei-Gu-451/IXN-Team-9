'''
This code was written by Milad Moradi
Institute for Artificial Intelligence and Decision Support
Medical University of Vienna
'''

from typing_extensions import final
import nltk
import json_lines
import random
import math
import numpy as np
from numpy import double
import networkx as nx

#-------------------- CLASSES

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
        
    def eucl_distance(self, second_vector):
        eucl_dist = 0
        i = 0
        for weight in self.representation:
            eucl_dist += (weight - second_vector[i]) ** 2
            i += 1
        
        eucl_dist = math.sqrt(eucl_dist)
        return eucl_dist;
    
    def cosine_similarity(self, second_vector):
        numerator = 0
        term1 = 0
        term2 = 0
        i = 0

        for weight in self.representation:
            numerator += weight * second_vector[i]
            term1 += weight ** 2
            term2 += second_vector[i] ** 2
            i += 1
            
        denominator = math.sqrt(term1) * math.sqrt(term2)
        cosine_sim = numerator / denominator
        return cosine_sim

    def set_token_list(self, tkn_list):
        self.feature_list = tkn_list
    
    def get_token_list(self):
        return self.feature_list;

class Cluster:
    def __init__(self, num):
        self.cluster_number = num
        self.mean = []
        self.members = []
        self.summary_members = 0

    def add_member(self, sentence_index):
        self.members.append(sentence_index)

    def remove_member(self, sentence_index):
        self.members.remove(sentence_index)

#-------------------- THE MAIN SUMMARIZATION FUNCTION

def produce_summary(compression_rate, sentence_list, clusters):
    summary_size = math.ceil(len(sentence_list) * compression_rate) + 1
    print('\nSummary size: ', summary_size)

    i = 0
    for cluster in clusters:
        cluster.summary_members = round(summary_size * (len(cluster.members) / len(sentence_list)))
        i += 1
    
    #--------------------- Sentence selection
    
    #For every member of each cluster calculate the average similarity with other members within the same cluster 
    for cluster in clusters:
        for sentence_index in cluster.members:
            temp_avg_similarity = 0
            denominator = 0

            for other_member in cluster.members:
                if sentence_index != other_member:
                    temp_avg_similarity += sentence_list[sentence_index].cosine_similarity(sentence_list[other_member].representation)
                    denominator += 1

            if denominator != 0:
                temp_avg_similarity /= denominator
            sentence_list[sentence_index].avg_similarity = temp_avg_similarity

    #Sort members of each cluster
    for cluster in clusters:
        #-----------------Bubble sort
        for i in range(0, len(cluster.members)):
            for j in range(i+1, len(cluster.members)):
                if sentence_list[cluster.members[i]].avg_similarity < sentence_list[cluster.members[j]].avg_similarity:
                    temp_index = cluster.members[i]
                    cluster.members[i] = cluster.members[j]
                    cluster.members[j] = temp_index

    summary_index=[]
    for cluster in clusters:
        for i in range(0, cluster.summary_members):
            summary_index.append(cluster.members[i])

    summary_index.sort()
    print('---------- Sorted selected sentences --------')
    for index in summary_index:
        print(index)


    #----------------------- Producing final summary
    final_summary = ''
    for index in summary_index:
        print(sentence_list[index].sentence_text)
        final_summary += sentence_list[index].sentence_text + '\n'

    return final_summary

def output_summary(*, final_summary, output_address):
    output_file_text = open(output_address, 'w')
    output_file_text.write(final_summary)
    output_file_text.close()

#-------------------- MAIN BODY OF SUMMARIZER

def summarize_text(*, input_file, output_file, compression_rate, number_of_clusters):
    #--------------------- Arguments -----------------------

    print("Input file is:", input_file)
    print("Output file is:", output_file)
    print("Compression rate is:", compression_rate)
    print("Number of clusters is:", number_of_clusters)


    #-------------------- Preprocessing --------------------

    input_address = input_file
    print('---------- Preprocessing started ----------\n')

    opened_file = open(input_address, encoding = "utf8")
    print("-----File opened-----")

    input_text = opened_file.read()
    print("-----File read-----")
    
    input_sentences = nltk.sent_tokenize(input_text)
    
    sentence_split_text = ''
    preprocessed_text = ''
    sentence_num = 1
    
    for sentence in input_sentences:
        tokenized_sentence = nltk.word_tokenize(sentence)
        
        if sentence_num > 1:
            sentence_split_text += '\n'
            preprocessed_text += '\n'
        
        sentence_split_text += sentence
        preprocessed_text += str(tokenized_sentence)
        sentence_num += 1
        
    temp_file_address = 'FILE/temp_input.txt'
    temp_file_token_address = 'FILE/temp_input_token.txt'
    temp_file = open(temp_file_address, 'w')
    temp_file_token = open(temp_file_token_address, 'w')
    temp_file.write(sentence_split_text)
    temp_file_token.write(preprocessed_text)
    temp_file.close()
    temp_file_token.close()


    #-------------------- Feature extraction --------------------

    import os
    os.system('/Library/Frameworks/Python.framework/Versions/3.7/bin/python3.7 bert/extract_features.py --input_file=FILE/temp_input.txt --output_file=FILE/temp_features.jsonl --vocab_file=bert/vocab.txt --bert_config_file=bert/bert_config.json --init_checkpoint=bert/bert_model.ckpt --layers=-1 --max_seq_length=128 --batch_size=8')
    #os.system('python3 bert/extract_features.py --input_file=FILE/temp_input.txt --output_file=FILE/temp_features.jsonl --vocab_file=bert/vocab.txt --bert_config_file=bert/bert_config.json --init_checkpoint=bert/bert_model.ckpt --layers=-1 --max_seq_length=128 --batch_size=8')
    #-------------------- Clustering --------------------


    print('---------- Text summarizer started ----------\n')
    
    input_address_text = 'FILE/temp_input.txt'
    input_address_feature = 'FILE/temp_features.jsonl'
    output_address = output_file

    input_file = open(input_address_text)
    print("-----File opened-----")

    input_text = input_file.read()
    print("-----File read-----")

    input_sentences = nltk.sent_tokenize(input_text)

    sentence_list = []
    sentence_num = 0

    for sentence in input_sentences:
        sentence_num += 1
        temp_sentence = Sentence(sentence_num, sentence)
        sentence_list.append(temp_sentence)

    #--------------------

    sentence_num = 0
    with open(input_address_feature) as input_file:
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

    print('-----------------------------------------------')


    #-------------------- Compute a representation for every sentence

    for sentence in sentence_list:
        if len(sentence.feature_list) > 0:
            for weight in sentence.feature_list[0].weight_list:
                sentence.representation.append(0.0)
        
        for feature in sentence.feature_list:
            i = 0
            for weight in feature.weight_list:
                sentence.representation[i] += weight
                i += 1
            
        j = 0
        for weight in sentence.representation:
            sentence.representation[j] /= len(sentence.feature_list)
            j += 1

    #-------------------- Clustering Algorithm
    #final_summary = k_cluster(sentence_list=sentence_list, compression_rate=compression_rate, number_of_clusters=number_of_clusters)

    #final_summary = merge_cluster(sentence_list=sentence_list, compression_rate=compression_rate, number_of_clusters=number_of_clusters)

    final_summary = text_rank(sentence_list=sentence_list, compression_rate=compression_rate)

    output_summary(final_summary=final_summary, output_address=output_address)




def k_cluster(*, sentence_list, compression_rate, number_of_clusters):
    print('\n---------- Clustering started ----------')

    cluster_list = []
    center_list = []      # Stored center of all Clusters ; Termination Condition
    for i in range(number_of_clusters):
        temp_cluster = Cluster(i+1)
        temp_cluster.members.append(i)
        temp_cluster.center = sentence_list[i]
        print(sentence_list[i].sentence_text)
        cluster_list.append(temp_cluster)

        center_list.append(i)

    center_list.sort()

    #-------------------- Starting clustering algorithm
    for iteration in range(1, 51):
        print('---------- Iteration: ', iteration)
        
        #-------------------- Allocate each sentence to a cluster with a highest cosine similiarity
        for i in range(len(sentence_list)):
            min_similiarity = (0, 0)
            for j in range(number_of_clusters):
                temp_cluster_center = cluster_list[j].center
                temp_similiarity = sentence_list[i].cosine_similarity(temp_cluster_center.representation)
                if temp_similiarity > min_similiarity[1]:
                    min_similiarity = (j, temp_similiarity)
                #print(i, j, temp_similiarity, min_similiarity)

            cluster_list[min_similiarity[0]].members.append(i)
            #print(i, '-----------------------------------', min_similiarity)

        #-------------------- For each cluster, find a new center
        temp_center_list = []

        for cluster in cluster_list:
            max_similarity_sum = (0, 0)

            for i in range(len(cluster.members)):
                temp_similiarity_sum = 0
                for j in cluster.members:
                    temp_similiarity_sum += sentence_list[i].cosine_similarity(sentence_list[j].representation)

                #print(temp_similiarity_sum, max_similarity_sum)
                if temp_similiarity_sum > max_similarity_sum[1]:
                    max_similarity_sum = (i, temp_similiarity_sum)

            cluster.center = sentence_list[cluster.cluster_number]
            print(max_similarity_sum[0], max_similarity_sum[1]/len(cluster.members), len(cluster.members))

            temp_center_list.append(max_similarity_sum[0])

        
        temp_center_list.sort()
        if center_list != temp_center_list:
            center_list = temp_center_list
            for cluster in cluster_list:
                cluster.members = []
        else:
            final_summary = produce_summary(compression_rate, sentence_list, cluster_list)
            print("\n---------- Finished ----------")
            return final_summary


def merge_cluster(*, sentence_list, compression_rate, number_of_clusters):
    print('\n---------- Clustering started ----------')

    clusters = []
    for i in range(len(sentence_list)):
        temp_cluster = Cluster(i+1)
        temp_cluster.members.append(i)
        clusters.append(temp_cluster)

    #-------------------- Starting clustering algorithm
    end_of_clustering = False

    iteration = 1
    while (end_of_clustering != True):

        print('---------- Iteration: ', iteration)

        highest_similarity = -10000000000
        similar_cluster1 = -1
        similar_cluster2 = -1

        for i in range(0, len(clusters)):
            for j in range(0, len(clusters)):
                if i < j:

                    #----------Compute the similarity between two clusters
                    denominator = 0
                    temp_similarity = 0
                    for index1 in clusters[i].members:
                        for index2 in clusters[j].members:
                            temp_similarity += sentence_list[index1].cosine_similarity(sentence_list[index2].representation)
                            denominator += 1

                    if denominator != 0:
                        temp_similarity /= denominator

                    if temp_similarity > highest_similarity:
                        highest_similarity = temp_similarity
                        similar_cluster1 = i
                        similar_cluster2 = j

        #----------Merge two most similar clusters
        clusters[similar_cluster1].members = clusters[similar_cluster1].members + clusters[similar_cluster2].members
        clusters.remove(clusters[similar_cluster2])
        print(similar_cluster1, 'and', similar_cluster2, 'merged')
        print('Number of clusters: ', str(len(clusters)))

        iteration += 1
        if len(clusters) <= number_of_clusters:
            end_of_clustering = True
            final_summary = produce_summary(compression_rate, sentence_list, clusters)
            print("\n---------- Finished ----------")
            return final_summary


def text_rank(*, sentence_list, compression_rate):
    similarity_matrix = np.zeros([len(sentence_list), len(sentence_list)])

    for i in range(len(sentence_list)):
        for j in range(len(sentence_list)):
            similarity_matrix[i][j] = sentence_list[i].cosine_similarity(sentence_list[j].representation)
    
    nx_graph = nx.from_numpy_array(similarity_matrix)
    scores = nx.pagerank(nx_graph)

    ranked_sentence_list = sorted(((scores[i], s) for i,s in enumerate(sentence_list)), reverse=True)
    final_summary = ''
    print(len(sentence_list))
    for i in range(int(len(sentence_list)*compression_rate)):
        print(ranked_sentence_list[i][1].sentence_text + '\n')
        final_summary += ranked_sentence_list[i][1].sentence_text + '\n'
    return final_summary