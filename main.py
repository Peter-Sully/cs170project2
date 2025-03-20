#Needed for inf
import math
#Needed for data loading/handling
import numpy as np
#Used to time runs
import timeit

def load_data(file):
    data = np.loadtxt(file)
    return data

def leave_one_out_cross_val(data, current_set, feature_to_add):
    number_correctly_classified = 0
    # Construct the features list correctly
    features = current_set.copy()
    if feature_to_add is not None:
        features.append(feature_to_add)
    
    for i in range(len(data)):
        object_to_classify = [data[i][j] for j in features]
        label_object_to_classify = data[i][0]

        nearest_neighbor_distance = float("inf")
        nearest_neighbor_location = None
        for k in range(len(data)):
            if k != i:
                neighbor_features = [data[k][j] for j in features]
                # Calculate Euclidean distance
                distance = math.sqrt(sum((p1 - p2) ** 2 for p1, p2 in zip(object_to_classify, neighbor_features)))
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
    #number of features (number of columns, minus 1 for class label)
    num_features = len(data[0])-1
    best_overall_accuracy = 0
    best_overall_set = []
    print("Beginning search.")
    for i in range(num_features):
        best_so_far = float("-inf")
        feature_to_add_at_this_level = None
        for k in range(1, num_features + 1):
            if k not in current_set:
                accuracy = leave_one_out_cross_val(data, current_set, k)
                print(f"Using feature(s) {{{', '.join(map(str, current_set + [k]))}}} accuracy is {accuracy * 100:.1f}%")

                if accuracy > best_so_far:
                    best_so_far = accuracy
                    feature_to_add_at_this_level = k
        if feature_to_add_at_this_level is not None:
            current_set.append(feature_to_add_at_this_level)
            print(f"Feature set {{{', '.join(map(str, current_set))}}} was best, accuracy is {best_so_far * 100:.1f}%")

            if best_so_far > best_overall_accuracy:
                best_overall_accuracy = best_so_far
                best_overall_set = current_set[:]

    print(f"\nFinished search!! The best feature subset is {{{', '.join(map(str, best_overall_set))}}}, which has an accuracy of {best_overall_accuracy * 100:.1f}%")

def backward_search(data):
    current_set = list(range(1, len(data[0])))  
    num_features = len(current_set)
    best_overall_accuracy = 0
    best_overall_set = current_set[:]

    print("\nBeginning search.")
    for i in range(num_features - 1):
        best_so_far = float("-inf")
        feature_to_remove_at_this_level = None
        
        for k in current_set:
            temp_set = current_set[:]
            temp_set.remove(k)

            accuracy = leave_one_out_cross_val(data, temp_set, None)
            print(f"Using feature(s) {{{', '.join(map(str, temp_set))}}} accuracy is {accuracy * 100:.1f}%")

            if accuracy > best_so_far:
                best_so_far = accuracy
                feature_to_remove_at_this_level = k
        
        if feature_to_remove_at_this_level is not None:
            current_set.remove(feature_to_remove_at_this_level)
            print(f"Feature set {{{', '.join(map(str, current_set))}}} was best, accuracy is {best_so_far * 100:.1f}%")
            if best_so_far > best_overall_accuracy:
                best_overall_accuracy = best_so_far
                best_overall_set = current_set[:]

    print(f"\nFinished search!! The best feature subset is {{{', '.join(map(str, best_overall_set))}}}, which has an accuracy of {best_overall_accuracy * 100:.1f}%")


def main():
    print("Welcome to Peter Sullivan's Feature Selection Algorithm.")
    file_name = input("Type in the name of the file to test: ")
    data = load_data(file_name)
    alg = input("Type in the number of the algorithm you want to run. \n\t1) Forward Selection\n\t2) Backward Elimination\n")
    if(alg != "1" and alg != "2"):
        print("Invalid algorithm choice. Exiting...")
        exit()
    num_features = len(data[0]) - 1
    num_instances = len(data)
    print(f"This dataset has {num_features} features (not including the class attribute), with {num_instances} instances")

    accuracy_all_features = leave_one_out_cross_val(data, list(range(1, num_features + 1)), None)
    print(f'Running nearest neighbor with all {num_features}, using "leaving-one-out" evaluation, I get an accuracy of {accuracy_all_features*100:.1f}%')

    if alg == "1":
        start_time = timeit.default_timer()
        feature_search(data)
        end_time = timeit.default_timer()
        print(f"Forward Selection took {end_time - start_time:.2f} seconds to complete.")
    elif alg == "2":
        start_time = timeit.default_timer()
        backward_search(data)
        end_time = timeit.default_timer()
        print(f"Backward Elimination took {end_time - start_time:.2f} seconds to complete.")
main()