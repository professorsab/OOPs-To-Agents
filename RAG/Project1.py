import math as m

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


def index_documents (texts,vector_store_instance,embedding_fuction):
    
    for idx, chunk in enumerate(texts, 1):
        embedding=embedding_fuction(chunk)
        vector_store_instance.add_document(idx,chunk,embedding)


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



FileName=input("please Input the file name you want to extract the data from.\n")

with open(FileName, 'r', encoding='latin-1') as file:
    long_text  = file.read()
    
chunks = load_and_split_text(long_text, 100)
s=SimpleVectorStore()
embedding=[]
query=None
index_documents(chunks,s,create_mock_embedding)
print("Indexing document... Done.")
while (query!="exit"):
    
  query=input("Ask me a question (type 'exit' to quit):\n")
  k = int(input("Please Input how many related answers you want\n"))
  
  
  embedding=create_mock_embedding(query)
  top_match=s.retrieve_top_k(embedding,k)
  
  response=run_rag_pipeline(query,s,create_mock_embedding,mock_llm_response,2)
  
  print("the llm respose is as follows:\n\n")
  print(response)
  
  for doc_id, text, embedding in top_match:
      print(f"ID: {doc_id}  Text: {text[:]}  Embedding: {embedding}\n\n")
      
  query=input("press Exit to close or pass to continue")