import numpy as np

def NormalizeData(numbers):
    
    if not numbers:
        return []  
    
    min_val = min(numbers)
    max_val = max(numbers)
    
    
    if min_val == max_val:
        return [0.5] * len(numbers)  
    
    normalized = [(x - min_val) / (max_val - min_val) for x in numbers]
    return normalized

def create_mock_embedding(string):
    
 array=[ord(char) for char in string]


#  for x1 in array:
#      print(x1)
    
 l=len(array)
 iter = l-3

 if l > 3:
     for i in range(iter):
        array[i] += array[i + 3]
     array = array[:3]  
     array = NormalizeData(array)
     return array
 else:
    array = NormalizeData(array)
    return array
      







print("Embedding 1", create_mock_embedding("The cat sat on the mat."))
print("Embedding 2",create_mock_embedding("The dog barked loudly."))
print("Embedding 3",create_mock_embedding("A small feline rested on a rug."))
print("Embedding 4",create_mock_embedding("A small feline rested on a rug."))