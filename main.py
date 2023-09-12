from flask import Flask, request, jsonify


import json

chosen_word = {}
chosen_word['num_guesses'] = 0
guesses = {1:"", 2:"", 3:"", 4:"", 5:""}
requested_hint = True
app = Flask(__name__)
@app.route('/', methods=['GET'])
def home():
  return "<h1>Textle</h1>"

# Client 1 chooses a word for Client 2 to guess and sends it to server
@app.route('/choose_word', methods=['POST'])
def choose_word():
  data = request.data
  chosen_word['word'] = json.loads(data)
  return jsonify(chosen_word['word'])
  
#Server sends guess feedback to client 2
@app.route('/get_feedback', methods=['GET'])
def get_feedback():
  data = request.data
  data = json.loads(data)
  result = ""
  letters_correct = []
  misplaced_letters = []
  for i in range(len(chosen_word['word'])):
    if data[i] == chosen_word['word'][i]:
      result += "O"
      letters_correct.append(data[i])
      
    elif ((data[i] in chosen_word['word']) and (data[i] not in letters_correct and data[i] not in misplaced_letters)):
      result += "+"
      misplaced_letters.append(result)

    else:
      result += "X"

  chosen_word['num_guesses'] += 1
  chosen_word['feedback'] = result
  guess_num = chosen_word['num_guesses']
  guesses[guess_num] = result
  
  return jsonify({"result":result})

@app.route('/request_feedback', methods=['GET'])
def send_feedback():
  return jsonify(guesses)
  
  
# Client 1 sends hint to server if guesses equals 3
@app.route('/send_hint', methods=['POST'])
def send_hint():
  data = request.data
  data = json.loads(data)
  chosen_word['hint'] = data
  return jsonify(chosen_word['hint'])

@app.route('/request_hint', methods=['POST'])
def request_hint():
  return jsonify(chosen_word['hint'])
  
# Server sends hint to client 2
# @app.route('/get_hint', methods=['GET'])
# def get_hint():
#   return jsonify(chosen_word['hint'])

@app.route('/get_guesses', methods=['GET'])
def get_guesses():
  data = request.data
  return jsonify(chosen_word['num_guesses'])

finished = ["0"]
@app.route('/finished_guessing', methods=['POST'])
def finished_guessing():
  finished[0] = "1"
  return jsonify(finished[0])
  

@app.route('/get_done', methods=['GET'])
def get_done():
  if finished[0] == "0":
    return jsonify("0")
  else:
    return jsonify("1")
  

# Client 2 sends result to server
@app.route('/send_result', methods=['POST'])
def send_result():
  data = request.data
  data = json.loads(data)
  chosen_word["result"] = data
  return jsonify(chosen_word["result"])
  
  
    
# Client 1 gets result from server
@app.route('/get_result', methods=['GET'])
def get_result():
  return jsonify(chosen_word["result"])

# Client 2 recieves the correct word once game is done
@app.route('/get_word', methods=['GET'])
def get_word():
  return jsonify(chosen_word["word"])
  
  


app.run(host='0.0.0.0')