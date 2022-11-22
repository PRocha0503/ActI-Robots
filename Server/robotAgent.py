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
        #Map with unknown values
        self.map = [["W" for i in range(self.model.grid.height)] for j in range(self.model.grid.width)]
        self.last = None

    def moveAgent(self,pos):
        self.last = self.pos
        self.model.grid.move_agent(self, pos)
    
    def moveWithBox(self,pos):
        self.last = self.pos
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

    def dontGoBack(self,map, dist):
        if self.last:
            for d in dist:
                if map[d] == self.last:
                    dist.remove(d)
                else:
                    return
    
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
                d = self.getDistance(xHome,yHome,_x,_y)
                dist.append(d)
                distMap[d] = _x,_y
            else:
                for a in isSomeOneThere(_x,_y):
                    if isinstance(a,BoxAgent) and a.collected == False:
                       self.map[_x][_y]="B"
                    elif isinstance(a,RobotAgent):
                        self.joinMaps(a)
        dist.sort()
        self.dontGoBack(distMap,dist)
        if abs(xHome-x) == 1 and abs(yHome-y) == 0 or abs(xHome-x) == 0 and abs(yHome-y) == 1 :
            self.model.grid.move_agent(self.box, self.model.dropLocation)
            self.box.collected = True
            self.box.y = self.model.numberOfBoxesCollected % 5 * 0.5
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
        #The cell is empty
        self.map[self.pos[0]][self.pos[1]] = "E"
        #Get the neighbors
        possible_steps = self.model.grid.get_neighborhood(
            self.pos,
            moore=False,
            include_center=False
            )
        occ = []
        boxPos = self.knownBox()
        unknownPos = self.knownUnknown()
        #Check if there is a box
        for pos in possible_steps:
            cellmates = self.model.grid.get_cell_list_contents([pos])
            if self.includes(cellmates,BoxAgent) and not self.includes(cellmates,RobotAgent):
                self.getBox(cellmates[0])
                self.map[pos[0]][pos[1]] = "P"
                return
            elif self.includes(cellmates,RobotAgent):
                occ.append(pos)
                for a in cellmates:
                    if isinstance(a,RobotAgent):
                        self.joinMaps(a)
            elif self.collectedBox(cellmates):
                self.map[pos[0]][pos[1]] = "C"
                occ.append(pos)
            else:
                self.map[pos[0]][pos[1]] = "E"
            
        if boxPos:
            self.goTo(boxPos)
            return
        elif unknownPos:
            self.goTo(unknownPos)
            return

        
        freeSpaces=list(map(lambda x: x not in occ, possible_steps))
        nextMoves = [p for p,f in zip(possible_steps,freeSpaces ) if f == True]
        if len(nextMoves) > 0:
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
        self.box.y = 0.3

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
                return a.pos
        return False
    def collectedBox(self,agents):
        for a in agents:
            if isinstance(a,BoxAgent):
                return a.collected
        return False
    def printMap(self):
        for i in range(len(self.map[0])):
            print(self.map[i])
        print("=====================================")
    def joinMaps(self,otherAgent):
        for i in range(len(self.map)):
            for j in range(len(self.map[0])):
                if self.map[i][j] == "W" and otherAgent.map[i][j] != "W":
                    self.map[i][j] = otherAgent.map[i][j]
                elif otherAgent.map[i][j] == "W" and self.map[i][j] != "W":
                    otherAgent.map[i][j] = self.map[i][j]
                elif self.map[i][j] == "P" and otherAgent.map[i][j] == "B":
                    otherAgent.map[i][j] = "P"
                elif self.map[i][j] == "B" and otherAgent.map[i][j] == "P":
                    self.map[i][j] = "P"
                elif self.map[i][j] == "E" and otherAgent.map[i][j] != "E":
                    otherAgent.map[i][j] = "E"
                elif self.map[i][j] != "E" and otherAgent.map[i][j] == "E":
                    self.map[i][j] = "E"
    def knownBox(self):
        for i in range(len(self.map)):
            for j in range(len(self.map[0])):
                if self.map[i][j] == "B":
                    pos = (i,j)
                    return pos
        return False
    def knownUnknown(self):
        for i in range(len(self.map)):
            for j in range(len(self.map[0])):
                if self.map[i][j] == "W":
                    pos = (i,j)
                    return pos
        return False
    def getDistance(self,x,y,x2,y2):
        return math.sqrt(math.pow((x-x2),2)+math.pow((y-y2),2)) 
    def goTo(self,pos):
        x,y = pos
        possible_steps = self.model.grid.get_neighborhood(
            self.pos,
            moore=False,
            include_center=False
            )

        def isSomeOneThere(x,y):
            return self.model.grid.get_cell_list_contents([(x,y)])
        
        dist = []
        distMap = {}
        self.dontGoBack(distMap,dist)
        fallback = []
        for step in possible_steps:
            _x,_y = step
            if not isSomeOneThere(_x,_y):
                d = self.getDistance(x,y,_x,_y)
                dist.append(d)
                distMap[d] = _x,_y
                fallback = _x,_y
            else:
                for a in isSomeOneThere(_x,_y):
                    if isinstance(a,BoxAgent) and a.collected==False:
                       self.map[_x][_y]="B"
                    elif isinstance(a,RobotAgent):
                        self.joinMaps(a)
        dist.sort()
        if len(dist) != 0:
            self.moveAgent(distMap[dist[0]])
        elif fallback:
            self.moveAgent(fallback)
