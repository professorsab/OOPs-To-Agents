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



vect1=[2,2,-1]
vect2=[5,-3,2]

result=calculate_dot_product(vect1,vect2)
print(result)

print(calculate_magnitude(vect1))
result=print (calculate_cosine_similarity(vect1,vect2))
print(result)