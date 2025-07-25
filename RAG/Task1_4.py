class SimpleVectorStore:
    def __init__(self):
        self.documents=[]
        
    def add_document(self,document_id,text,embedding):
        self.documents.append((document_id,text,embedding))
    
    def get_all_embeddings(self):
        return self.documents
    
    def get_document_by_id(self,document_id):
        for id in self.documents:
            if id[0]==document_id:
                return id[1]
        return None
            
            
        
        
        
        
    
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
    
 array=[ord(char) for char in str(string)]


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

object=SimpleVectorStore()

string1="The cat sat on the mat."
string2="The dog barked loudly."
string3="Animals are crazy"
string4="A small feline rested on a rug."
string5="Pakistan got independance on 14th august 1947"
embedding1= create_mock_embedding(string1)
embedding2=create_mock_embedding(string2)
embedding3=create_mock_embedding(string3)
embedding4=create_mock_embedding(string4)
embedding5=create_mock_embedding(string5)       

object.add_document(1001,string1,embedding1)
object.add_document(1002,string2,embedding2)
object.add_document(1003,string3,embedding3)
object.add_document(1004,string4,embedding4)
object.add_document(1005,string5,embedding5)

 
        
        