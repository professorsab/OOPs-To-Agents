
class Agent:
    def __init__(self):
        self.weather_details={}
        self.packing_details={}
        self.jasonquery={}

    def weather_tool(self,location):
        if (location=="paris"):
            return {"condition": "rainy", "temp": 14} 
        else:
            return ["error"]
    
    def packing_advisor(self,weather_conditions):
        if (weather_conditions=="rainy"):
            return ["umbrella", "jacket"] 
        else :
            return ["error"]
    
    
    
    
    
    
    
    
    def precieve(self):
        query=input("Enter your query: ")
        querylist=query.split()
        intent={}
        self.jasonquery={"location": "paris","intent": "Null"}
        for words in querylist:
            if words in ["pack", "packing", "bring", "carry"]:
                self.jasonquery["intent"]="packing"
    
        self.Think()
    
            
    
  
    def Think(self):
        self.weather_details=self.weather_tool(self.jasonquery["location"])
        if (self.jasonquery["intent"]=="packing"):
            self.packing_details=self.packing_advisor(self.weather_details["condition"])


    def goal(self):
        
        print(f"Location: {self.jasonquery['location']}")
        print(f"weather : {self.weather_details}")
        print(f"Packing : {self.packing_details}")





    
  

agent=Agent()
agent.precieve()
agent.goal()

















