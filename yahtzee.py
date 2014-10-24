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

smstraight = [ [1,2,3,4], [2,3,4,5], [3,4,5,6] ]
lgstraight = [ [1,2,3,4,5], [2,3,4,5,6] ]
rule = [
 lambda dices : collections.Counter(dices)[1]*1   ## Aces - 0
,lambda dices : collections.Counter(dices)[2]*2   ## Twos - 1
,lambda dices : collections.Counter(dices)[3]*3   ## Threes - 2
,lambda dices : collections.Counter(dices)[4]*4   ## Fours - 3
,lambda dices : collections.Counter(dices)[5]*5   ## Fives - 4
,lambda dices : collections.Counter(dices)[6]*6   ## Sixes - 5
,lambda dices : reduce(lambda x,y:x+y,dices) if len([(x,y)for x,y in collections.Counter(dices).most_common(1) if y >= 3 ]) >= 1 else 0   ## 3 of a kind - 6
,lambda dices : reduce(lambda x,y:x+y,dices) if len([(x,y)for x,y in collections.Counter(dices).most_common(1) if y >= 4 ]) >= 1 else 0   ## 4 of a kind - 7
,lambda dices : 25 if reduce(lambda x,y: x+y ,[y for x,y in collections.Counter(dices).most_common(2) if y >= 2]) == 5 else 0   ## Full House - 8
,lambda dices : 30 if len( [list(x) for x in [set(dices).intersection(set(d)) for d in smstraight] if len(x)==4] ) >0 else 0   ## 30 Sm.Straight - 9
,lambda dices : 40 if len( [list(x) for x in [set(dices).intersection(set(d)) for d in lgstraight] if len(x)==5] ) >0 else 0   ## 40 Lg.Straight - 10
,lambda dices : 50 if collections.Counter(dices).values()[0]==5 else 0   ## Yahtzee - 11
,lambda dices : reduce(lambda x,y:x+y ,dices)   ## chance - 12
]
@app.route("/<user>/decision",methods=['POST'])
def userDecision(user):
  id = int(user)
  slot = int(request.json["slot"])
  dices = [int(x["eye"])+1 for x in request.json["dices"] ]
  point = rule[slot](dices)
  global players
  players[id].game[slot] = point
  players[id].turn = 0
  return jsonify(slot=slot,point=point)

if __name__ == "__main__":
  app.run(debug=True,host='0.0.0.0')