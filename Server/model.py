from mesa import Model, agent
from mesa.time import RandomActivation
from mesa.space import MultiGrid
from mesa.datacollection import DataCollector
from boxAgent import BoxAgent
from robotAgent import RobotAgent

class RobotModel(Model):
    """
    Model class for the Robot Model
    input: width, height, number of boxes, max frames
    output: model
    """
    def __init__(self, width, height, numberOfBoxes, maxFrames):
        """
        Initialize the model
        input: width, height, number of boxes, max frames
        output: model
        """
        #The grid
        self.grid = MultiGrid(width,height,torus = False) 
        #The scheduler
        self.schedule = RandomActivation(self)
        #The number of boxes
        self.numberOfBoxes = numberOfBoxes
        #The number of robots
        self.numberOfRobots = 5
        #The max frames
        self.maxFrames = maxFrames
        #The current frame
        self.currentFrame = 0
        #The number of boxes collected
        self.numberOfBoxesCollected = 0
        #Run the model
        self.running = True

    

        #Stack Location
        self.setDropLocation()


        #Place the boxes and the robots
        self.placeBoxes()
        self.placeRobots()
    
    def setDropLocation(self):
        """
        Set the drop Location
        input:none
        output:none
        """
        pos = (0,0)
        while not self.grid.is_cell_empty(pos):
            pos = (pos[0]+1,pos[1])
        self.dropLocation  = pos
    
    def placeBoxes(self):
        """
        Place the boxes
        input: none
        output: none
        """
        for i in range(self.numberOfBoxes):
            cords = self.grid.find_empty()
            #Create a box agent
            box = BoxAgent(cords, self)
            #Place the box agent
            self.grid.place_agent(box,cords)
            #Add the box agent to the schedule
            self.schedule.add(box)
    def placeRobots(self):
        """
        Place the robots
        input: none
        output: none
        """
        for i in range(self.numberOfRobots):
            cords = self.grid.find_empty()
            #Create a robot agent
            robot = RobotAgent(cords, self)
            #Place the robot agent
            self.grid.place_agent(robot, cords)
            #Add the robot agent to the schedule
            self.schedule.add(robot)

    def newDropLocation(self):
        if self.numberOfBoxesCollected % 5 == 0 and self.numberOfBoxesCollected != 0:
            x,y = self.dropLocation
            newPosition = (x+1,y)
            while not self.grid.is_cell_empty(newPosition):
                print("Cell ocupied",newPosition)
                newPosition = (newPosition[0]+1,newPosition[1])
            self.dropLocation  = newPosition
    
    def getRobots(self):
        """
        Get the robots
        input: none
        output: robots
        """
        return [{"x":robot.pos[0],"y":0,"z":robot.pos[1]} for robot in self.schedule.agents if type(robot) is RobotAgent]
    def getBoxes(self):
        """
        Get the boxes
        input: none
        output: boxes
        """
        return [{"x":box.pos[0],"y":box.y,"z":box.pos[1]} for box in self.schedule.agents if type(box) is BoxAgent]
            
    def step(self):
        """
        Advance the model by one step
        input: none
        output: none
        """
        #Advance the scheduler
        self.schedule.step()
        #Advance the frame
        self.currentFrame += 1
        #Check if the max frames have been reached
        if self.currentFrame >= self.maxFrames or self.numberOfBoxesCollected == self.numberOfBoxes:
            #Stop the model
            self.running = False
        
        

