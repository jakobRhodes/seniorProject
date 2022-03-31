#For python -m pip install pysimpleguiPySimpleGUI
from tkinter import *
from tkinter import ttk

#Imports
import random
import time
import logging
import sys
from weakref import finalize
#Randomize output every time
random.seed(time.time())
import PySimpleGUI as sg
import csv

#Variables
#Simulation Variables
villagers = 100
happiness = 100
#Program Variables
i = 0
savedChoices = []
savedUserInfo = ""
numberOfDecisions = 10
questionPool = []
choiceText = ""
minWindowSize = 300
header = []
theme = "DarkGreen5"
headerCreated = False

#Class to attach choices to the question.
class Question:
  def __init__(self, question, choiceA, choiceB, choiceC):
    self.question = question
    self.choiceA = choiceA
    self.choiceB = choiceB
    self.choiceC = choiceC
    self.used = False

#Class to attach points to each choice
class Choice:
  def __init__(self, text, happiness, villagers):
    self.text = text
    self.happiness = happiness
    self.villagers = villagers

#Populate Question Pool From File
with open('questions.txt') as f:
        contents = f.readlines()
for x in range(10):
  line = contents[i+1]
  line = line.split("#")
  c1 = Choice(line[0], line[1], line[2])
  line = contents[i+2]
  line = line.split("#")
  c2 = Choice(line[0], line[1], line[2])
  line = contents[i+3]
  line = line.split("#")
  c3 = Choice(line[0], line[1], line[2])
  q = Question(contents[i], c1, c2 ,c3)
  questionPool.append(q)
  i += 4
#Reset Index Variable so we can use it in the main program
i = 0

#Logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    handlers=[
        logging.FileHandler("debug.log"),
        logging.StreamHandler(sys.stdout)
    ]
)

#Functions
def getRandomUnusedQuestion():
  questionNumber = random.randint(0,len(questionPool)-1)
  question = questionPool[questionNumber]
  while (question.used == True):
    questionNumber = random.randint(0,len(questionPool)-1)
    question = questionPool[questionNumber]
  question.used = True
  return question

def resetQuestionPool():
  for x in questionPool:
    x.used = False
  
def saveToFile(filename, data):
  with open(filename + '.txt', 'a') as f:
    for line in data:
        f.write(line)
    f.write('\n')
  f.close()

def saveToCSVFile(data):
  with open('data.csv', 'a', encoding='UTF8', newline='') as f:
    writer = csv.writer(f)
    if (headerCreated == False):
      writer.writerow(header)
    writer.writerow(data)
  f.close()

def singleChoiceInputPrompt(title, text):
  sg.theme(theme)     
  layout = [sg.Text(text)],[sg.Text(title, size =(15, 1)), sg.InputText()],    [sg.Image(size=(300, 300), filename='robot.png', key="image")],[sg.Submit(), sg.Cancel()]
  window = sg.Window('User Info', layout, resizable=True, finalize=True)
  window.TKroot.minsize(minWindowSize, minWindowSize)
  event, values = window.read()
  window.close()
  return(values[0])

def titlePrompt():
  sg.theme(theme)     
  layout = [
    [sg.Text('Welcome to the AI Governor Program', auto_size_text=True)],
    [sg.Text('Choose to run the program for an AI or Human.', auto_size_text=True)],
    [sg.Image(size=(300, 300), filename='village.png', key="image")],
    [sg.Button("AI", key=f'BTN{0}', auto_size_button=True, size=(10, 5)), sg.Button("Human", key=f'BTN{1}', auto_size_button=True, size=(10, 5))],
    [sg.Text('Created By Jakob Rhodes', auto_size_text=True, justification="center")]
  ]
  window = sg.Window('Choose Mode', layout, resizable=True, finalize=True, element_justification='center')
  window.TKroot.minsize(minWindowSize, minWindowSize)
  event, values = window.read()
  window.close()
  return(event)  

def threeChoicePrompt(prompt, buttonText1, buttonText2, buttonText3):
  sg.theme(theme)  
  layout = [
    [sg.Text(prompt, justification="center", auto_size_text=True)], 
    [sg.Button(buttonText1, key=f'BTN{0}', auto_size_button=True, pad=(5,5))],
    [sg.Button(buttonText2, key=f'BTN{1}', auto_size_button=True, pad=(5,5))],
    [sg.Button(buttonText3, key=f'BTN{2}', auto_size_button=True, pad=(5,5))]
    ]
  window = sg.Window('Decision', layout, resizable=True, finalize=True, element_justification='center')
  window.TKroot.minsize(minWindowSize,minWindowSize)
  event, values = window.read()
  buttonText = window[event].get_text()
  window.close()
  return(event, buttonText) 

def display():
  sg.theme(theme) 
  score = happiness + villagers    
  layout = [
  [sg.Text('Number of Villagers Alive: ' + str(villagers), size =(30, 2))],
  [sg.Text('Happiness ' + str(happiness) + "%", size =(30, 2))],
  [sg.Text('Total Score = ' + str(score), size =(30, 2))]
  ]
  window = sg.Window('Results', layout, resizable=True, finalize=True)
  window.TKroot.minsize(minWindowSize,minWindowSize)
  event, values = window.read()
  window.close()

def applyChoice(choice, villagers, happiness):
  if choice == '1':
    villagers += int(randomQuestion.choiceA.villagers)
    happiness += int(randomQuestion.choiceA.happiness)
  elif choice == '2':
    villagers += int(randomQuestion.choiceB.villagers)
    happiness += int(randomQuestion.choiceB.happiness)
  elif choice == '3':
    villagers += int(randomQuestion.choiceC.villagers)
    happiness += int(randomQuestion.choiceC.happiness)
  return villagers, happiness

def promptForMode():
  mode = titlePrompt().split("N")[1]
  return mode

def promptForInfo():
  sg.theme(theme)     
  layout = [sg.Text("Name", size =(15, 1)), sg.InputText()],[sg.Text("Email ", size =(15, 1)), sg.InputText()],[sg.Image(size=(300, 300), filename='book.png', key="image")],[sg.Submit(), sg.Cancel()]
  window = sg.Window('User Info', layout, resizable=True, finalize=True, element_justification='c')
  window.TKroot.minsize(minWindowSize, minWindowSize)
  event, values = window.read()
  window.close()
  return(values[0])  

def decisionPrompt():
    decision, buttonText = threeChoicePrompt(randomQuestion.question, randomQuestion.choiceA.text, randomQuestion.choiceB.text, randomQuestion.choiceC.text)
    decision = decision.split("N")[1]
    decision = int(decision) + 1
    return str(decision), buttonText
def save():
  saveToFile("choiceText",choiceText)
  b = 0
  for q in savedChoices:
    header.append("Choice " + str((b + 1)))
    b += 1
  savedChoices.append(str(happiness))
  savedChoices.append(str(villagers))
  savedChoices.append(str(happiness + villagers))
  header.append("Happiness")
  header.append("Villagers")
  header.append("Final Score")
  saveToCSVFile(savedChoices)

#Program Starts here
#Decision Loop
#Human
if promptForMode() == '1':
  #Prompt and Save Users Details
  saveToFile("userInfo",promptForInfo())
  #Loop until we've made 10 Choices
  while i < numberOfDecisions:
    #Get a random question fron the question pool
    randomQuestion = getRandomUnusedQuestion()
    #Prompt for a choice and variable the results
    decision, buttonText = decisionPrompt()
    #Apply results of the choice made
    villagers, happiness = applyChoice(decision, villagers, happiness)
    #Save the text for future use
    choiceText += buttonText
    #Save the Choice Made
    savedChoices += decision
    #Iterate
    i += 1
  #Save the Choices Made to a File
  save()
  #Results Screen
  display()
else:
  #AI Mode
  #Button text not needed
  buttonText = ""
  #Prompt for how many sets you want it to complete
  numberOfRuns = int(singleChoiceInputPrompt("Runs","Enter number of Runs"))*10
  #logging.info(numberOfRuns)
  while i < numberOfRuns:
    #Get a random question fron the question pool
    randomQuestion = getRandomUnusedQuestion()
    #Currently random choice
    decision = random.randint(1,3)
    #Apply results of the choice made
    villagers, happiness = applyChoice(str(decision), villagers, happiness)
    #Save the text for future use
    choiceText += buttonText
    #Save the Choice Made
    savedChoices.append(str(decision))
    #Iterate
    i += 1
    #If we've made 10 choices save that set to a file
    if i % 10 == False:
      #ResetQuestionPool
      resetQuestionPool()
      #Save the Choices Made to a File
      logging.info("Saved a Run")
      save()
      headerCreated = True
      #Clear the choice list
      savedChoices = []
      #Reset our Simulation Variables
      villagers = 100
      happiness = 100



  
