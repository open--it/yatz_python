from flask import Flask, jsonify, Response, request
from random import randint
import collections
import json

class Player:
  def __init__(self,id):
    self.id = seq
    self.game = [None,None,None,None,None,None,None,None,None,None,None,None,None]
    self.turn = 0

class PlayerEncoder(json.JSONEncoder):
  def default(self, obj):
    if isinstance(obj, Player):
      return {
        'id':obj.id,
        'game':obj.game,
        'turn':obj.turn
      }
    return json.JSONEncoder.default(self, obj)

seq = 0
players = []
app = Flask(__name__,static_url_path='')

@app.route("/")
def yahtzee():
  return app.send_static_file('index.html')

@app.route("/enroll")
def enroll():
  global seq
  global players
  players.append(Player(seq))
  seq+=1
  return jsonify(id=seq-1)

@app.route("/players")
def playerss():
  global players
  return Response(json.dumps(players, cls=PlayerEncoder),mimetype='application/json')

@app.route("/<user>/roll",methods=['POST'])
def userRoll(user):
  id = int(user)
  cubes = list(request.json)
  global players
  if players[id].turn < 3 :
    for x in range(len(cubes)):
      if cubes[x]["status"]=="unhold" :
        cubes[x]["eye"] = randint(0,5)
    players[id].turn +=1
  return Response(json.dumps(cubes), mimetype='application/json')

@app.route("/<user>/decision",methods=['POST'])
def userDecision(user):
  return "decision"

if __name__ == "__main__":
  app.run(debug=True,host='0.0.0.0')