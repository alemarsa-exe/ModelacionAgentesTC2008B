from mesa import Model
from mesa.time import SimultaneousActivation, RandomActivationByType
from mesa.space import MultiGrid
import time
import numpy as np
import itertools
from agent import *


class StreetModel(Model):
    def __init__(self,M,N):
        self.grid = MultiGrid(M,N,False)
        self.x = M
        self.y = N
        self.schedule = SimultaneousActivation(self)
        self.running = True
        self.id = 0
        self.time = 0
        self.kill_agents = []


        pos = [0,1,2,7,8,9]
        for i in pos:
            for j in pos:
                a = GrassAgent(self.id, i, j, self)
                self.grid.place_agent(a, (i, j))
                self.schedule.add(a)
                self.id = self.id + 1
        
        posTraffic = [[2,4,2], [7,5,0], [4,7,3], [5,2,1]]

        for i in posTraffic:
            a = TrafficLightAgent(self.id, i[0], i[1], i[2], self)
            self.grid.place_agent(a, (i[0], i[1]))
            self.schedule.add(a)
            self.id = self.id + 1

        posTrafficMirror = [[2,3,2,4,2], [7,6,7,5,0], [3,7,4,7,3], [6,2,5,2,1]]

        for i in posTrafficMirror:
            a = TrafficLightAgent(self.id, i[0], i[1], i[4], self)
            a.mirror = (i[2], i[3])
            self.grid.place_agent(a, (i[0], i[1]))
            self.schedule.add(a)
            self.id = self.id + 1

        a = CarAgentDifferentA(self.id, 0, 4, 0, self)
        self.grid.place_agent(a, (0, 4))
        self.schedule.add(a)
        self.id = self.id + 1

        a = CarAgent(self.id, 0, 3, 0, self)
        self.grid.place_agent(a, (0, 3))
        self.schedule.add(a)
        self.id = self.id + 1



        a = CarAgentDifferentB(self.id, 9, 5, 2, self)
        self.grid.place_agent(a, (9, 5))
        self.schedule.add(a)
        self.id = self.id + 1

        a = CarAgent(self.id, 9, 6, 2, self)
        self.grid.place_agent(a, (9, 6))
        self.schedule.add(a)
        self.id = self.id + 1



        a = CarAgentDifferentC(self.id, 3, 9, 1, self)
        self.grid.place_agent(a, (3, 9))
        self.schedule.add(a)
        self.id = self.id + 1

        a = CarAgent(self.id, 4, 9, 1, self)
        self.grid.place_agent(a, (4, 9))
        self.schedule.add(a)
        self.id = self.id + 1




        a = CarAgent(self.id, 5, 0, 3, self)
        self.grid.place_agent(a, (5, 0))
        self.schedule.add(a)
        self.id = self.id + 1

        a = CarAgent(self.id, 6, 0, 3, self)
        self.grid.place_agent(a, (6, 0))
        self.schedule.add(a)
        self.id = self.id + 1


        

        a = RoadAgent(self.id, 4, 4, self)
        self.grid.place_agent(a, (4, 4))
        self.schedule.add(a)
        self.id = self.id + 1

        a = RoadAgent(self.id, 4, 5, self)
        self.grid.place_agent(a, (4, 5))
        self.schedule.add(a)
        self.id = self.id + 1

        a = RoadAgent(self.id, 5, 4, self)
        self.grid.place_agent(a, (5, 4))
        self.schedule.add(a)
        self.id = self.id + 1

        a = RoadAgent(self.id, 5, 5, self)
        self.grid.place_agent(a, (5, 5))
        self.schedule.add(a)
        self.id = self.id + 1

                
    def step(self):
        self.schedule.step()
        carPos = []
        trafficLights = []
        for agent in self.schedule.agents:
            if(type(agent) == CarAgent or type(agent) == CarAgentDifferentA or type(agent) == CarAgentDifferentB or type(agent) == CarAgentDifferentC):
            #     carPos.append((str(agent.id), agent.coords[0], agent.z, agent.coords[1], str(type(agent))))
                carID = str(agent.id)
                carX = agent.coords[0]
                carZ = agent.coords[1]
                carY = agent.z
                carType = str(type(agent))

                pos = [carID, carX, carY, carZ, carType]
                carPos.append(pos)

            if(type(agent) == TrafficLightAgent):
                #trafficLights.append((agent.id, agent.state))
                lightID = str(agent.id)
                lightState = agent.state
                l = [lightID, lightState]
                trafficLights.append(l)

        print(carPos)
        print(trafficLights)
        self.time += 1
        for x in self.kill_agents:
            self.grid.remove_agent(x)
            self.schedule.remove(x)
            self.kill_agents.remove(x)
        
        return carPos, trafficLights