from xmlrpc.client import MAXINT, MININT
import nltk
import json_lines
import math
import random
import numpy as np
import networkx as nx
from sklearn.cluster import MeanShift, DBSCAN, OPTICS

from . import file

# Change this variable to your python3.7 directory
PYTHON_DIRECTORY = '/Library/Frameworks/Python.framework/Versions/3.7/bin/python3.7'
# PYTHON_DIRECTORY = '/usr/bin/python3.7'

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

    # Provides interface for different distance methods
    def distance(self, second_vector, distance_num):
        if distance_num == 1:
            return self.eucl_distance(second_vector=second_vector)
        elif distance_num == 2:
            return self.manh_distance(second_vector=second_vector)
        elif distance_num == 3:
            # Use inverse cosine similarity to model the distance between two sentences
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

    # Computer the mean 
    def update_mean(self, sentence_list):
        if len(sentence_list) < 1:
            self.mean = []
        else:
            feature_num = len(sentence_list[0].representation)
            self.mean = np.zeros(feature_num)

            for sentence in self.members:
                vector = sentence_list[sentence].representation
                for i in range(feature_num):
                    self.mean[i] += vector[i]

            for i in range(feature_num):
                self.mean[i] /= len(self.members)

        return self.mean

    # Compute and return the Sum of Squared Error
    def compute_sse(self, sentence_list, distance_num):
        mean = self.update_mean(sentence_list=sentence_list)
        sse = 0

        for sentence in self.members:
            distance = sentence_list[sentence].distance(mean, distance_num)
            sse += distance * distance

        return sse

    # Compute the average distance between all sentences from this cluster and another cluster
    def avg_distance(self, second_cluster, sentence_list, distance_num):
        distance = 0

        # Compute the distance sum between every sentence of two clusters
        for index1 in self.members:
            for index2 in second_cluster.members:
                distance += sentence_list[index1].distance(sentence_list[index2].representation, distance_num)

        # Computer the average distance between every sentence of two clusters
        distance /= len(second_cluster.members) * len(self.members)

        return distance

    # Compute the minimal distance between all sentences from this cluster and another cluster
    def min_distance(self, second_cluster, sentence_list, distance_num):
        min_distance, temp_distance = MAXINT, MAXINT

        # Compute the distance sum between every sentence of two clusters
        for index1 in self.members:
            for index2 in second_cluster.members:
                temp_distance = sentence_list[index1].distance(sentence_list[index2].representation, distance_num)

                if temp_distance < min_distance:
                    min_distance = temp_distance

        return min_distance

    # Compute the maximum distance between all sentences from this cluster and another cluster
    def max_distance(self, second_cluster, sentence_list, distance_num):
        max_distance, temp_distance = 0, 0

        # Compute the distance sum between every sentence of two clusters
        for index1 in self.members:
            for index2 in second_cluster.members:
                temp_distance = sentence_list[index1].distance(sentence_list[index2].representation, distance_num)

                if temp_distance > max_distance:
                    max_distance = temp_distance

        return max_distance




#---------------------------------------- MAIN BODY OF SUMMARIZER ----------------------------------------


def summarize_text(*, input_file, output_file, compression_rate, number_of_clusters, algorithm_num, distance_num):
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

    sentence_list = preprocessing(input_file=input_file, temp_file_address=temp_file_address, \
        temp_file_token_address=temp_file_token_address, temp_file_features_address=temp_file_features_address)

    print('-------------- The number of sentences : ', len(sentence_list), '--------------')
    # If too less text : output and exit summarization
    if len(sentence_list) <= number_of_clusters:
        print('\n-------------------- Number of sentence less than number of clusters --------------------\n')
        file.write_txt_file(output_file_name=output_file, text=file.read_txt_file(filename=input_file), append=False)
        return


    print('\n\n-------------------- Clustering started --------------------\n')

    # K-Clustering Algorithm
    if algorithm_num == 1:
        final_summary = k_center(sentence_list=sentence_list, compression_rate=compression_rate, \
            number_of_clusters=number_of_clusters, distance_num=distance_num)
    elif algorithm_num == 2:
        final_summary = k_means(sentence_list=sentence_list, compression_rate=compression_rate, \
            number_of_clusters=number_of_clusters, distance_num=distance_num)
    elif algorithm_num == 3:
        final_summary = bi_k_means(sentence_list=sentence_list, compression_rate=compression_rate, \
            number_of_clusters=number_of_clusters, distance_num=distance_num)

    # Hierarchical-Clustering
    elif algorithm_num == 4:
        final_summary = single_agglomerative_cluster(sentence_list=sentence_list, compression_rate=compression_rate, \
            number_of_clusters=number_of_clusters, distance_num=distance_num)
    elif algorithm_num == 5:
        final_summary = complete_agglomerative_cluster(sentence_list=sentence_list, compression_rate=compression_rate, \
            number_of_clusters=number_of_clusters, distance_num=distance_num)
    elif algorithm_num == 6:
        final_summary = upgma_agglomerative_cluster(sentence_list=sentence_list, compression_rate=compression_rate, \
            number_of_clusters=number_of_clusters, distance_num=distance_num)

    # Density-Clustering
    elif algorithm_num == 7:
        final_summary = dbscan_clustering(sentence_list=sentence_list, compression_rate=compression_rate)
    elif algorithm_num == 8:
        final_summary = optics_clustering(sentence_list=sentence_list, compression_rate=compression_rate, \
            distance_num=distance_num)
    elif algorithm_num == 9:
        final_summary = mean_shift_clustering(sentence_list=sentence_list, compression_rate=compression_rate)

    # Graph-based Algorithms
    elif algorithm_num == 10:
        final_summary = text_rank(sentence_list=sentence_list, compression_rate=compression_rate)

    else:
        print('\n\nException : Unknown Algorithm. Please reset the algorithm num.\n\n')
        return 1


    print('\n\n-------------------- Write summary to output file --------------------\n')

    file.write_txt_file(output_file_name=output_file, text=final_summary, append=False)


    print('\n\n-------------------- Delete temp files --------------------\n')

    file.delete_file(temp_file_address)
    file.delete_file(temp_file_token_address)
    file.delete_file(temp_file_features_address)

    return len(sentence_list)


# Preprocess the text file and extract features for the sentences
def preprocessing(*, input_file, temp_file_address, temp_file_token_address, temp_file_features_address):
    print('\n-------------------- Split sentences and get tokens --------------------\n')

    input_text = file.read_txt_file(filename=input_file)
    input_sentences = nltk.sent_tokenize(input_text)
    sentence_split_text, preprocessed_text = '', ''
    sentence_list, sentence_num = [], 0

    for sentence in input_sentences:
        tokenized_sentence = nltk.word_tokenize(sentence)

        if sentence_num > 0:
            sentence_split_text += '\n'
            preprocessed_text += '\n'

        sentence_split_text += sentence
        preprocessed_text += str(tokenized_sentence)
        temp_sentence = Sentence(sentence_num, sentence)
        sentence_list.append(temp_sentence)
        sentence_num += 1

    print('\n-------------------- Prepare text files --------------------\n')

    # Write sentences and tokens
    file.write_txt_file(output_file_name=temp_file_address, text=sentence_split_text, append=False)
    file.write_txt_file(output_file_name=temp_file_token_address, text=preprocessed_text, append=False)


    print('\n-------------------- Feature extraction --------------------\n')

    import os
    os.system(PYTHON_DIRECTORY + ' app/bert/extract_features.py'\
            ' --input_file=' + temp_file_address +' --output_file=' + temp_file_features_address + \
                ' --vocab_file=app/bert/vocab.txt --bert_config_file=app/bert/bert_config.json'\
                    ' --init_checkpoint=app/bert/bert_model.ckpt --layers=-1 --max_seq_length=128 --batch_size=8')


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

    return sentence_list


# K-Center Clustering Algorithm - Algorithm No. 1
def k_center(*, sentence_list, compression_rate, number_of_clusters, distance_num):
    print('\n\n\n-------------------- Algorithm 1 : K-Center Clustering --------------------\n\n\n')

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


# K-Means-Clustering Algorithm - Algorithm No. 2
def k_means(*, sentence_list, compression_rate, number_of_clusters, distance_num):
    print('\n\n\n-------------------- Algorithm 2 : K-Means Clustering --------------------\n\n\n')

    #-------------------- Initialize the initial cluster with random centers
    cluster_list = []
    for i in range(number_of_clusters):
        temp_cluster = Cluster(i)
        temp_cluster.mean = sentence_list[i].representation
        cluster_list.append(temp_cluster)

    # Decalre the distribution table
    distribution, temp_distribution = {}, {}

    #-------------------- Starting clustering algorithm
    for iteration in range(1, 51):
        print('\n\n-------------------- Iteration: ', iteration, '--------------------\n')

        #-------------------- In the beginning of each iteration, clear all clusters
        for cluster in cluster_list:
            cluster.members = []

        #-------------------- Allocate each sentence to a cluster with a lowest distance
        for i in range(len(sentence_list)):
            min_distance, closest_cluster = MAXINT, -1

            for j in range(len(cluster_list)):  # Compute its distance to each cluster means
                temp_distance = sentence_list[i].distance(cluster_list[j].mean, distance_num)
                #print(temp_distance, min_distance)

                if temp_distance < min_distance:
                    closest_cluster, min_distance = j, temp_distance

            cluster_list[closest_cluster].add_member(i)
            temp_distribution[i] = closest_cluster

        #-------------------- For each cluster, compute its new mean
        num = 0
        for cluster in cluster_list:
            cluster.update_mean(sentence_list=sentence_list)
            print(len(cluster.members))
            num += len(cluster.members)
        assert len(sentence_list) == num

        #print(temp_distribution, distribution)

        #-------------------- If the clustering doesn't change, exit the loop
        if distribution == temp_distribution:
            #-------------------- If the clustering is the same as last clustering, exit the loop
            print("\n-------------------- Exit Loop --------------------\n")
            break
        else:
            # Store the clustering for 
            distribution = temp_distribution
            temp_distribution = {}


    print("\n-------------------- Final Summary --------------------\n")
    final_summary = produce_summary_for_clustering(cluster_list=cluster_list, \
        sentence_list=sentence_list, compression_rate=compression_rate, distance_num=distance_num)

    print("\n-------------------- Finished --------------------\n")
    return final_summary


# Bi-K-Means-Clustering Algorithm - Algorithm No. 3
def bi_k_means(*, sentence_list, compression_rate, number_of_clusters, distance_num):
    print('\n\n\n-------------------- Algorithm 3 : Bi-K-Means Clustering --------------------\n\n\n')

    # Initialize the beginning single cluster which contains all sentences
    init_cluster = Cluster(0)
    for i in range(len(sentence_list)):
        init_cluster.add_member(i)
    cluster_list = [init_cluster]

    print("\n-------------------- Enter Loop --------------------\n")
    # Continue when there are less cluster than required
    while len(cluster_list) < number_of_clusters:
        print("\n-------------------- Number of clusters : {} --------------------\n".format(str(len(cluster_list))))
        max_reduce_sse, remove_cluster = MININT, -1
        append_cluster1, append_cluster2 =  Cluster(len(cluster_list)), Cluster(len(cluster_list)+1)

        for cluster in cluster_list:
            # If this cluster can be divided
            if len(cluster.members) >= 2:
                # Compute the current square of sum
                current_sse = cluster.compute_sse(sentence_list=sentence_list, distance_num=distance_num)

                # Attempt binary clustering in the current cluster
                (new_cluster1, new_cluster2) = bi_clustering(cluster=cluster, sentence_list=sentence_list, distance_num=distance_num)

                # Compute the new square of sum
                new_sse = new_cluster1.compute_sse(sentence_list=sentence_list, distance_num=distance_num) + \
                    new_cluster2.compute_sse(sentence_list=sentence_list, distance_num=distance_num)
                
                # If it is able to reduce the sse in a maximum scale, then store this information
                if current_sse - new_sse > max_reduce_sse:
                    max_reduce_sse = current_sse - new_sse
                    remove_cluster = cluster
                    append_cluster1, append_cluster2 = new_cluster1, new_cluster2
            else:
                continue

        # Remove the cluster that can reduce sse of greatest
        cluster_list.remove(remove_cluster)
        # And append the two cluster divided from the original one
        cluster_list.append(append_cluster1)
        cluster_list.append(append_cluster2)

        sentence_num = 0
        for cluster in cluster_list:
            sentence_num += len(cluster.members)
        assert sentence_num==len(sentence_list)

    print("\n-------------------- Final Summary --------------------\n")
    final_summary = produce_summary_for_clustering(cluster_list=cluster_list, \
        sentence_list=sentence_list, compression_rate=compression_rate, distance_num=distance_num)

    print("\n-------------------- Finished --------------------\n")
    return final_summary

# Split one cluster into two cluster using k-means clustering mechanism
def bi_clustering(*, cluster, sentence_list, distance_num):
    if len(cluster.members) < 2:
        return

    sentences = cluster.members
    cluster1, cluster2 = Cluster(1), Cluster(2)
    cluster1.mean = sentence_list[sentences[0]].representation
    cluster2.mean = sentence_list[sentences[1]].representation
    distribution, temp_distribution = {}, {}

    for iteration in range(51):
        print('\n\n-------------------- Bi-Cluster-Iteration: ', iteration, '--------------------\n')
        for sentence in sentences:
            temp_distance1 = sentence_list[sentence].distance(cluster1.mean, distance_num)
            temp_distance2 = sentence_list[sentence].distance(cluster2.mean, distance_num)

            if temp_distance1 < temp_distance2:
                cluster1.add_member(sentence)
                temp_distribution[sentence] = 1
            else:
                cluster2.add_member(sentence)
                temp_distribution[sentence] = 2

        #-------------------- For each cluster, compute its new mean
        cluster1.update_mean(sentence_list=sentence_list)
        cluster2.update_mean(sentence_list=sentence_list)

        #-------------------- If the clustering doesn't change, exit the loop
        if distribution == temp_distribution:
            return (cluster1, cluster2)
        else:
            # Store the clustering for 
            distribution = temp_distribution
            temp_distribution = {}

            cluster1.members = []
            cluster2.members = []




# Single-Agglomerative-Clustering Algorithm - Algorithm No. 4
def single_agglomerative_cluster(*, sentence_list, compression_rate, number_of_clusters, distance_num):
    print('\n\n\n-------------------- Algorithm 4 : Single-Agglomerative-Clustering --------------------\n\n\n')

    # Initialize the initial clusters
    cluster_list = []
    for i in range(len(sentence_list)):
        temp_cluster = Cluster(i)
        temp_cluster.members.append(i)
        cluster_list.append(temp_cluster)

    # Main loop
    while (len(cluster_list) > number_of_clusters):
        print('\n-------------------- Iteration: {} --------------------'.format(str(len(sentence_list) - len(cluster_list) + 1)))

        min_distance = MAXINT
        similar_cluster1, similar_cluster2 = -1, -1

        # Find the two clusters which is most close to each others
        for i in range(0, len(cluster_list) - 1):
            for j in range(i + 1, len(cluster_list)):
                # Computer the minimal distance between two clusters
                temp_distance = cluster_list[i].min_distance(second_cluster=cluster_list[j], \
                    sentence_list=sentence_list, distance_num=distance_num)

                # If this distance is smaller than the stored minimal, mark it as the new minimal
                if temp_distance < min_distance:
                    min_distance = temp_distance
                    similar_cluster1, similar_cluster2 = i, j

        #---------- Merge two most close to each other clusters
        cluster_list[similar_cluster1].members = cluster_list[similar_cluster1].members + cluster_list[similar_cluster2].members
        cluster_list.remove(cluster_list[similar_cluster2])
        print(similar_cluster1, 'and', similar_cluster2, 'merged')
        print('---------- Number of clusters: {} ----------\n'.format(str(len(cluster_list))))

    #----------- Produce final summary
    print("\n-------------------- Final Summary --------------------\n")
    final_summary = produce_summary_for_clustering(cluster_list=cluster_list, \
        sentence_list=sentence_list, compression_rate=compression_rate, distance_num=distance_num)

    print("\n-------------------- Finished --------------------\n")
    return final_summary


# Complete-Agglomerative-Clustering Algorithm - Algorithm No. 5
def complete_agglomerative_cluster(*, sentence_list, compression_rate, number_of_clusters, distance_num):
    print('\n\n\n-------------------- Algorithm 5 : Complete-Agglomerative-Clustering --------------------\n\n\n')

    # Initialize the initial clusters
    cluster_list = []
    for i in range(len(sentence_list)):
        temp_cluster = Cluster(i)
        temp_cluster.members.append(i)
        cluster_list.append(temp_cluster)

    # Main loop
    while (len(cluster_list) > number_of_clusters):
        print('\n-------------------- Iteration: {} --------------------'.format(str(len(sentence_list) - len(cluster_list) + 1)))

        min_distance = MAXINT
        similar_cluster1, similar_cluster2 = -1, -1

        # Find the two clusters which is most close to each others
        for i in range(0, len(cluster_list) - 1):
            for j in range(i + 1, len(cluster_list)):
                # Computer the maximum distance between two clusters
                temp_distance = cluster_list[i].max_distance(second_cluster=cluster_list[j], \
                    sentence_list=sentence_list, distance_num=distance_num)

                # If this distance is smaller than the stored minimal, mark it as the new minimal
                if temp_distance < min_distance:
                    min_distance = temp_distance
                    similar_cluster1, similar_cluster2 = i, j

        #---------- Merge two most close to each other clusters
        cluster_list[similar_cluster1].members = cluster_list[similar_cluster1].members + cluster_list[similar_cluster2].members
        cluster_list.remove(cluster_list[similar_cluster2])
        print(similar_cluster1, 'and', similar_cluster2, 'merged')
        print('---------- Number of clusters: {} ----------\n'.format(str(len(cluster_list))))

    #----------- Produce final summary
    print("\n-------------------- Final Summary --------------------\n")
    final_summary = produce_summary_for_clustering(cluster_list=cluster_list, \
        sentence_list=sentence_list, compression_rate=compression_rate, distance_num=distance_num)

    print("\n-------------------- Finished --------------------\n")
    return final_summary

# UPGMA-Agglomerative-Clustering Algorithm - Algorithm No. 6
def upgma_agglomerative_cluster(*, sentence_list, compression_rate, number_of_clusters, distance_num):
    print('\n\n\n-------------------- Algorithm 6 : UPGMA-Agglomerative-Clustering --------------------\n\n\n')

    # Initialize the initial clusters
    cluster_list = []
    for i in range(len(sentence_list)):
        temp_cluster = Cluster(i)
        temp_cluster.members.append(i)
        cluster_list.append(temp_cluster)

    # Main loop
    while (len(cluster_list) > number_of_clusters):
        print('\n-------------------- Iteration: {} --------------------'.format(str(len(sentence_list) - len(cluster_list) + 1)))

        min_distance = MAXINT
        similar_cluster1, similar_cluster2 = -1, -1

        # Find the two clusters which is most close to each others
        for i in range(0, len(cluster_list) - 1):
            for j in range(i + 1, len(cluster_list)):
                # Computer the average distance between two clusters
                temp_distance = cluster_list[i].avg_distance(second_cluster=cluster_list[j], \
                    sentence_list=sentence_list, distance_num=distance_num)

                # If this distance is smaller than the stored minimal, mark it as the new minimal
                if temp_distance < min_distance:
                    min_distance = temp_distance
                    similar_cluster1, similar_cluster2 = i, j

        #---------- Merge two most close to each other clusters
        cluster_list[similar_cluster1].members = cluster_list[similar_cluster1].members + cluster_list[similar_cluster2].members
        cluster_list.remove(cluster_list[similar_cluster2])
        print(similar_cluster1, 'and', similar_cluster2, 'merged')
        print('---------- Number of clusters: {} ----------\n'.format(str(len(cluster_list))))

    #----------- Produce final summary
    print("\n-------------------- Final Summary --------------------\n")
    final_summary = produce_summary_for_clustering(cluster_list=cluster_list, \
        sentence_list=sentence_list, compression_rate=compression_rate, distance_num=distance_num)

    print("\n-------------------- Finished --------------------\n")
    return final_summary


# DBSCAN-Clustering Algorithm - Algorithm No. 7
def dbscan_clustering(*, sentence_list, compression_rate):
    print('\n\n\n-------------------- Algorithm 7 : DBSCAN-Clustering Algorithm --------------------\n\n\n')

    print("\n-------------------- Initialize Matrix --------------------\n")
    Matrix = []
    for sentence in sentence_list:
        Matrix.append(sentence.representation)

    print("-------------------- Number of sentences : {}--------------------\n".format(str(len(Matrix))))


    print("\n-------------------- Perform clustering --------------------\n")
    clustering = DBSCAN(eps=0.05, min_samples=2, metric='cosine').fit(np.array(Matrix))

    labels = list(clustering.labels_)
    print(labels)
    print("\n-------------------- Number of labels : {}--------------------\n".format(str(max(labels) + 1)))


    print("\n-------------------- Get Clustering Result --------------------\n")
    cluster_list = []
    for i in range(max(labels) + 1):
        cluster_list.append(Cluster(i))

    for i in range(len(labels)):
        if labels[i] != -1:
            cluster_list[labels[i]].add_member(i)

    print("Clustering :  ", end = '')
    for cluster in cluster_list:
        print(len(cluster.members), end = '   ')
    print("\n")


    print("\n-------------------- Final Summary --------------------\n")
    final_summary = produce_summary_for_clustering(cluster_list=cluster_list, \
        sentence_list=sentence_list, compression_rate=compression_rate, distance_num=3)


    print("\n-------------------- Finished --------------------\n")
    return final_summary


# OPTICS-Clustering Algorithm - Algorithm No. 8
def optics_clustering(*, sentence_list, compression_rate, distance_num):
    print('\n\n\n-------------------- Algorithm 8 : OPTICS-Clustering Algorithm --------------------\n\n\n')

    print("\n-------------------- Initialize Matrix --------------------\n")
    Matrix = []
    for sentence in sentence_list:
        Matrix.append(sentence.representation)

    print("-------------------- Number of sentences : {}--------------------\n".format(str(len(Matrix))))


    print("\n-------------------- Perform clustering --------------------\n")
    if distance_num == 1:
        clustering = OPTICS(max_eps=MAXINT, min_samples=2, metric='euclidean').fit(Matrix)
    elif distance_num == 2:
        clustering = OPTICS(max_eps=MAXINT, min_samples=2, metric='manhattan').fit(Matrix)
    elif distance_num == 3:
        clustering = OPTICS(max_eps=MAXINT, min_samples=2, metric='cosine').fit(Matrix)
    else:
        print('\n\nException : Unknown Distance Method. Please reset the distance num.\n\n')

    labels = list(clustering.labels_)
    print(labels)
    print("-------------------- Number of labels : {} --------------------\n".format(str(max(labels) + 1)))


    print("\n-------------------- Get Clustering Result --------------------\n")
    cluster_list = []
    for i in range(max(labels) + 1):
        cluster_list.append(Cluster(i))

    for i in range(len(labels)):
        if labels[i] != -1:
            cluster_list[labels[i]].add_member(i)

    print("Clustering :  ", end = '')
    for cluster in cluster_list:
        print(len(cluster.members), end = '   ')
    print("\n")

    print("-------------------- Number of clusters : {} --------------------\n".format(str(len(cluster_list))))


    print("\n-------------------- Final Summary --------------------\n")
    final_summary = produce_summary_for_clustering(cluster_list=cluster_list, \
        sentence_list=sentence_list, compression_rate=compression_rate, distance_num=distance_num)


    print("\n-------------------- Finished --------------------\n")
    return final_summary



# Means-Shift-Clustering Algorithm - Algorithm No. 9
def mean_shift_clustering(*, sentence_list, compression_rate):
    print('\n\n\n-------------------- Algorithm 9 : Mean-Shift-Clustering Algorithm --------------------\n\n\n')

    print("\n-------------------- Initialize Matrix --------------------\n")
    Matrix = []
    for sentence in sentence_list:
        Matrix.append(sentence.representation)
    print("-------------------- Number of sentences : {}--------------------\n".format(str(len(Matrix))))

    print("\n-------------------- Perform clustering --------------------\n")
    clustering = MeanShift().fit(Matrix)
    labels = list(clustering.labels_)
    print(labels)
    print("-------------------- Number of clusters : {}--------------------\n".format(str(max(labels))))

    print("\n-------------------- Get Clustering Result --------------------\n")
    cluster_list = []
    for i in range(max(labels) + 1):
        cluster_list.append(Cluster(i))

    for i in range(len(labels)):
        cluster_list[labels[i]].add_member(i)

    print("-------------------- Number of clusters : {}--------------------\n".format(str(len(cluster_list))))

    print("\n-------------------- Final Summary --------------------\n")
    final_summary = produce_summary_for_clustering(cluster_list=cluster_list, \
        sentence_list=sentence_list, compression_rate=compression_rate, distance_num=1)

    print("\n-------------------- Finished --------------------\n")
    return final_summary



# Select sentences in clustering algorithms and produce a final summary
def produce_summary_for_clustering(*, cluster_list, sentence_list, compression_rate, distance_num):
    print("\n\n-------------------- Produce the final summary --------------------\n\n")

    selected_sentences = [] #select the top sentences in each cluster
    distance_dict = {}

    for cluster in cluster_list:
        # Compute the mean of the cluster
        cluster.update_mean(sentence_list)

        for i in cluster.members: # i is the no of sentences in sentence_list
            distance_dict[i] = sentence_list[i].distance(cluster.mean, distance_num)
            #print(distance_dict[i])

    # Sort the sentences according to their distance to center
    sorted_list = sorted(distance_dict.items(), key = lambda item:item[1])
    #print('Sorted similiarity dict : ', sorted_list)

    # Calculate the number of sentences to be selected in this cluster
    num_sentence_selected = int(len(sentence_list)*compression_rate)
    print('Number of sentence selected : ', num_sentence_selected, '\n')

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




# TextRank / PageRank Algorithm - Algorithm No. 10
def text_rank(*, sentence_list, compression_rate):
    print('\n\n\n-------------------- Algorithm 10 : Text-Rank Algorithm --------------------\n\n\n')

    # Initialize the similarity matrix
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
    for i in range(int(len(sentence_list)*compression_rate) + 1):
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