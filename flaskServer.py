from flask import Flask, request, jsonify
from model import StreetModel
import json

# Size of the board:
width = 10
height = 10

model = StreetModel(width, height)


def positionsToJSON(carPos):
    posDICT = []
    for p in carPos:
        pos = {
            "carId": p[0],
            "x": p[1],
            "y": p[2],
            "z": p[3],
            "typeCar": p[4],
        }
        posDICT.append(pos)
    #return jsonify({'positions': posDICT})
    return json.dumps(posDICT)

# def grassToJSON(grassPos):
#     posDICT = []
#     for p in grassPos:
#         pos = {
#             "carId": p[0],
#             "x": p[1],
#             "y": p[2],
#             "z": p[3],
#             "typeCar": p[4],
#         }
#         posDICT.append(pos)
#     #return jsonify({'positions': posDICT})
#     return json.dumps(posDICT)


def lightStatesToJSON(trafficLights):
    lightDICT = []
    count = 0
    for tra in trafficLights:
        light = {
            "lightId": tra[0],
            "state": tra[1]
        }
        lightDICT.append(light)
        #count += 1
    # for s in range(4):
    #     light = {
    #         "state": lightStates[s]
    #     }
    #     lightDICT.append(light)
    #return jsonify({'positions': lightDICT})
    return json.dumps(lightDICT)


# Set the number of agents here:
# flock = []

app = Flask("Cruce")


@app.route('/')
def root():
    return jsonify([{
        'message': 'Hello World!'
    }])


@app.route('/init', methods=['POST', 'GET'])
def model_run():
    [carPos, trafficLights] = model.step()

    ans = "{ \"positions\": " + positionsToJSON(
        carPos) + ", \"trafficLights\": " + lightStatesToJSON(trafficLights) + " }"


    return ans


if __name__ == '__main__':
    app.run(host="localhost", port=8585, debug=True)