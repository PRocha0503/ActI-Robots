# from boxAgent import BoxAgent
# from robotAgent import RobotAgent
from model import RobotModel, BoxAgent,RobotAgent
from mesa.visualization.modules import CanvasGrid, BarChartModule,PieChartModule
from mesa.visualization.ModularVisualization import ModularServer
from mesa.visualization.UserParam import Slider,NumberInput

def agent_portrayal(agent):
    """
    Portrayal Method for canvas
    input: agent
    output: portrayal
    """
    if agent is None:
        return
    portrayal={"Shape":"rect",
                     "Filled":"true",
                     "Layer":0,
                     "Color":"yellow",
                     "w":0.8,
                     "h":0.8
                     }
    

    if isinstance(agent,BoxAgent):
        portrayal["Layer"]=1
        portrayal["Color"]="brown"
        portrayal["w"]=0.5
        portrayal["h"]=0.5
    
    return portrayal
#Parameters for the model
model_params = {
    "width": 20,
    "height": 20,
    "numberOfBoxes": Slider("Number of Boxes", 10,5, 40,1),
    "maxFrames":Slider("Max Frames", 200, 10, 1000,10)
    }

#Grid object
grid  =  CanvasGrid(agent_portrayal, 20, 20, 500, 500)

#Server object
server = ModularServer(RobotModel,[grid], "Robot Model", model_params)

#Run the server
server.port = 8521 
server.launch()