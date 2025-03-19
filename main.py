import random
def leave_one_out_cross_val(data, current_set, feature_to_add):
    accuracy = random.randint(1,100)
    return accuracy

def feature_search(data):
    current_set = []
    for i in range(len(data)):
        print(f"On the {i+1}th level of the search tree")
        best_so_far = 0
        for k in range(len(data)):
            if k not in current_set:
                print(f"--Considering adding the {k+1}th feature")
                accuracy = leave_one_out_cross_val(data, current_set, k+1)

                if accuracy > best_so_far:
                    best_so_far = accuracy
                    feature_to_add_at_this_level = k
        current_set.append(feature_to_add_at_this_level) 
        print(f"On level {i+1} added feature {feature_to_add_at_this_level+1} to current set")
                
data = [1,2,3,4]
feature_search(data)