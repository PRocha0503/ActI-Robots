import math
from boxAgent import BoxAgent
from mesa import Agent

class RobotAgent(Agent):
    """
    Robot agent class
    input: unique id, model
    output: robot agent
    """

    def __init__(self,unique_id,model):
        """
        Initialize the robot agent
        input: unique id, model
        output: robot agent
        """
        super().__init__(unique_id, model)
        self.box = None
    def moveAgent(self,pos):
        self.model.grid.move_agent(self, pos)
    
    def moveWithBox(self,pos):
        self.model.grid.move_agent(self, pos)
        self.model.grid.move_agent(self.box, pos)

    def move(self):
        """
        Move the robot
        input: none
        output: none
        """
        if (self.box):
            self.moveHome()
            return
        else:
            self.searchForBox()
    
    def moveHome(self):
        """
        Go back to dropLocation
        input:none
        output:none
        """
        xHome,yHome = self.model.dropLocation
        x,y = self.pos
        #Get adj cells
        possible_steps = self.model.grid.get_neighborhood(
            self.pos,
            moore=False,
            include_center=False
            )

        def isSomeOneThere(x,y):
            return self.model.grid.get_cell_list_contents([(x,y)])
        
        dist = []
        distMap = {}
        
        for step in possible_steps:
            _x,_y = step
            if not  isSomeOneThere(_x,_y ):
                d = math.sqrt(math.pow((xHome-_x),2)+math.pow((yHome-_y),2))
                dist.append(d)
                distMap[d] = _x,_y
        dist.sort()

        if abs(xHome-x) == 1 and abs(yHome-y) == 0 or abs(xHome-x) == 0 and abs(yHome-y) == 1 :
            self.model.grid.move_agent(self.box, self.model.dropLocation)
            self.box.collected = True
            self.model.numberOfBoxesCollected += 1
            self.model.newDropLocation()
            self.box = None

        elif len(dist) >0 :
            self.moveWithBox(distMap[dist[0]])

    
    def searchForBox(self):
        """
        Search for a box
        input: none
        output: none
        """
        #Get the neighbors
        possible_steps = self.model.grid.get_neighborhood(
            self.pos,
            moore=False,
            include_center=False
            )
        occ = []
        #Check if there is a box
        for pos in possible_steps:
            cellmates = self.model.grid.get_cell_list_contents([pos])
            if self.includes(cellmates,BoxAgent) and not self.includes(cellmates,RobotAgent):
                self.getBox(cellmates[0])
                return
            elif self.includes(cellmates,RobotAgent) or self.collectedBox(cellmates):
                occ.append(pos)
        
        freeSpaces=list(map(lambda x: x not in occ, possible_steps))
        nextMoves = [p for p,f in zip(possible_steps,freeSpaces ) if f == True]
        nextMove = self.random.choice(nextMoves)
        self.moveAgent(nextMove)

    

    def getBox(self,box):
        """
        Get the box
        input: box
        output: none
        """
        self.model.grid.move_agent(box, self.pos)
        self.box = box

    def step(self):
        """
        Step function
        input: none
        output: none
        """
        self.move()

    def includes(self,agents,type):
        """
        Check if a array includes an agent
        input: agents,type
        output: bool
        """
        for a in agents:
            if type == BoxAgent:
                try:
                    return not a.collected
                except:
                    continue
            if isinstance(a,type):
                return True
        return False
    
    def collectedBox(self,agents):
        for a in agents:
            if isinstance(a,BoxAgent):
                return a.collected
        return False