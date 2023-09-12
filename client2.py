import requests

BASE_URL = 'https://Textle.devingriffin.repl.co'
win = False
win_end = "Congratulations! You were successful in guessing the word!"
lose_end = "Oof, better luck next time!\n"
num_guesses = 0

#Starting messages 
print("Welcome to Textle! Your job is to guess a five letter word that another user has inputted. You have 5 chances. Good luck!\n\n")
print("Your guess results will include the following:\nO - correct letter and position\nX - letter not included\n+ - letter included but wrong position")

#Guessing loop
for i in range(5):
  word = input("Guess a five letter word: ")
  if len(word)!=5:
    print("You entered an invalid guess.")
    continue
  response2 = requests.get(BASE_URL + '/get_feedback', json=word) #getting feedback from server
  data = response2.json()
  print("Your result is: ", data['result'])
  if data['result']=="OOOOO":
    win = True
    break
  num_guesses+=1
  if num_guesses==3 and not win: #hint option
    answer = input("Would you like a hint? (y/n) ")
    if answer=="y":
      response3 = requests.post(BASE_URL + '/request_hint', "1") #requesting hint if needed
      print("Your hint is: ", response3.json())
    else:
      continue
#End result messages
if win:
  print(win_end)
  end_msg = requests.post(BASE_URL+'/send_result', json="Client 2 successfully guessed your word!")
else:
  print("\n")
  print(lose_end)
  correct_word = requests.get(BASE_URL + '/get_word')
  print("The correct word was: "+correct_word.json())
  end_msg = requests.post(BASE_URL+'/send_result', json="Client 2 wasn't able to guess your word!")

done = requests.post(BASE_URL +'/finished_guessing', "1")

