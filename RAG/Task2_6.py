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


import math as m

def calculate_dot_product(vec1, vec2):
    result=(vec1[0]*vec2[0])+(vec1[1]*vec2[1])+(vec1[2]*vec2[2])
    return result

def calculate_magnitude(vec):
    result=vec[0]**2+vec[1]**2+vec[2]**2
    result =m.sqrt(result)
    return result

def calculate_cosine_similarity(vec1, vec2):
     dot_product=calculate_dot_product(vec1,vec2)
     magnitude1=calculate_magnitude(vec1)
     magnitude2=calculate_magnitude(vec2)
     result=(dot_product) / (magnitude1 * magnitude2)
     return result
     
    
    

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
    
    def retrieve_top_k(self, query_embedding, k=1):
     similarities=[]
     for doc_id, text,embedding in self.get_all_embeddings():
         similarity=(calculate_cosine_similarity(query_embedding,embedding))
         similarities.append((doc_id, text, similarity))
         
     similarities.sort(key=lambda x: x[2], reverse=True)
        
     return similarities[:k]
     
     
   
       
       
def load_and_split_text(long_text, chunk_size=50):
    result = [] 
    if chunk_size < 1:
        print("chunk size cannot be less than 1")
        return result
    
    while long_text:
        length = len(long_text)
        if length <= chunk_size:
            result.append(long_text)
            break
            
        if chunk_size < length and long_text[chunk_size] in [" ", "."]:
            result.append(long_text[:chunk_size])
            long_text = long_text[chunk_size:].lstrip()
        else:
            i = min(chunk_size, length - 1)
            while i < length:
                if long_text[i] in [" ", "."]:
                    result.append(long_text[:i])
                    long_text = long_text[i+1:].lstrip()
                    break
                i += 1
            else:
                result.append(long_text[:chunk_size])
                long_text = long_text[chunk_size:]
    
    return result

def augment_prompt(query, retrieved_texts):
    prompt = f"Find information about '{query}' in these documents: {retrieved_texts}"
    return prompt

def mock_llm_response(prompt):
    response = "Here's what I found about your question in the documents."
    return response

def run_rag_pipeline(query, vector_store, embedding_func, mock_llm_func, k=1):
   embedding=embedding_func(query)
   similar_docs=vector_store.retrieve_top_k(embedding,k)
   doc_texts=[text for _,text,_ in similar_docs]
   
   prompt=augment_prompt(query,doc_texts)
   response=mock_llm_func(prompt)
   
   return response
   

def index_documents (texts,vector_store_instance,embedding_fuction):
    
    for idx, chunk in enumerate(texts, 1):
        embedding=embedding_fuction(chunk)
        vector_store_instance.add_document(idx,chunk,embedding)
     
    
long_text = "The history of computers dates back to the 1800s with Charles Babbage's Analytical Engine, the first mechanical computer. In the 1930s, Alan Turing proposed the concept of a universal machine. The first electronic computers emerged in the 1940s, including ENIAC which filled entire rooms. The 1950s saw transistor-based computers replacing vacuum tubes, making them smaller and more reliable. Integrated circuits in the 1960s led to mainframe computers used by businesses and universities. The personal computer revolution began in the 1970s with machines like the Altair 8800 and Apple I. The 1980s brought graphical user interfaces and the IBM PC, while the 1990s saw the rise of the Internet and mobile computing. Today's smartphones are millions of times more powerful than early computers that occupied whole buildings. Quantum computing now represents the next frontier in computational technology."

chunks = load_and_split_text(long_text, 100)
s=SimpleVectorStore()
embedding=[]
index_documents(chunks,s,create_mock_embedding)

# print("Stored documents:")
# for doc_id, text, embedding in s.get_all_embeddings():
#     print(f"ID: {doc_id}  Text: {text[:]}  Embedding: {embedding}")
    
    
query="When was the first computer invented?"
embedding=create_mock_embedding(query)
top_match=s.retrieve_top_k(embedding,2)

# for doc_id, text, embedding in top_match:
#     print(f"ID: {doc_id}  Text: {text[:]}  Embedding: {embedding}")
    
    
response=run_rag_pipeline(query,s,create_mock_embedding,mock_llm_response,2)

print("the llm respose is as follows:")
print(response)

for doc_id, text, embedding in top_match:
    print(f"ID: {doc_id}  Text: {text[:]}  Embedding: {embedding}")
    

