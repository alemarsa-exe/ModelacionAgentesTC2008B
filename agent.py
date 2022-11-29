from mesa import Agent
import numpy as np
import random


class GrassAgent(Agent):
    def __init__(self,id, x, y, model):
        super().__init__(id, model)
        self.id = id
        self.model = model
        self.coords = x,y
        self.desc = "Grass"
    def step(self):
        return
    def advance(self):
        return
        
class RoadAgent(Agent):
    def __init__(self,id, x, y, model):
        super().__init__(id, model)
        self.id = id
        self.coords = x,y
        self.model = model
        self.desc = "Road"
    def step(self):
        return
    def advance(self):
        return

class TrafficLightAgent(Agent):
    def __init__(self,id, x, y, direction, model):
        super().__init__(id, model)
        self.id = id
        self.coords = x,y
        self.model = model
        self.direction = direction
        self.state = "Yellow"
        self.desc = "TrafficLight"
        self.dist = 1000
        self.mirror = None
    def step(self):

        if self.mirror is not None:
            mirrorLight = self.model.grid.get_cell_list_contents(self.mirror)
            for agent in mirrorLight:
                if type(agent) == TrafficLightAgent:
                    self.state = agent.state
                    self.dist = agent.dist
        else: 
            self.dist=1000
            if self.direction == 0:

                cellList = self.model.grid.get_cell_list_contents([(self.coords[0]+1, self.coords[1]),(self.coords[0]+2, self.coords[1]),(self.coords[0]+1, self.coords[1]+1),(self.coords[0]+2, self.coords[1]+1)])
                for agent in cellList:
                    newCoords = agent.coords
                    aux = newCoords[0] - 1
                    newCoords = aux, newCoords[1]
                    dist = newCoords[0] - self.coords[0] - 1
                    self.dist = dist

            if self.direction == 1:
                cellList = self.model.grid.get_cell_list_contents([(self.coords[0], self.coords[1]-1),(self.coords[0], self.coords[1]-2),(self.coords[0]+1, self.coords[1]-1),(self.coords[0]+1, self.coords[1]-2)])
                for agent in cellList:
                    newCoords = agent.coords
                    aux = newCoords[1] + 1
                    newCoords = newCoords[0], aux
                    dist = self.coords[1] - newCoords[1] - 1
                    self.dist = dist
            
            if self.direction == 2:
                cellList = self.model.grid.get_cell_list_contents([(self.coords[0]-1, self.coords[1]),(self.coords[0]-2, self.coords[1]),(self.coords[0]-1, self.coords[1]-1),(self.coords[0]-2, self.coords[1]-1)])
                for agent in cellList:
                    newCoords = agent.coords
                    aux = newCoords[0] + 1
                    newCoords = aux, newCoords[1]
                    dist = self.coords[0] - newCoords[0] - 1
                    self.dist = dist

            if self.direction == 3:
                cellList = self.model.grid.get_cell_list_contents([(self.coords[0], self.coords[1]+1),(self.coords[0], self.coords[1]+2),(self.coords[0]-1, self.coords[1]+1),(self.coords[0]-1, self.coords[1]+2)])
                for agent in cellList:
                    newCoords = agent.coords
                    aux = newCoords[1] - 1
                    newCoords = newCoords[0], aux
                    dist = newCoords[1] - self.coords[1] - 1
                    print("3: ", dist)
                    self.dist = dist
            
            allLightsList = [(2,4), (7,5), (4,7), (5,2)]

            allLights = self.model.grid.get_cell_list_contents(allLightsList)
            lowestDist = 1000
            agentLowestDist = None
            for agent in allLights:
                if type(agent) == TrafficLightAgent:
                    if agent.dist < lowestDist:
                        agentLowestDist = agent
                        
            if agentLowestDist is not None:
                checkRoad = False


                RoadCellsList2 = [(3,3),(3,4),(3,5),(3,6), (4,3),(4,4),(4,5),(4,6), (5,3),(5,4),(5,5),(5,6), (6,3),(6,4),(6,5),(6,6), (2,4), (7,5), (4,7), (5,2),(2,3),(3,7),(7,6),(6,2)]

                RoadCells = self.model.grid.get_cell_list_contents(RoadCellsList2)
                for agent in RoadCells:
                    if type(agent) == CarAgent:
                        checkRoad = True


                if checkRoad == False:
                    agentLowestDist.state = "Green"

                if agentLowestDist.direction == 0:

                    oppositeLights = self.model.grid.get_cell_list_contents([(5,2), (4,7)])
                    for agent in oppositeLights:
                        if agentLowestDist.state == "Green":
                            agent.state = "Red"
                        elif agentLowestDist.state == "Red":
                            agent.state = "Green"
                    sameLight = self.model.grid.get_cell_list_contents([(2,4)])
                    for agent in sameLight:
                        agent.state = agentLowestDist.state

                elif agentLowestDist.direction == 1:
                    oppositeLights = self.model.grid.get_cell_list_contents([(2,4), (7,5)])
                    for agent in oppositeLights:
                        if agentLowestDist.state == "Green":
                            agent.state = "Red"
                        elif agentLowestDist.state == "Red":
                            agent.state = "Green"
                    sameLight = self.model.grid.get_cell_list_contents([(4,7)])
                    for agent in sameLight:
                        agent.state = agentLowestDist.state
                
                elif agentLowestDist.direction == 2:

                    oppositeLights = self.model.grid.get_cell_list_contents([(5,2), (4,7)])
                    for agent in oppositeLights:
                        if agentLowestDist.state == "Green":
                            agent.state = "Red"
                        elif agentLowestDist.state == "Red":
                            agent.state = "Green"
                    sameLight = self.model.grid.get_cell_list_contents([(7,5)])
                    for agent in sameLight:
                        agent.state = agentLowestDist.state
                
                elif agentLowestDist.direction == 3:
                    oppositeLights = self.model.grid.get_cell_list_contents([(2,4), (7,5)])
                    for agent in oppositeLights:
                        if agentLowestDist.state == "Green":
                            agent.state = "Red"
                        elif agentLowestDist.state == "Red":
                            agent.state = "Green"
                    sameLight = self.model.grid.get_cell_list_contents([(5,2)])
                    for agent in sameLight:
                        agent.state = agentLowestDist.state
            
            
            return

    def advance(self):
        return

class CarAgent(Agent):
    def __init__(self,id, x, y, direction, model):
        super().__init__(id, model)
        self.id = id
        self.coords = x,y
        self.z = 3
        self.model = model
        self.speed = np.random.choice(np.arange(1, 4), p=[0.3, 0.4, 0.3])
        self.next_pos = None
        self.direction = direction
        self.desc = "Car"
    def step(self):

        crash = self.model.grid.get_cell_list_contents([self.coords])

        for agent in crash:
            if ((type(agent) is CarAgent or type(agent) is CarAgentDifferentA or type(agent) is CarAgentDifferentB or type(agent) is CarAgentDifferentC) and agent.id != self.id):
                self.model.kill_agents.append(agent)
                return

        if self.direction == 0:
            #Change
            if self.coords == (8,4):
                self.next_pos = self.coords[0], self.coords[1]+1
                self.direction = 2
                return 
            lightCheck = ""
            if self.coords[0] != 9:
                checkLight = self.model.grid.get_cell_list_contents([(self.coords[0]+1,self.coords[1])])
                for agent in checkLight:
                    if type(agent) == TrafficLightAgent:
                        lightCheck = agent.state
                    #Change
                    elif type(agent) == GrassAgent:
                        self.direction = 3
                        return
            if lightCheck == "Green" or lightCheck == "":
                if(self.coords[0] < 9):
                    if self.model.time % self.speed == 0:
                        self.next_pos = self.coords[0]+1, self.coords[1]
                else:
                    #Change
                    self.next_pos = self.coords[0], self.coords[1]+1
                    self.direction = 3

        elif self.direction == 1:
            #Change
            if self.coords == (4,1):
                self.next_pos = self.coords[0]+1, self.coords[1]
                self.direction = 3
                return 
            lightCheck = ""
            if self.coords[1] != 0:
                checkLight = self.model.grid.get_cell_list_contents([(self.coords[0],self.coords[1]-1)])
                for agent in checkLight:
                    if type(agent) == TrafficLightAgent:
                        lightCheck = agent.state
                    #Change
                    elif type(agent) == GrassAgent:
                        self.direction = 0
                        return
            if lightCheck == "Green" or lightCheck == "":
                if(self.coords[1] > 0):
                    if self.model.time % self.speed == 0:
                        self.next_pos = self.coords[0], self.coords[1]-1
                else:
                    self.next_pos = self.coords[0]+1, self.coords[1]
                    self.direction = 0

        elif self.direction == 2:
            #Change
            if self.coords == (1,5):
                self.next_pos = self.coords[0], self.coords[1]-1
                self.direction = 0
                return 
            lightCheck = ""
            if self.coords[0] != 0:
                checkLight = self.model.grid.get_cell_list_contents([(self.coords[0]-1,self.coords[1])])
                for agent in checkLight:
                    if type(agent) == TrafficLightAgent:
                        lightCheck = agent.state
                    #Change
                    elif type(agent) == GrassAgent:
                        self.direction = 1
                        return
            if lightCheck == "Green" or lightCheck == "":
                if(self.coords[0] > 0):
                    if self.model.time % self.speed == 0:
                        self.next_pos = self.coords[0]-1, self.coords[1]
                else:
                    self.next_pos = self.coords[0], self.coords[1]-1
                    self.direction = 1

        elif self.direction == 3:
            #Change
            if self.coords == (5,8):
                self.next_pos = self.coords[0]-1, self.coords[1]
                self.direction = 1
                return 
            lightCheck = ""
            if self.coords[1] != 9:
                checkLight = self.model.grid.get_cell_list_contents([(self.coords[0],self.coords[1]+1)])
                for agent in checkLight:
                    if type(agent) == TrafficLightAgent:
                        lightCheck = agent.state
                    #Change
                    elif type(agent) == GrassAgent:
                        self.direction = 2
                        return
            if lightCheck == "Green" or lightCheck == "":
                if(self.coords[1] < 9):
                    if self.model.time % self.speed == 0:
                        self.next_pos = self.coords[0], self.coords[1]+1
                else:
                    self.next_pos = self.coords[0]-1, self.coords[1]
                    self.direction = 2
    def advance(self):
        if self.next_pos is not None:
            self.coords = self.next_pos
            self.model.grid.move_agent(self,self.coords)

class CarAgentDifferentA(Agent):
    def __init__(self,id, x, y, direction, model):
        super().__init__(id, model)
        self.id = id
        self.coords = x,y
        self.z = 3
        self.model = model
        self.speed = np.random.choice(np.arange(1, 4), p=[0.3, 0.4, 0.3])
        self.next_pos = None
        self.direction = direction
        self.desc = "car"
        self.state = "None"
    
    def step(self):

        crash = self.model.grid.get_cell_list_contents([self.coords])

        for agent in crash:
            if ((type(agent) is CarAgent or type(agent) is CarAgentDifferentA or type(agent) is CarAgentDifferentB or type(agent) is CarAgentDifferentC) and agent.id != self.id):
                self.model.kill_agents.append(agent)
                return

        if self.direction == 0: 
            if self.coords == (8,4):
                self.next_pos = self.coords[0], self.coords[1]+1
                self.direction = 2
                return 
            lightCheck = ""
            if self.coords[0] != 9:
                checkLight = self.model.grid.get_cell_list_contents([(self.coords[0]+1,self.coords[1])])
                for agent in checkLight:
                    if type(agent) == TrafficLightAgent:
                        lightCheck = agent.state
                    #Change
                    elif type(agent) == GrassAgent:
                        self.direction = 3
                        return
            if lightCheck == "Green" or lightCheck == "":
                if(self.coords[0] < 9):
                    if self.model.time % self.speed == 0:
                        self.next_pos = self.coords[0]+1, self.coords[1]
                else:
                    #Change
                    self.next_pos = self.coords[0], self.coords[1]+1
                    self.direction = 3
            elif lightCheck == "Red":
                self.speed = 5
                self.next_pos = self.coords[0]+1, self.coords[1]

        elif self.direction == 1:
            #Change
            if self.coords == (4,1):
                self.next_pos = self.coords[0]+1, self.coords[1]
                self.direction = 3
                return 
            lightCheck = ""
            if self.coords[1] != 0:
                checkLight = self.model.grid.get_cell_list_contents([(self.coords[0],self.coords[1]-1)])
                for agent in checkLight:
                    if type(agent) == TrafficLightAgent:
                        lightCheck = agent.state
                    #Change
                    elif type(agent) == GrassAgent:
                        self.direction = 0
                        return
            if lightCheck == "Green" or lightCheck == "":
                if(self.coords[1] > 0):
                    if self.model.time % self.speed == 0:
                        self.next_pos = self.coords[0], self.coords[1]-1
                else:
                    self.next_pos = self.coords[0]+1, self.coords[1]
                    self.direction = 0

        elif self.direction == 2:
            #Change
            if self.coords == (1,5):
                self.next_pos = self.coords[0], self.coords[1]-1
                self.direction = 0
                return 
            lightCheck = ""
            if self.coords[0] != 0:
                checkLight = self.model.grid.get_cell_list_contents([(self.coords[0]-1,self.coords[1])])
                for agent in checkLight:
                    if type(agent) == TrafficLightAgent:
                        lightCheck = agent.state
                    #Change
                    elif type(agent) == GrassAgent:
                        self.direction = 1
                        return
            if lightCheck == "Green" or lightCheck == "":
                if(self.coords[0] > 0):
                    if self.model.time % self.speed == 0:
                        self.next_pos = self.coords[0]-1, self.coords[1]
                else:
                    self.next_pos = self.coords[0], self.coords[1]-1
                    self.direction = 1
            elif lightCheck == "Red":
                self.speed = 5
                self.next_pos = self.coords[0]-1, self.coords[1]

        elif self.direction == 3:
            #Change
            if self.coords == (5,8):
                self.next_pos = self.coords[0]-1, self.coords[1]
                self.direction = 1
                return 
            lightCheck = ""
            if self.coords[1] != 9:
                checkLight = self.model.grid.get_cell_list_contents([(self.coords[0],self.coords[1]+1)])
                for agent in checkLight:
                    if type(agent) == TrafficLightAgent:
                        lightCheck = agent.state
                    #Change
                    elif type(agent) == GrassAgent:
                        self.direction = 2
                        return
            if lightCheck == "Green" or lightCheck == "":
                if(self.coords[1] < 9):
                    if self.model.time % self.speed == 0:
                        self.next_pos = self.coords[0], self.coords[1]+1
                else:
                    self.next_pos = self.coords[0]-1, self.coords[1]
                    self.direction = 2
                if(self.coords[1] < 9):
                    if self.model.time % self.speed == 0:
                        self.next_pos = self.coords[0], self.coords[1]+1
                else:
                    self.next_pos = self.coords[0]-1, self.coords[1]
                    self.direction = 2
    def advance(self):
        if self.next_pos is not None:
            self.coords = self.next_pos
            self.model.grid.move_agent(self,self.coords)

#Agente diferente
class CarAgentDifferentB(Agent):
    def __init__(self,id, x, y, direction, model):
        super().__init__(id, model)
        self.id = id
        self.coords = x,y
        self.z = 3
        self.model = model
        self.speed = np.random.choice(np.arange(1, 4), p=[0.3, 0.4, 0.3])
        self.next_pos = None
        self.direction = direction
        self.desc = "TrafficLight"
    def step(self):

        crash = self.model.grid.get_cell_list_contents([self.coords])

        for agent in crash:
            if ((type(agent) is CarAgent or type(agent) is CarAgentDifferentA or type(agent) is CarAgentDifferentB or type(agent) is CarAgentDifferentC) and agent.id != self.id):
                self.model.kill_agents.append(agent)
                return

        #semaforo esquina inferior izquierda
        if self.direction == 0: 
            #Change
            if self.coords == (8,4):
                self.next_pos = self.coords[0], self.coords[1]+1
                self.direction = 2
                return
            lightCheck = ""
            if self.coords[0] != 9:
                checkLight = self.model.grid.get_cell_list_contents([(self.coords[0]+1,self.coords[1])])
                for agent in checkLight:
                    if type(agent) == TrafficLightAgent:
                        lightCheck = agent.state
                    #Change
                    elif type(agent) == GrassAgent:
                        self.direction = 3
                        return
            if lightCheck == "Green" or lightCheck == "":
                if(self.coords[0] < 4 or (self.coords[0] >= 5 and self.coords[0] < 9)):
                    if self.model.time % self.speed == 0:
                        self.next_pos = self.coords[0]+1, self.coords[1]
                elif(self.coords[0] == 4):
                    self.next_pos = self.coords[0], self.coords[1]
                    self.direction = 1
                elif(self.coords[0] == 9):
                    self.next_pos = self.coords[0], self.coords[1]+1
                    self.direction = 3
            elif lightCheck == "Red":
                self.next_pos = self.coords[0]+1, self.coords[1]

        #semaforo esquina superior izquierda
        elif self.direction == 1:
            #Change
            if self.coords == (4,1):
                self.next_pos = self.coords[0]+1, self.coords[1]
                self.direction = 3
                return 
            lightCheck = ""
            if self.coords[1] != 0:
                checkLight = self.model.grid.get_cell_list_contents([(self.coords[0],self.coords[1]-1)])
                for agent in checkLight:
                    if type(agent) == TrafficLightAgent:
                        lightCheck = agent.state
                    #Change
                    elif type(agent) == GrassAgent:
                        self.direction = 0
                        return
            if lightCheck == "Green" or lightCheck == "":
                if(self.coords[1] > 5 or (self.coords[1] <= 4 and self.coords[1] > 0)):
                    if self.model.time % self.speed == 0:
                        self.next_pos = self.coords[0], self.coords[1]-1
                elif(self.coords[1] == 5):
                    self.next_pos = self.coords[0], self.coords[1]
                    self.direction = 2
                elif(self.coords[1] == 0):
                    self.next_pos = self.coords[0]+1, self.coords[1]
                    self.direction = 0

        #semaforo esquina superior derecha
        elif self.direction == 2:
            #Change
            if self.coords == (1,5):
                self.next_pos = self.coords[0], self.coords[1]-1
                self.direction = 0
                return 
            lightCheck = ""
            if self.coords[0] != 0:
                checkLight = self.model.grid.get_cell_list_contents([(self.coords[0]-1,self.coords[1])])
                for agent in checkLight:
                    if type(agent) == TrafficLightAgent:
                        lightCheck = agent.state
                    #Change
                    elif type(agent) == GrassAgent:
                        self.direction = 1
                        return
            if lightCheck == "Green" or lightCheck == "":
                if(self.coords[0] > 5 or (self.coords[0] <= 4 and self.coords[0] > 0)):
                    if self.model.time % self.speed == 0:
                        self.next_pos = self.coords[0]-1, self.coords[1]
                elif(self.coords[0] == 5):
                    self.next_pos = self.coords[0], self.coords[1]
                    self.direction = 3
                elif(self.coords[0] == 0):
                    self.next_pos = self.coords[0], self.coords[1]-1
                    self.direction = 1
            elif lightCheck == "Red":
                self.next_pos = self.coords[0]-1, self.coords[1]

        #semaforo esquina inferior derecha
        elif self.direction == 3:
            #Change
            if self.coords == (5,8):
                self.next_pos = self.coords[0]-1, self.coords[1]
                self.direction = 1
                return 
            lightCheck = ""
            if self.coords[1] != 9:
                checkLight = self.model.grid.get_cell_list_contents([(self.coords[0],self.coords[1]+1)])
                for agent in checkLight:
                    if type(agent) == TrafficLightAgent:
                        lightCheck = agent.state
                    #Change
                    elif type(agent) == GrassAgent:
                        self.direction = 2
                        return
            if lightCheck == "Green" or lightCheck == "":
                if(self.coords[1] < 4 or(self.coords[1] >= 5 and self.coords[1] < 9)):
                    if self.model.time % self.speed == 0:
                        self.next_pos = self.coords[0], self.coords[1]+1
                elif(self.coords[1] == 4):
                    self.next_pos = self.coords[0], self.coords[1]
                    self.direction = 0
                elif(self.coords[1] == 9):
                    self.next_pos = self.coords[0]-1, self.coords[1]
                    self.direction = 2
    def advance(self):
        if self.next_pos is not None:
            self.coords = self.next_pos
            self.model.grid.move_agent(self,self.coords)


class CarAgentDifferentC(Agent):
    def __init__(self,id, x, y, direction, model):
        super().__init__(id, model)
        self.id = id
        self.coords = x,y
        self.z = 3
        self.model = model
        self.speed = 2
        self.next_pos = None
        self.direction = direction
        self.desc = "TrafficLight"
    def step(self):

        crash = self.model.grid.get_cell_list_contents([self.coords])

        for agent in crash:
            if ((type(agent) is CarAgent or type(agent) is CarAgentDifferentA or type(agent) is CarAgentDifferentB or type(agent) is CarAgentDifferentC) and agent.id != self.id):
                self.model.kill_agents.append(agent)
                return

        if self.direction == 0: 
            #Change
            if self.coords == (8,4):
                self.next_pos = self.coords[0], self.coords[1]+1
                self.direction = 2
                return 
            lightCheck = ""
            if self.coords[0] != 9:
                checkLight = self.model.grid.get_cell_list_contents([(self.coords[0]+1,self.coords[1])])
                for agent in checkLight:
                    if type(agent) == TrafficLightAgent:
                        lightCheck = agent.state
                    #Change
                    elif type(agent) == GrassAgent:
                        self.direction = 3
                        return
            if lightCheck == "Green" or lightCheck == "":
                if(self.coords[0] < 9):
                    if self.model.time % self.speed == 0:
                        self.next_pos = self.coords[0]+1, self.coords[1]
                else:
                    self.next_pos = self.coords[0], self.coords[1]+1
                    self.direction = 3

        elif self.direction == 1:
            #Change
            if self.coords == (4,1):
                self.next_pos = self.coords[0]+1, self.coords[1]
                self.direction = 3
                return 
            lightCheck = ""
            if self.coords[1] != 0:
                checkLight = self.model.grid.get_cell_list_contents([(self.coords[0],self.coords[1]-1)])
                for agent in checkLight:
                    if type(agent) == TrafficLightAgent:
                        lightCheck = agent.state
                    #Change
                    elif type(agent) == GrassAgent:
                        self.direction = 0
                        return
            if lightCheck == "Green" or lightCheck == "":
                if(self.coords[1] > 0):
                    if self.model.time % self.speed == 0:
                        self.next_pos = self.coords[0], self.coords[1]-1
                else:
                    self.next_pos = self.coords[0]+1, self.coords[1]
                    self.direction = 0
            elif lightCheck == "Red":
                self.speed = 1
                self.next_pos = self.coords[0], self.coords[1]-1

        elif self.direction == 2:
            #Change
            if self.coords == (1,5):
                self.next_pos = self.coords[0], self.coords[1]-1
                self.direction = 0
                return 
            lightCheck = ""
            if self.coords[0] != 0:
                checkLight = self.model.grid.get_cell_list_contents([(self.coords[0]-1,self.coords[1])])
                for agent in checkLight:
                    if type(agent) == TrafficLightAgent:
                        lightCheck = agent.state
                    #Change
                    elif type(agent) == GrassAgent:
                        self.direction = 1
                        return
            if lightCheck == "Green" or lightCheck == "":
                if(self.coords[0] > 0):
                    if self.model.time % self.speed == 0:
                        self.next_pos = self.coords[0]-1, self.coords[1]
                else:
                    self.next_pos = self.coords[0], self.coords[1]-1
                    self.direction = 1

        elif self.direction == 3:
            #Change
            if self.coords == (5,8):
                self.next_pos = self.coords[0]-1, self.coords[1]
                self.direction = 1
                return 
            lightCheck = ""
            if self.coords[1] != 9:
                checkLight = self.model.grid.get_cell_list_contents([(self.coords[0],self.coords[1]+1)])
                for agent in checkLight:
                    if type(agent) == TrafficLightAgent:
                        lightCheck = agent.state
                    #Change
                    elif type(agent) == GrassAgent:
                        self.direction = 2
                        return
            if lightCheck == "Green" or lightCheck == "":
                if(self.coords[1] < 9):
                    if self.model.time % self.speed == 0:
                        self.next_pos = self.coords[0], self.coords[1]+1
                else:
                    self.next_pos = self.coords[0]-1, self.coords[1]
                    self.direction = 2
            elif lightCheck == "Red":
                self.speed = 1
                self.next_pos = self.coords[0], self.coords[1]+1

    def advance(self):
        if self.next_pos is not None:
            self.coords = self.next_pos
            self.model.grid.move_agent(self,self.coords)









class CrashAgent(Agent):
    def __init__(self,id, x, y, model):
        super().__init__(id, model)
        self.id = id
        self.coords = x,y
        self.model = model
    
    def step(self):

        crash = self.model.grid.get_cell_list_contents([self.coords])

        for agent in crash:
            if (type(agent) is CarAgent):
                self.model.kill_agents.append(agent)
                return