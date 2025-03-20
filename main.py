import math
import numpy as np

def load_data(file):
    data = np.loadtxt(file)
    return data

def leave_one_out_cross_val(data, current_set, feature_to_add):
    number_correctly_classified = 0
    for i in range(len(data)):
        object_to_classify = data[i][1:]
        label_object_to_classify = data[i][0]

        nearest_neighbor_distance = float("inf")
        nearest_neighbor_location = float("inf")
        for k in range(len(data)):
            if k != i:
                distance = math.sqrt(sum((p1 - p2) ** 2 for p1, p2 in zip(object_to_classify, data[k][1:])))
                if distance < nearest_neighbor_distance:
                    nearest_neighbor_distance = distance
                    nearest_neighbor_location = k
                    nearest_neighbor_label = data[nearest_neighbor_location][0]
        if label_object_to_classify == nearest_neighbor_label:
            number_correctly_classified += 1
    accuracy = number_correctly_classified / len(data)
    return accuracy



def feature_search(data):
    current_set = []
    for i in range(len(data)):
        print(f"On the {i+1}th level of the search tree")
        best_so_far = float("-inf")
        feature_to_add_at_this_level = None
        for k in range(len(data)):
            if k not in current_set:
                print(f"--Considering adding the {k+1}th feature")
                accuracy = leave_one_out_cross_val(data, current_set, k)

                if accuracy > best_so_far:
                    best_so_far = accuracy
                    feature_to_add_at_this_level = k
        current_set.append(feature_to_add_at_this_level) 
        print(f"On level {i+1} added feature {feature_to_add_at_this_level+1} to current set")
                
data = [1,2,3,4]
feature_search(data)