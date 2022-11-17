from flask import Flask, request, jsonify
from model import RobotModel, BoxAgent,RobotAgent

#Board parameters
numberOfBoxes = 5
width = 10
height = 10
maxFrames = 200
currentStep = 0
robotModel=0



app = Flask("agentes")

@app.route('/init', methods=['POST'])
def init():
    global numberOfBoxes, width, height, maxFrames,currentStep,robotModel
    numberOfBoxes = request.json['numberOfBoxes']
    width = request.json['width']
    height = request.json['height']
    maxFrames = request.json['maxFrames']
    currentStep = 0
    print(numberOfBoxes, width, height, maxFrames)
    robotModel = RobotModel( width, height, numberOfBoxes, maxFrames)
    return jsonify({"message":"Parameters recieved, model initiated."})

@app.route('/robots', methods=['GET'])
def getRobots():
    global robotModel
    return jsonify({"positions":robotModel.getRobots()})
@app.route('/boxes', methods=['GET'])
def getBoxes():
    global robotModel
    return jsonify({"positions":robotModel.getBoxes()})


@app.route('/step', methods=['GET'])
def step():
    global robotModel, currentStep
    robotModel.step()
    currentStep += 1
    return jsonify({'message':f'Model updated to step {currentStep}.', 'currentStep':currentStep})

if __name__=='__main__':
    app.run(host="localhost", port=8585, debug=True)