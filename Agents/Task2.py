class Agent:
    def __init__(self):
        self.weather_details = {}
        self.attractions = []
        self.time_estimates = []
        self.jasonquery = {}

    def weather_tool(self, location):  # Fixed: proper indentation (4 spaces)
        if location.lower() == "paris":
            return {"condition": "rainy", "temp": 14}
        elif location.lower() == "barcelona":
            return {"condition": "sunny", "temp": 22}
        elif location.lower() == "islamabad":
            return {"condition": "rainy", "temp": 20}
        else:
            return {"condition": "unknown", "temp": 0}

    def attractions_tool(self, location):  # Fixed: proper indentation (4 spaces)
        if location == "Barcelona":
            return ["Sagrada Familia", "Park Güell"]
        elif location == "Islamabad":
            return ["Margalla Hills", "Faisal Masjid"]

    def time_estimator(self, activity):  # Fixed: proper indentation (4 spaces)
        if activity == "Sagrada Familia":
            return {"activity": "Sagrada Familia", "time": "2 hours", "type": "indoor"}
        elif activity == "Park Güell":
            return {"activity": "Park Güell", "time": "3 hours", "type": "outdoor"}
        elif activity == "Margalla Hills":
            return {"activity": "Margalla Hills", "time": "5 hours", "type": "outdoor"}
        elif activity == "Faisal Masjid":
            return {"activity": "Faisal Masjid", "time": "3 hours", "type": "indoor"}
        else:
            return {"activity": activity, "time": "unknown", "type": "unknown"}

    def orient(self, query):  # Fixed: proper indentation (4 spaces)
        search_string = "if it rains"
        if search_string in query:
            return 1
        else:
            return 0

    def decide(self):
        weather_condition = self.weather_details["condition"]
        indoor_only = self.jasonquery["indoor_only"]
        selected_activities = []

        for activity in self.attractions:
            info = self.time_estimator(activity)
            if indoor_only == 1 or weather_condition == "rainy":
                if info["type"] == "indoor":
                    selected_activities.append(info)
            else:
                selected_activities.append(info)

        self.time_estimates = selected_activities

    def observe(self):
        query = input("Enter your query ")
        querylist = query.split()
        location = ""

        for i in range(len(querylist)):
            if querylist[i] == "in" or querylist[i] == "for" or querylist[i] == "at":
                location = querylist[i + 1].capitalize()
                break

        self.jasonquery = {
            "location": location,
            "intent": "itinerary",
            "indoor_only": self.orient(query)
        }

    def act(self):
        self.weather_details = self.weather_tool(self.jasonquery["location"])
        self.attractions = self.attractions_tool(self.jasonquery["location"])
        self.decide()

    def goal(self):
        print("Location:", self.jasonquery["location"])
        print("Weather:", self.weather_details)
        print("Itinerary:")
        for item in self.time_estimates:
            print("-", item["activity"], "(", item["time"], ",", item["type"], ")")

agent = Agent()
agent.observe()
agent.act()
agent.goal()
