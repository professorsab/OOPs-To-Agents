class Agent:
    def __init__(self):
        self.attractions=[]
        self.querylist = []
        self.prefrence = None

    def Believe(self):
        query = input("Enter your query ")
        self.querylist = query.split()
        

        self.Desires()
    
    def Desires(self):
        

        for i in range(len(self.querylist)):
            if self.querylist[i] == "sunshine" or self.querylist[i] == "sunny" or self.querylist[i] == "sunny." or self.querylist[i] == "sunshine."  :
                self.prefrence = "sunny"
                break
            elif self.querylist[i]=="rainy" or self.querylist[i]=="rains":
                self.prefrence="rainy"
                break


        if self.prefrence is None:
         self.prefrence = "unknown"
        self.Intends()

    def Intends(self):
        self.tool()

        

    def tool(self):
        if self.prefrence == "sunny":
            self.attractions=["Daman-e-Koh ","Margalla Hills", "Saidpur Village"]
        elif self.prefrence=="rainy":
            self.attractions=["Centaurus Mall ","Safa Gold Mall ","Indoor Bowling (F9)"]

        else:
            self.attractions=["Please specify the intention in the query as Sunny or Rainy"]


    def Display(self):
        print(f"the user specified weather is : {self.prefrence.capitalize()}")
        print (f"The following are the Places to visit in a {self.prefrence} Weather: ")
        for item in self.attractions:
            print(f"* {item}")



        


agent = Agent()
agent.Believe()
agent.Display()

 