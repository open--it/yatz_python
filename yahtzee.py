from flask import Flask

app = Flask(__name__,static_url_path='')

@app.route("/")
def yahtzee():
  return "hello world"

@app.route("/enroll")
def enroll():
  return "enroll "

@app.route("/players")
def playerss():
  return "players"

@app.route("/<user>/roll",methods=['POST'])
def userRoll(user):
  return "roll"

@app.route("/<user>/decision",methods=['POST'])
def userDecision(user):
  return "decision"

if __name__ == "__main__":
  app.run(debug=True,host='0.0.0.0')