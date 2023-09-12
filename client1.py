# ***The first client is prompted to enter a five letter word. ***

import requests, time

BASE_URL = 'https://Textle.devingriffin.repl.co' #access granted by a url
print("Welcome to Textle! Your job is to input a five letter word for another user to guess.\n\n")
x = 0

word1 = input("Choose a five letter word to guess: ")

data_sent = word1 #dictionary of the data you want to send
response = requests.post(BASE_URL + '/choose_word', json=data_sent) #defining URL(/hello_post) to send data
hint = input("Enter a hint in case the other player needs one: ")
hintPost = requests.post(BASE_URL + '/send_hint', json=hint)
done = "0"

#While client 2 is guessing
guess_num = 1
while (done == "0"):
  time.sleep(3)
  feedback = requests.get(BASE_URL + '/request_feedback')
  feedback = feedback.json()
  if feedback[str(guess_num)] != "":
    if guess_num==6:
      break
    print("The other player's feedback for guess "+str(guess_num)+ " was", feedback[str(guess_num)])
    guess_num += 1
  done_result = requests.get(BASE_URL + '/get_done')
  done = done_result.json()
  
#After all guesses
if done=="1":
  result = requests.get(BASE_URL + '/get_result')
  print(result.json())



  



