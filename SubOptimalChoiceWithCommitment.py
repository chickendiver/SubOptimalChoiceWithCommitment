from sys import platform as _platform
from psychopy import visual, core, parallel, gui, event
import time, csv, random, datetime, os, logging, sys
import readPort

#Determine which OS is being used, and calculate the screen size
if _platform == "linux" or _platform == "linux2":
    # Linux
    import Tkinter
    
    root = Tkinter.Tk()

    screen_width = root.winfo_screenwidth()
    screen_height = root.winfo_screenheight()
    
    print("_width: " + str(screen_width) + "\n" + "height: " + str(screen_height))
    
elif _platform == "win32":
    # Windows...
   from win32api import GetSystemMetrics
   print "width =", GetSystemMetrics (0)
   print "height =",GetSystemMetrics (1) 
   screen_width = GetSystemMetrics (0)
   screen_height = GetSystemMetrics (1)

# Constants
# -------------------------------------------------------------------------------
  
L_X = (-1*(screen_width/3))
R_X = (screen_width/3)
I_STIM_Y = (-1*(screen_width/16))
CHOICE_Y = (screen_width/16)

# Time (in seconds) the hopper will stay up if the beam is not broken.
TIMEOUT_PERIOD = 60

#Time (in seconds) the hopper will stay up when the beam is broken
REWARD_TIME = 1

#Width of border around stimuli
LINE_WIDTH = 4

# Time of day at which experiment will start
# First element represents hours (24hr format)
# Second element represents minutes
# Set to 09:15
EXPERIMENT_START_TIME = [9, 15]

#Time (in seconds) the experiment will run
EXPERIMENT_TIME = 6300 #seconds = 105min

#A stimulus which can lead to one of two other stimuli
class ChoiceStim:
  def __init__(self, name):
          self.x = 0
          self.y = CHOICE_Y
          self.width = 100
          self.height = 100
          self.fillColour = "Gray"
          self.outlineColour = "Silver"
          self.name = name
          self.initStims = []

  def set_fill (self, fillCol):
        self.fillColour = fillCol

  def set_x (self, x):
        self.x = x

  def set_y (self, y):
        self.y = y

  def get_x(self):
        return self.x

  def get_y(self):
        return self.y
        
  def set_outline (self, outlineCol):
        self.outlineColour = outlineCol

  def add_initStim (self, stim):
        self.initStims.append(stim)

  def draw(self):
        global win

        if self.name == "ChoiceA":
          self.boundingBox = visual.Rect(win, lineWidth = LINE_WIDTH, width = self.width, height = self.height, pos = (self.x, self.y), units = "pix", lineColor = self.outlineColour, fillColor = "White")
          CCInnerCirc = visual.Circle(win, lineWidth = LINE_WIDTH, radius = 15, pos = (self.x, self.y), units = "pix", lineColor = "Black", fillColor = "Black")
          self.boundingBox.draw()
          CCInnerCirc.draw()

        elif self.name == "ChoiceB":
          self.boundingBox = visual.Rect(win, lineWidth = LINE_WIDTH, width = self.width, height = self.height, pos = (self.x, self.y), units = "pix", lineColor = self.outlineColour, fillColor = "White")
          CBInnerRect = visual.Rect(win, lineWidth = LINE_WIDTH, width = 30, height = 30, pos = (self.x, self.y), units = "pix", lineColor = "Black", fillColor = "White")
          self.boundingBox.draw()
          CBInnerRect.draw()

        elif self.name == "ChoiceC":
          topRight = (self.x + (self.width/2), self.y + (self.height/2))
          bottomLeft = (self.x - (self.width/2), self.y - (self.height/2))
          topLeft = (self.x - (self.width/2), self.y + (self.height/2))
          bottomRight = (self.x + (self.width/2), self.y - (self.height/2))

          self.boundingBox = visual.Rect(win, lineWidth = LINE_WIDTH, width = self.width, height = self.height, pos = (self.x, self.y), units = "pix", lineColor = self.outlineColour, fillColor = "White")
          CALine1 = visual.Line(win, start = (topRight), end = (bottomLeft), lineWidth = LINE_WIDTH, units = "pix", lineColor = "Black")
          CALine2 = visual.Line(win, start = (bottomRight), end = (topLeft), lineWidth = LINE_WIDTH, units = "pix", lineColor = "Black")
          self.boundingBox.draw()
          CALine1.draw()
          CALine2.draw()

        else:
          self.boundingBox = visual.Rect(win, lineWidth = 4, width = self.width, height = self.height, pos = (self.x, self.y), units = "pix", lineColor = self.outlineColour, fillColor = self.fillColour)
          self.boundingBox.draw()

#A stimulus which leads to one other stimulus, directly below it
class InitialLinkStim:
  def __init__(self, name):
          self.x = 0
          self.y = I_STIM_Y
          self.radius = 50
          self.fillColour = "Gray"
          self.outlineColour = "Silver"
          self.name = name
          self.termStims = []
          self.subOpt = False

  def set_subOpt(self, value):
        self.subOpt = value

  def get_subOpt():
         return self.subOpt

  def set_fill (self, fillCol):
        self.fillColour = fillCol
        
  def set_outline (self, outlineCol):
        self.outlineColour = outlineCol

  def add_termStim (self, stim):
        self.termStims.append(stim)

  def set_x (self, x):
        self.x = x

  def set_y (self, y):
        self.y = y

  def get_x(self):
        return self.x

  def get_y(self):
        return self.y

  def draw(self):
        global win

        if self.name == "InitA":
          self.boundingBox = visual.Circle(win, lineWidth = LINE_WIDTH, radius = self.radius, pos = (self.x, self.y), units = "pix", lineColor = self.outlineColour, fillColor = "White")
          InitAVertLine = visual.Line(win, start = (self.x, (self.y + self.radius)), end = (self.x, (self.y - self.radius)), lineWidth = LINE_WIDTH, units = "pix", lineColor = "Black")
          self.boundingBox.draw()
          InitAVertLine.draw()

        elif self.name == "InitB":
          topStart = ((self.x - 35), (self.y + 20))
          topEnd = ((self.x + 35), (self.y + 20))
          midStart = ((self.x - self.radius), (self.y))
          midEnd = ((self.x + self.radius), (self.y))
          bottomStart = ((self.x - 35), (self.y - 20))
          bottomEnd = ((self.x + 35), (self.y - 20))

          self.boundingBox = visual.Circle(win, lineWidth = LINE_WIDTH, radius = self.radius, pos = (self.x, self.y), units = "pix", lineColor = self.outlineColour, fillColor = "White")
          InitBTopLine = visual.Line(win, start = (topStart), end = (topEnd), lineWidth = LINE_WIDTH, units = "pix", lineColor = "Black")
          InitBMidLine = visual.Line(win, start = (midStart), end = (midEnd), lineWidth = LINE_WIDTH, units = "pix", lineColor = "Black")
          InitBBottomLine = visual.Line(win, start = (bottomStart), end = (bottomEnd), lineWidth = LINE_WIDTH, units = "pix", lineColor = "Black")
          self.boundingBox.draw()
          InitBTopLine.draw()
          InitBMidLine.draw()
          InitBBottomLine.draw()

        else:
          self.boundingBox = visual.Circle(win, lineWidth = LINE_WIDTH, radius = self.radius, pos = (self.x, self.y), units = "pix", lineColor = self.outlineColour, fillColor = self.fillColour)
          self.boundingBox.draw()

  def drawTermLinks(self):
          result = rollForTermResult(self)

          drawBlanksNoFlip(listOfBlanks)

          if result == 0:
            termStimShown = self.termStims[0]
            self.termStims[0].draw()
          else:
            termStimShown = self.termStims[1]
            self.termStims[1].draw()

          return termStimShown

#A stimulus which is presented and then holds for a particular period of time, regardless of input
class TerminalLinkStim:
  def __init__(self, name):
          self.x = 0
          self.y = I_STIM_Y
          self.radius = 50
          self.fillColour = "Gray"
          self.outlineColour = "Silver"
          self.name = name
          self.chanceOfReinforcement = 0


  def set_fill (self, fillCol):
        self.fillColour = fillCol

  def get_fill(self):
        return self.fillColour
        
  def set_outline (self, outlineCol):
        self.outlineColour = outlineCol

  def set_chanceOfReinforcement(self, chance):
        self.chanceOfReinforcement = chance

  def set_x (self, x):
        self.x = x

  def set_y (self, y):
        self.y = y

  def get_x(self):
        return self.x

  def get_y(self):
        return self.y

  def draw(self):
        global win

        if self.name == "TermA":
          self.fillColour = "Green"
        elif self.name == "TermB":
          self.fillColour = "Orange"
        elif self.name == "TermC":
          self.fillColour = "Red"
        elif self.name == "TermD":
          self.fillColour = "Purple"

        self.boundingBox = visual.Circle(win, lineWidth = LINE_WIDTH, radius = self.radius, pos = (self.x, self.y), units = "pix", lineColor = self.outlineColour, fillColor = self.fillColour)
        self.boundingBox.draw()
          
#Determine which terminal link is shown
def rollForTermResult(initialLink):
    global termResults1, termResults2, rolledABefore, rolledBBefore, index1, index2

    #reset the chance output array for stims of InitA
    if not rolledABefore:
      termResults1 = [0,0,1,1,1,
                      1,1,1,1,1]

      random.shuffle(termResults1)
      index1 = 0

    #reset the chance output array for stims of InitB
    if not rolledBBefore:
      termResults2 = [0,0,1,1,1,
                      1,1,1,1,1]
      random.shuffle(termResults2)
      index2 = 0

    rolledABefore = True
    rolledBBefore = True

    if initialLink.name == "InitA":
      result = termResults1[index1]
      index1 += 1

      if index1 == len(termResults1):
        rolledABefore = False

    elif initialLink.name == "InitB":
      result = termResults2[index2]
      index2 += 1

      if index2 == len(termResults2):
        rolledBBefore = False

    return result

# A rigged function for returning "1" or "0" 50% of the time.
# Save whether the function has been called before.
def rollDiceForFiftyFifty():
    global rolledFFBefore, FFResults, FFIndex

    if not rolledFFBefore:
        FFResults = [0,0,0,0,0,
                     1,1,1,1,1]

        random.shuffle(FFResults)
        FFIndex = -1

    rolledFFBefore = True

    FFIndex += 1

    if FFIndex == len(FFResults):
      random.shuffle(FFResults)
      FFIndex = -1

    return FFResults[FFIndex]

#Starts logging for admin purposes
def initialize_logger(output_dir):
    logger = logging.getLogger()
    logger.setLevel(logging.DEBUG)
     
    # create console handler and set level to info
    handler = logging.StreamHandler()
    handler.setLevel(logging.INFO)
    formatter = logging.Formatter("%(levelname)s - %(message)s")
    handler.setFormatter(formatter)
    logger.addHandler(handler)
 
    # create error file handler and set level to error
    handler = logging.FileHandler(os.path.join(output_dir, "error.log"),"w", encoding=None, delay="true")
    handler.setLevel(logging.ERROR)
    formatter = logging.Formatter("%(levelname)s - %(message)s")
    handler.setFormatter(formatter)
    logger.addHandler(handler)
 
    # create debug file handler and set level to debug
    handler = logging.FileHandler(os.path.join(output_dir, "all.log"),"w")
    handler.setLevel(logging.DEBUG)
    formatter = logging.Formatter("%(levelname)s - %(message)s")
    handler.setFormatter(formatter)
    logger.addHandler(handler)

#Creates window, sets up mouse, etc.
def setup():
    global win, mouse, rolledABefore, rolledBBefore, subjectNumber, datafile, writer, parallelPort, portValue, rolledFiftyFiftyBefore, trialNumber, birdAte

    logging.debug("Setting up...")
    
    #initialize the window
    win = visual.Window(fullscr = True, rgb = [-1.000,-1.000,-1.000], units = "pix", winType = "pyglet")

    #setup input from the mouse
    mouse = event.Mouse(visible = True)
    core.checkPygletDuringWait = True

    parallelPort = parallel.ParallelPort(address=0x0378)

    portValue = 0x0000
    turnOnFan()

    birdAte = False

    rolledABefore = False  
    rolledBBefore = False
    rolledFFBefore = False
    rolledFiftyFiftyBefore = False
    trialNumber = 0

    dataFolderPath = os.getcwd() + "\SubOptimal_Data_Logs"
    logging.debug(dataFolderPath)
    if not os.path.exists(dataFolderPath):
      os.makedirs(dataFolderPath)

    filename = dataFolderPath + '/' + (time.strftime("%d_%m_%Y")) + '_' + (time.strftime("%H_%M")) + '_' + 'Subject_' + str(subjectNumber) + '_data.csv'
    datafile = open(filename, 'wb')
    writer = csv.writer(datafile, delimiter=',')

    if condition == "Autoshaping (FR1)" or condition == "Operant Training (FR1)" or condition == "Operant Training (FR3)" or condition == "Operant Training (FR5)":

       writer.writerow(["ResearchAssistant", "SubjectNumber", "SetNumber",
                      "SessionNumber", "DateStarted", "Contingency",
                      "Condition", "PeckstoReward", "ProgramName", "TrialNumber",
                      "ProgramLoadTime", "BirdInBoxTime", "StartTime", 
                      "ExperimentEndTime", "ApparatusPresent",
                      "TimeoutPeriod", "RewardTime", "StimulusPresented", 
                      "StimulusSide", "ReactionTimes", "PeckNum", 
                      "ITI", "BirdAte"])

    else:
        writer.writerow(['ResearchAssistant', 'SubjectNumber', 'SetNumber', 
                         'SessionNumber', 'DateandTimeRun', 'Contingency', 
                         'Condition', 'NumberofPecksRequired', 'ProgramName', 
                         'TrialNumber', 'ProgramLoadTime', 'BirdInBoxTime', 
                         'ExperimentStartTime', 'ExperimentEndTime', 
                         'ApparatusPresent', 'TimeoutPeriod', 'RewardTime', 
                         'ChoiceStimulus', 'Initial-Link', 'Terminal-Link', 'Terminal-LinkColour',
                         'ChoiceStimulusSidePecked', 'Initial-LinkSidePecked', 
                         'ChoiceStimulusPecked',
                         'ChoiceStimulusReactionTime', 'Initial-LinkReactionTime', 
                         'Terminal-LinkPeckLog', 'TerminalLinkLatency', 
                         'Terminal-LinkFinalResponse', 'Terminal-LinkDuration', 
                         'Inter-TrialInterval(ITI)', 
                         'ChoiceStimulusScreenPeckCount', 
                         'InitialLinkScreenPeckCount', 
                         'Terminal-LinkScreenPeckCount', 'Sub-OptimalLinkChosen', 'BirdAte'])

# Creates all stimuli required, and sets them as global values
def createStimuli():
    global blankLeftChoiceStim, blankCentreChoiceStim, blankRightChoiceStim
    global blankLeftTermStim, blankRightTermStim, choiceA, choiceB, choiceC
    global initA, initB, termLinkA, termLinkB, termLinkC, termLinkD
    global listOfBlanks

    logging.debug("Creating stimuli...")

    listOfBlanks = []

    blankLeftChoiceStim = ChoiceStim("BlankL")
    blankCentreChoiceStim = ChoiceStim("BlankC")
    blankRightChoiceStim = ChoiceStim("BlankR")

    blankLeftChoiceStim.set_x(L_X)
    blankCentreChoiceStim.set_x(0)
    blankRightChoiceStim.set_x(R_X)

    blankLeftTermStim = TerminalLinkStim("BlankL")
    blankRightTermStim = TerminalLinkStim("BlankR")

    blankLeftTermStim.set_x(L_X)
    blankRightTermStim.set_x(R_X)

    listOfBlanks.append(blankLeftChoiceStim)
    listOfBlanks.append(blankCentreChoiceStim)
    listOfBlanks.append(blankRightChoiceStim)
    listOfBlanks.append(blankLeftTermStim)
    listOfBlanks.append(blankRightTermStim)

    choiceA = ChoiceStim("ChoiceA")
    choiceB = ChoiceStim("ChoiceB")
    choiceC = ChoiceStim("ChoiceC")

    initA = InitialLinkStim("InitA")
    initB = InitialLinkStim("InitB")

    termLinkA = TerminalLinkStim("TermA")
    termLinkB = TerminalLinkStim("TermB")
    termLinkC = TerminalLinkStim("TermC")
    termLinkD = TerminalLinkStim("TermD")


# Matches initial links with choice stimuli, 
# based on contingency.
def matchStimuli(contingency, reversal):

    logging.debug("Matching Stimuli...")

    if contingency == "1":
        choiceA.set_x(L_X)
        choiceB.set_x(R_X)

        initA.set_x(L_X)
        initB.set_x(R_X)

        termLinkA.set_x(L_X)
        termLinkB.set_x(L_X)
        termLinkC.set_x(R_X)
        termLinkD.set_x(R_X)

        if reversal == False:
          termLinkA.set_chanceOfReinforcement(1)
          termLinkB.set_chanceOfReinforcement(0)
          termLinkC.set_chanceOfReinforcement(0.5)
          termLinkD.set_chanceOfReinforcement(0.5)

        elif reversal == True:
          termLinkA.set_chanceOfReinforcement(0.5)
          termLinkB.set_chanceOfReinforcement(0.5)
          termLinkC.set_chanceOfReinforcement(1)
          termLinkD.set_chanceOfReinforcement(0)


        choiceA.add_initStim(initA)
        choiceB.add_initStim(initB)
        choiceC.add_initStim(initA) 
        choiceC.add_initStim(initB)

        initA.add_termStim(termLinkA)
        initA.add_termStim(termLinkB)
        initB.add_termStim(termLinkC)
        initB.add_termStim(termLinkD)

    elif contingency == "2":
        choiceA.set_x(R_X)
        choiceB.set_x(L_X)

        initA.set_x(L_X)
        initB.set_x(R_X)

        termLinkA.set_x(L_X)
        termLinkB.set_x(R_X)
        termLinkC.set_x(R_X)
        termLinkD.set_x(L_X)

        if reversal == False:
          termLinkA.set_chanceOfReinforcement(0)
          termLinkB.set_chanceOfReinforcement(0.5)
          termLinkC.set_chanceOfReinforcement(0.5)
          termLinkD.set_chanceOfReinforcement(1)

        elif reversal == True:
          termLinkA.set_chanceOfReinforcement(0.5)
          termLinkB.set_chanceOfReinforcement(1)
          termLinkC.set_chanceOfReinforcement(0)
          termLinkD.set_chanceOfReinforcement(0.5)

        choiceA.add_initStim(initB)
        choiceB.add_initStim(initA)
        choiceC.add_initStim(initA)
        choiceC.add_initStim(initB)

        initA.add_termStim(termLinkD)
        initA.add_termStim(termLinkA)
        initB.add_termStim(termLinkB)
        initB.add_termStim(termLinkC)
        
    elif contingency == "3":
        choiceA.set_x(L_X)
        choiceB.set_x(R_X)

        initA.set_x(R_X)
        initB.set_x(L_X)

        termLinkA.set_x(R_X)
        termLinkB.set_x(R_X)
        termLinkC.set_x(L_X)
        termLinkD.set_x(L_X)

        if reversal == False:
          termLinkA.set_chanceOfReinforcement(0.5)
          termLinkB.set_chanceOfReinforcement(0.5)
          termLinkC.set_chanceOfReinforcement(1)
          termLinkD.set_chanceOfReinforcement(0)

        elif reversal == True:
          termLinkA.set_chanceOfReinforcement(1)
          termLinkB.set_chanceOfReinforcement(0)
          termLinkC.set_chanceOfReinforcement(0.5)
          termLinkD.set_chanceOfReinforcement(0.5)

        choiceA.add_initStim(initB)
        choiceB.add_initStim(initA)
        choiceC.add_initStim(initA)
        choiceC.add_initStim(initB)

        initA.add_termStim(termLinkA)
        initA.add_termStim(termLinkB)
        initB.add_termStim(termLinkC)
        initB.add_termStim(termLinkD)

    elif contingency == "4":
        choiceA.set_x(R_X)
        choiceB.set_x(L_X)

        initA.set_x(R_X)
        initB.set_x(L_X)

        termLinkA.set_x(R_X)
        termLinkB.set_x(L_X)
        termLinkC.set_x(L_X)
        termLinkD.set_x(R_X)

        if reversal == False:
          termLinkA.set_chanceOfReinforcement(0.5)
          termLinkB.set_chanceOfReinforcement(1)
          termLinkC.set_chanceOfReinforcement(0)
          termLinkD.set_chanceOfReinforcement(0.5)

        elif reversal == True:
          termLinkA.set_chanceOfReinforcement(1)
          termLinkB.set_chanceOfReinforcement(0.5)
          termLinkC.set_chanceOfReinforcement(0.5)
          termLinkD.set_chanceOfReinforcement(0)

        choiceA.add_initStim(initA)
        choiceB.add_initStim(initB)
        choiceC.add_initStim(initA)
        choiceC.add_initStim(initB)

        initA.add_termStim(termLinkD)
        initA.add_termStim(termLinkA)
        initB.add_termStim(termLinkB)
        initB.add_termStim(termLinkC)

# Makes a list of choice stimuli, returns the list
def makeChoiceStimList():
    logging.debug("Randomizing choice stimuli...")

    choiceList = []

    choiceList1 = [choiceA, choiceB]
    choiceList2 = [choiceA, choiceC]
    choiceList3 = [choiceB, choiceC]

    for i in range(0,20):
      # 20 of each type of forced choice
      choiceList.append([choiceA])
      choiceList.append([choiceB])
      choiceList.append([choiceC])

      # 40 of each type of choice 
      choiceList.append(choiceList1)
      choiceList.append(choiceList2)
      choiceList.append(choiceList3)
      choiceList.append(choiceList1)
      choiceList.append(choiceList2)
      choiceList.append(choiceList3)

    random.shuffle(choiceList)

    return choiceList

# Draws blank stimuli, but doesn't present them. 
# Must be used in conjunction with another stimulus
# presentation function
def drawBlanksNoFlip(stimuli):
    for i in range(0,len(stimuli)):
        stimuli[i].draw()

# Draws each stimuli in "stimuli"
def drawStims(stimuli):
    logging.debug("Drawing stimuli...")

    if len(stimuli) != len(listOfBlanks):
        drawBlanksNoFlip(listOfBlanks)

    for i in range(0,len(stimuli)):
      stimuli[i].draw()

    win.flip()

# Waits for input on any object provided in "Stimuli"
# Returns after "targetPeckRequired" number of clicks on
# stimuli is reached.
def waitForClicks(targetPeckRequired, stimuli, duration):

    logging.debug("Waiting for clicks...")
    peckNum = 0
    targetPeckNum = 0
    targetPecked = ""
    oldMouseIsDown = True

    targetFlag = False
    reactionTimes = []
    reactionTimer = core.Clock()
    stimTimer = core.CountdownTimer(duration)
    
    while ((stimTimer.getTime() > 0) and (targetFlag == False)):
      #event.clearEvents('mouse')
      #mouse.clickReset()

      mouseIsDown = mouse.getPressed()[0]
      mouse.clickReset()

      if mouseIsDown and not oldMouseIsDown:

          # Add click reaction times to list.
          reactionTimes.append(reactionTimer.getTime())
          pos = mouse.getPos()
          logging.debug(pos)

          for i in range (0,len(stimuli)):
            if stimuli[i].getBoundingBox().contains(pos):
              targetPeckNum += 1
              if targetPeckNum >= targetPeckRequired:
                targetFlag = True
                targetPecked = stimuli[i]
                break

          reactionTimer.reset()
          peckNum += 1
       
      oldMouseIsDown = mouseIsDown

      if event.getKeys(["escape"]):
        logging.debug("User pressed escape")
        exit()


    return targetPecked, targetFlag, peckNum, reactionTimes

# Waits for the user to press the escape key
# Used for ITI waiting
# When time is 0, loop will go infinitely
# Every other value of time will start a counter for that length of time (in s)
def waitForExitPress(time = 0):
  logging.debug("Waiting for exit key to be pressed")
  if time == 0:
    while True:
      if event.getKeys(["escape"]):
            logging.debug("User pressed escape")
            exit()
  else:
    waitTimer = core.CountdownTimer(time) 
    while (waitTimer.getTime() > 0):
      if event.getKeys(["escape"]):
            logging.debug("User pressed escape")
            exit()

# Displays a blank screen and waits for the escape key
def displayEndScreen():
  logging.debug("Displaying end screen")
  drawBlanksNoFlip(listOfBlanks)
  spacebarText = visual.TextStim(win, text='Experiment Ended. Press ESC to exit.', alignHoriz = 'center', alignVert = 'bottom')
  spacebarText.draw()
  win.flip()
  waitForExitPress()
  
# Probabilities:
# 1 = 100%
# 0.5 = 50%
# 0 = no reward
def giveReward(probability):
  global fiftyFifty, fiftyFiftyIndex, rolledFiftyFiftyBefore, birdAte
  hopperDropped = ""
  if apparatusPresent:
    if probability == 1:
      logging.debug("Reward given with probability of: ", probability)
      hopperDropped = dropHoppersAtRandom()

    elif probability == 0.5:
      if not rolledFiftyFiftyBefore:
        fiftyFifty = [0,0,0,0,0,
                      1,1,1,1,1]

        random.shuffle(fiftyFifty)
        rolledFiftyFiftyBefore = True
        fiftyFiftyIndex = -1
      
      fiftyFiftyIndex += 1
      if fiftyFifty[fiftyFiftyIndex] == 1:
        hopperDropped = dropHoppersAtRandom()
        logging.debug("Reward given with probability of: " + str(probability))
      else:
        logging.debug("Reward not given")
        probability = 0
        # In place of 1 second of hopper access
        core.wait(REWARD_TIME)

    else:
      logging.debug("Reward not given")
      # In place of 1 second of hopper access
      core.wait(REWARD_TIME)

    if probability > 0:

      birdAte = False
      hopperTimer = core.CountdownTimer(TIMEOUT_PERIOD)

      # Read IR beam

      if hopperDropped == "L":

        while (hopperTimer.getTime() > 0):
          core.wait(0.1)
          irValue = readLeftHopperBeam()
          if irValue == 0:
              birdAte = True
              break
        
        ## 1 second of hopper access
        core.wait(REWARD_TIME)
        dropLeftHopper()

      else:
      # Assume right hopper was dropped
        while (hopperTimer.getTime() > 0):
          core.wait(0.1)
          irValue = readRightHopperBeam()
          if irValue == 0:
              birdAte = True
              break

        ## 1 second of hopper access
        core.wait(REWARD_TIME)
        dropRightHopper()
 
  else:
    logging.debug("Apparatus not present")

    ## FIX: MAKE THIS CODE MORE CONDENSED.
    if probability == 1:
      logging.debug("Reward given with probability of: " + str(probability))

    elif probability == 0.5:
      if not rolledFiftyFiftyBefore:
        fiftyFifty = [0,0,0,0,0,
                      1,1,1,1,1]

        random.shuffle(fiftyFifty)
        rolledFiftyFiftyBefore = True
        fiftyFiftyIndex = -1
      
      fiftyFiftyIndex += 1
      if fiftyFiftyIndex == (len(fiftyFifty) -1):
        rolledFiftyFiftyBefore = False

      if fiftyFifty[fiftyFiftyIndex] == 1:
        logging.debug("Reward given with probability of: " + str(probability))
      else:
        logging.debug("Reward not given")
        probability = 0

    else:
      logging.debug("Reward not given")
      # In place of 1 second of hopper access
      core.wait(REWARD_TIME)

    if probability > 0:
      
      birdAte = True

# Randomly chooses a hopper to drop.
# Call this function when it doesn't matter which hopper is dropped
def dropHoppersAtRandom():
  chanceArray = [0,1]
  random.shuffle(chanceArray)
  if chanceArray[0] == 1:
    raiseLeftHopper()
    hopperDropped = "L"
  else:
    raiseRightHopper()
    hopperDropped = "R"

  logging.debug("Hopper dropped: " + str(hopperDropped))
  return hopperDropped

# Raises the hopper and turns the light on.
def raiseLeftHopper():
  global portValue
  portValue = portValue | (0x0010)
  portValue = portValue | (0x0004)

  parallelPort.setData(portValue)

# Raises the hopper and turns the light on.
def dropLeftHopper():
  global portValue
  portValue = portValue & ~(0x0010)
  portValue = portValue & ~(0x0004)

  parallelPort.setData(portValue)

def raiseRightHopper():
  global portValue
  portValue = portValue | (0x0020)
  portValue = portValue | (0x0008)

  parallelPort.setData(portValue)

def dropRightHopper():
  global portValue
  portValue = portValue & ~(0x0020)
  portValue = portValue & ~(0x0008)

  parallelPort.setData(portValue)

def turnOnHouseLight():
  global portValue
  portValue = portValue | (0x0001)

  parallelPort.setData(portValue)

def turnOffHouseLight():
  global portValue
  portValue = portValue & ~(0x0001)

  parallelPort.setData(portValue)

def turnOnFan():
  global portValue
  portValue = portValue | (0x0002)

  parallelPort.setData(portValue)

def turnOffFan():
  global portValue
  portValue = portValue & ~(0x0002)

  parallelPort.setData(portValue)

# Reads from left IR beam. Called after hopper is dropped
def readLeftHopperBeam():
  #return if beam broken

  value = readPort.readPort(0x0201) & (0x20)
  logging.debug("LEFT IR: " + str(value))
  return value

# Reads from right IR beam. Called after hopper is dropped
def readRightHopperBeam():
  #return if beam broken
  
  value = readPort.readPort(0x0201) & (0x10)
  logging.debug("RIGHT IR: " + str(value))
  return value

#Reads IR beam status on port 0x0201 (GamePort)
def checkForApparatus():
  #return True if apparatus present, False otherwise

  logging.debug("Checking for apparatus")
  value = readPort.readPort(0x0201)
  logging.debug("Apparatus value " + str(value))
  if value == 0x00ff:
    return True
  else:
    return False

def waitForTermLinks():

  logging.debug("Waiting for terminal clicks...")
  peckNum = 0
  oldMouseIsDown = True

  reactionTimes = []
  reactionTimer = core.Clock()
  stimTimer = core.CountdownTimer(TERM_DUR)
  stimTimer.reset()
  while (stimTimer.getTime() > 0):

    mouseIsDown = mouse.getPressed()[0]
    mouse.clickReset()

    if mouseIsDown and not oldMouseIsDown:

        # Add click reaction times to list.
        reactionTimes.append(reactionTimer.getTime())
        reactionTimer.reset()
        pos = mouse.getPos()
        logging.debug(pos)

        peckNum += 1
     
    oldMouseIsDown = mouseIsDown

    if event.getKeys(["escape"]):
      logging.debug("User pressed escape")
      exit()

  return peckNum, reactionTimes


# Main experimental phase. Reversal changes chance of reinforcement.
def doExperimentalPhase():
    logging.debug("Starting experimental phase...")
    global birdAte

    createStimuli()
    matchStimuli(contingency, reversal)
    stimList = makeChoiceStimList()

    startTime = time.time()
    expTimer = core.CountdownTimer(EXPERIMENT_TIME)

    trialNumber = 0

    print("StimList Len: " + str(len(stimList)))
    logging.debug("StimList Length " +  str(len(stimList)))

    for i in range(0,len(stimList)):
        choicePeckNum = 0
        initPeckNum = 0

        trialNumber += 1
        if (expTimer.getTime() <= 0):
          break
        drawStims(stimList[i])
        cStimPecked, cClickFlag, cPeckNum, cReactionTimes = waitForClicks(1, stimList[i], expTimer.getTime())
        if cClickFlag == True:
          drawStims(cStimPecked.initStims)
          iStimPecked, iClickFlag, iPeckNum, iReactionTimes = waitForClicks(1, cStimPecked.initStims, expTimer.getTime())
          if iClickFlag == True:
            termStimShown = iStimPecked.drawTermLinks()
            win.flip()

            tPeckNum, tReactionTimes = waitForTermLinks()

            drawStims(listOfBlanks) #Display blank stimuli for duration of ITI
            
            birdAte = False
            giveReward(termStimShown.chanceOfReinforcement)
            
          
        cStimSide = ""
        iStimSide = ""
        if cClickFlag == True:
          if cStimPecked.get_x() == L_X:
            cStimSide = "LEFT"
          elif cStimPecked.get_x() == R_X:
            cStimSide = "RIGHT"
          elif cStimPecked.get_x() == 0:
            cStimSide = "CENTRE"
        else:
          cStimSide = "NO STIM PECKED"

        if cClickFlag == True:
          if iStimPecked.get_x() == L_X:
            iStimSide = "LEFT"
          elif iStimPecked.get_x() == R_X:
            iStimSide = "RIGHT"
          elif iStimPecked.get_x() == 0:
            iStimSide = "CENTRE"
        else:
          iStimSide = "NO STIM PECKED"
        
        # FIX: Verify this value
        subOptChosen = termStimShown.chanceOfReinforcement != 0.5

        cStimPresented = ""
        for j in range(0, len(stimList[i])):
          cStimPresented += stimList[i][j].name + " "

        iStimPresented = ""
        for h in range(0, len(cStimPecked.initStims)):
          iStimPresented += cStimPecked.initStims[h].name + " "

        if len(tReactionTimes) == 0:
          tReactionTimes.append("")
          sumReactionTimes = ""
        else:
          sumReactionTimes = sum(tReactionTimes)

        tPeckLog = ""
        for m in range(0, len(tReactionTimes)):
          if m == 0:
            tPeckLog = str(tReactionTimes[m])
          else:
            tPeckLog = tPeckLog + ", " + str(tReactionTimes[m])

        cReactTimeStr = ""
        for k in range(0, len(cReactionTimes)):
          if k == 0:
            cReactTimeStr = str(cReactionTimes[k])
          else:
            cReactTimeStr = cReactTimeStr + ", " + str(cReactionTimes[k])

        iReactTimeStr = ""
        for l in range(0, len(iReactionTimes)):
          if l == 0:
            iReactTimeStr = str(iReactionTimes[l])
          else:
            iReactTimeStr = iReactTimeStr + ", " + str(iReactionTimes[l])


        logging.debug(str(expTimer.getTime()))
        writer.writerow([researchAssistant, subjectNumber, setNumber,
                      sessionNumber, dateStarted + " " + timeStarted, contingency,
                      condition, "1", programName, trialNumber,
                      programLoadTime, birdInBoxTime, experimentStartTime, 
                      "", apparatusPresent,
                      TIMEOUT_PERIOD, REWARD_TIME, cStimPresented,
                      iStimPresented, termStimShown.name, termStimShown.get_fill(),
                      cStimSide, iStimSide,
                      cStimPecked.name, cReactTimeStr, iReactTimeStr, tPeckLog,
                      tReactionTimes[0], sumReactionTimes, TERM_DUR,
                      ITI, cPeckNum, iPeckNum, tPeckNum, subOptChosen, birdAte])

        waitForExitPress(ITI)

    endTime = time.strftime("%H:%M")
    logging.debug(str(endTime))

    writer.writerow([researchAssistant, subjectNumber, setNumber,
                      sessionNumber, dateStarted + " " + timeStarted, contingency,
                      condition, "1", programName, "", 
                      programLoadTime, birdInBoxTime, experimentStartTime, 
                      endTime, apparatusPresent,
                      TIMEOUT_PERIOD, REWARD_TIME, "",
                      "", "", "",
                      "", "",
                      "", "", "", "",
                      "", "", TERM_DUR,
                      ITI, "", "", "", "", ""])

    drawStims(listOfBlanks)
    waitForExitPress(expTimer.getTime())

    displayEndScreen()

# Generates a list of initial link stimuli choices
def makeInitStimList():
    logging.debug("Randomizing init stimuli...")

    initList = []

    initList1 = [initA, initB]

    for i in range(0,40):
      # 40 of each forced choice
      initList.append([initA])
      initList.append([initB])

      # 80 choice trials
      initList.append(initList1)
      initList.append(initList1)

    random.shuffle(initList)

    return initList

# Stimulus pairing phase.
def doStimPairing():
    global birdAte

    createStimuli()
    matchStimuli(contingency, reversal)
    stimList = makeInitStimList()

    trialNumber = 0
    startTime = time.time()
    expTimer = core.CountdownTimer(EXPERIMENT_TIME)

    for i in range(0,len(stimList)):
        trialNumber += 1
        if (expTimer.getTime() <= 0):
          break
        drawStims(stimList[i])
        iStimPecked, iClickFlag, iPeckNum, iReactionTimes = waitForClicks(1, stimList[i], expTimer.getTime())
        if iClickFlag == True:
          termStimShown = iStimPecked.drawTermLinks()
          win.flip()

          tPeckNum, tReactionTimes = waitForTermLinks()
          
          drawStims(listOfBlanks) #Display blank stimuli for duration of ITI

          birdAte = False
          giveReward(termStimShown.chanceOfReinforcement)
          

          if iClickFlag == True:
            if iStimPecked.get_x() == L_X:
              iStimSide = "LEFT"
            elif iStimPecked.get_x() == R_X:
              iStimSide = "RIGHT"
            elif iStimPecked.get_x() == 0:
              iStimSide = "CENTRE"
          else:
            iStimSide = "NO STIM PECKED"
          
          # FIX: Verify this value
          subOptChosen = termStimShown.chanceOfReinforcement != 0.5

          stimPresented = ""
          for j in range(0, len(stimList[i])):
            stimPresented += stimList[i][j].name + " "

          termStimPresented = termStimShown.name

          if len(tReactionTimes) == 0:
            tReactionTimes.append("")
            sumReactionTimes = ""
          else:
            sumReactionTimes = sum(tReactionTimes)
          tPeckLog = ""

          for m in range(0, len(tReactionTimes)):
            if m == 0:
              tPeckLog = str(tReactionTimes[m])
            else:
              tPeckLog = tPeckLog + ", " + str(tReactionTimes[m])

          iReactTimeStr = ""
          for l in range(0, len(iReactionTimes)):
            if l == 0:
              iReactTimeStr = str(iReactionTimes[l])
            else:
              iReactTimeStr = iReactTimeStr + ", " + str(iReactionTimes[l])

          writer.writerow([researchAssistant, subjectNumber, setNumber,
                        sessionNumber, dateStarted + " " + timeStarted, contingency,
                        condition, "1", programName, trialNumber,
                        programLoadTime, birdInBoxTime, experimentStartTime, 
                        "", apparatusPresent,
                        TIMEOUT_PERIOD, REWARD_TIME, "",
                        stimPresented, termStimPresented, termStimShown.get_fill(),
                        "", iStimSide,
                        "", "", iReactTimeStr, tPeckLog,
                        tReactionTimes[0], sumReactionTimes, TERM_DUR,
                        ITI, "", iPeckNum, tPeckNum, subOptChosen, birdAte])

          waitForExitPress(ITI)

    endTime = time.strftime("%H:%M")

    writer.writerow([researchAssistant, subjectNumber, setNumber,
                      sessionNumber, dateStarted + " " + timeStarted, contingency,
                      condition, "1", programName, "",
                      programLoadTime, birdInBoxTime, experimentStartTime, 
                      endTime, apparatusPresent,
                      TIMEOUT_PERIOD, REWARD_TIME, "",
                      "", "", "",
                      "", "",
                      "", "", "", "",
                      "", "", TERM_DUR,
                      ITI, "", "", "", "", ""])

    drawStims(listOfBlanks)
    waitForExitPress(expTimer.getTime())

    displayEndScreen()

# Generates randomized list of stimuli for experiments with
# Multiple stimuli presented at once.
def generateListOfAllStims():

  LChoiceA = ChoiceStim("ChoiceA")
  LChoiceA.set_x(L_X)
  CChoiceA = ChoiceStim("ChoiceA")
  RChoiceA = ChoiceStim("ChoiceA")
  RChoiceA.set_x(R_X)
  LChoiceB = ChoiceStim("ChoiceB")
  LChoiceB.set_x(L_X)
  CChoiceB = ChoiceStim("ChoiceB")
  RChoiceB = ChoiceStim("ChoiceB")
  RChoiceB.set_x(R_X)
  LChoiceC = ChoiceStim("ChoiceC")
  LChoiceC.set_x(L_X)
  CChoiceC = ChoiceStim("ChoiceC")
  RChoiceC = ChoiceStim("ChoiceC")
  RChoiceC.set_x(R_X)

  LinitA = InitialLinkStim("InitA")
  LinitA.set_x(L_X)
  RinitA = InitialLinkStim("InitA")
  RinitA.set_x(R_X)
  LinitB = InitialLinkStim("InitB")
  LinitB.set_x(L_X)
  RinitB = InitialLinkStim("InitB")
  RinitB.set_x(R_X)

  LtermLinkA = TerminalLinkStim("TermA")
  LtermLinkA.set_x(L_X)
  RtermLinkA = TerminalLinkStim("TermA")
  RtermLinkA.set_x(R_X)
  LtermLinkB = TerminalLinkStim("TermB")
  LtermLinkB.set_x(L_X)
  RtermLinkB = TerminalLinkStim("TermB")
  RtermLinkB.set_x(R_X)
  LtermLinkC = TerminalLinkStim("TermC")
  LtermLinkC.set_x(L_X)
  RtermLinkC = TerminalLinkStim("TermC")
  RtermLinkC.set_x(R_X)
  LtermLinkD = TerminalLinkStim("TermD")
  LtermLinkD.set_x(L_X)
  RtermLinkD = TerminalLinkStim("TermD")
  RtermLinkD.set_x(R_X)

  stimList = [[LChoiceA], [CChoiceA], [RChoiceA],
              [LChoiceB], [CChoiceB], [RChoiceB],
              [LChoiceC], [CChoiceC], [RChoiceC],
              [LinitA], [RinitA],
              [LinitB], [RinitB],
              [LtermLinkA], [RtermLinkA],
              [LtermLinkB], [RtermLinkB],
              [LtermLinkC], [RtermLinkC],
              [LtermLinkD], [RtermLinkD]]

  random.shuffle(stimList)
  return stimList

# Operant Training. "pecksToReward" signifsties the FR schedule.
def doTraining(ITI, pecksToReward, rewardIfNotPecked):

  createStimuli()
  trialNumber = 0

  expTimer = core.CountdownTimer(EXPERIMENT_TIME)

  while (expTimer.getTime() > 0):

    stimList = generateListOfAllStims()

    for i in range(0, len(stimList)):
      trialNumber += 1

      if (expTimer.getTime() <= 0):
            break

      drawStims(stimList[i])
      logging.debug("stimdur: " + str(stimDur))
      stimPecked, clickFlag, peckNum, reactionTimes = waitForClicks(pecksToReward, stimList[i], stimDur)

      if rewardIfNotPecked or clickFlag:
        giveReward(1)

      drawStims(listOfBlanks) #Display blank stimuli for duration of ITI

      if clickFlag == True:
        if stimPecked.get_x() == L_X:
          stimSide = "LEFT"
        elif stimPecked.get_x() == R_X:
          stimSide = "RIGHT"
        elif stimPecked.get_x() == 0:
          stimSide = "CENTRE"
        else:
          stimSide = "UNKOWN"
      else:
          stimSide = "NO STIM PECKED"

      stimPresented = ""
      for j in range(0, len(stimList[i])):
        stimPresented += stimList[i][j].name + " "

      reactTimeStr = ""
      for k in range(0, len(reactionTimes)):
        if k == 0:
          reactTimeStr = str(reactionTimes[k])
        else:
          reactTimeStr = reactTimeStr + ", " + str(reactionTimes[k])

      writer.writerow([researchAssistant, subjectNumber, setNumber,
                        sessionNumber, dateStarted + " " + timeStarted, contingency,
                        condition, pecksToReward, programName, trialNumber,
                        programLoadTime, birdInBoxTime, experimentStartTime, 
                        "", apparatusPresent,
                        TIMEOUT_PERIOD, REWARD_TIME, stimPresented, 
                        stimSide, reactTimeStr, peckNum, 
                        ITI])

      waitForExitPress(ITI)

      if event.getKeys(keyList=["escape"]):
          logging.debug("User pressed escape")
          exit()

  endTime = time.strftime("%H:%M")

  writer.writerow([researchAssistant, subjectNumber, setNumber,
                   sessionNumber, dateStarted + " " + timeStarted, contingency,
                   condition, pecksToReward, programName, "",
                   programLoadTime, birdInBoxTime, experimentStartTime, 
                   endTime, apparatusPresent,
                   TIMEOUT_PERIOD, REWARD_TIME, "", 
                   "", "", "", 
                   ITI])

  displayEndScreen()



# Creates GUI for experiment details
# Returns an array of all responses, and whether the user has pressed "Cancel"
def getUserInput():
    userCancelled = False
    myDlg = gui.Dlg(title="Sub-Optimal Choice with Commitment", labelButtonOK=' START ')
    myDlg.addField('Subject number:', 0)
    myDlg.addField('Session number:', 0)
    myDlg.addField('Set number:', 0)
    myDlg.addField('Condition:', choices = ['Autoshaping (FR1)', 'Operant Training (FR1)', 'Operant Training (FR3)', 'Operant Training (FR5)', 'Stim Pairing', 'Experimental Phase', 'Experimental Reversal'])
    myDlg.addField('Contingency:', choices = ['1', '2', '3', '4'])
    myDlg.addField('Stimulus Timeout:', 60)
    myDlg.addField('Is this a test?:', choices = ['Yes', 'No'])
    myDlg.addField('Research Assistant:')
    myDlg.show()  # show dialog and wait for OK or Cancel
    
    if myDlg.OK:  # User pressed "Start"
        experimentParameters = myDlg.data
        print experimentParameters
    else: # User pressed "Cancel"
        logging.debug('user cancelled')
        experimentParameters = []
        userCancelled = True

    return experimentParameters, userCancelled

#Waits for spacebar input from user for indefinite period of time
def waitForSpacebar():

  while True:
    if event.getKeys(["space"]):
      logging.debug("User pressed spacebar")
      break

#Timer function which only allows the experiment to be run at a certain time
def waitForExperiment():
  bibTextContent = "Bird in Box --- Waiting until " + str(EXPERIMENT_START_TIME[0]) + ":" + str(EXPERIMENT_START_TIME[1])
  bibText =visual.TextStim(win, text=bibTextContent, pos=(0.0, 500), alignVert = "top")
  bibText.draw()
  win.flip()


  while True:
    if (time.localtime()[3] == EXPERIMENT_START_TIME[0]):
      if (time.localtime()[4] >= EXPERIMENT_START_TIME[1]):
        break
    elif (time.localtime()[3] > EXPERIMENT_START_TIME[0]):
      break
    if event.getKeys(["escape"]):
        logging.debug("User pressed escape")
        exit()


# Turns all inputs into global variables, sets up experiment, and decides
# which experimental phase to call.
def main():
    global ITI, contingency, reversal, subjectNumber, apparatusPresent, TERM_DUR
    global subjectNumber, sessionNumber, condition, contingency
    global stimulusTimeout, testRunFlag, researchAssistant
    global dateStarted, timeStarted, programStartTime, birdInBoxTime
    global programLoadTime, setNumber, programName, experimentStartTime, stimDur
 
    initialize_logger('./')
     
    logging.debug("debug message")
    logging.info("info message")
    logging.warning("warning message")
    logging.error("error message")
    logging.critical("critical message")

    logging.info('\n\n\n' + (time.strftime("%d_%m_%Y @ ")) + (time.strftime("%H:%M")) + ':\n\n')

    userResponses, userCancelled = getUserInput()

    if userCancelled == True:
      exit()

    subjectNumber = userResponses[0]
    sessionNumber = userResponses[1]
    setNumber = userResponses[2]
    condition = userResponses[3]
    contingency = userResponses[4]
    stimDur = userResponses[5]
    testRunFlag = userResponses[6]
    researchAssistant = userResponses[7]

    programName = "SubOptimalChoiceWithCommitment.py"

    if len(researchAssistant) == 0:
      researchAssistant = "Unlisted"

    if checkForApparatus() == True:
      apparatusPresent = True
    else:
      apparatusPresent = False

    #Timestamp of when program is run
    dateStarted = time.strftime("%d_%m_%Y") 
    timeStarted = time.strftime("%H:%M")

    try: 
      setup()
    except:
      e = sys.exc_info()[0]
      
      if type(e) != type(SystemExit):
        logging.exception(e)
        raise

    if testRunFlag == "Yes":
      ITI = 2
      TERM_DUR = 2
      mouse.setVisible(1)
    else:
      ITI = 10
      TERM_DUR = 10
      mouse.setVisible(0)

    try:
      programLoadTime = time.strftime("%H:%M")
      spacebarText =visual.TextStim(win, text='Press spacebar to begin', alignHoriz = 'center', alignVert = 'center')
      spacebarText.draw()
      win.flip()
      waitForSpacebar()

      if testRunFlag == "No":
        waitForExperiment()

      birdInBoxTime = time.strftime("%H:%M")
    except:
      e = sys.exc_info()[0]
      
      if type(e) != type(SystemExit):
        logging.exception(e)
        raise

    try:
      experimentStartTime = time.strftime("%H:%M")
      if condition == 'Autoshaping (FR1)':
        if testRunFlag == "Yes":
          doTraining(5, 1, True)
        else:
          doTraining(240, 1, True)
      elif condition == 'Operant Training (FR1)':
        if testRunFlag == "Yes":
          doTraining(5, 1, False)
        else:
          doTraining(60, 1, False)
      elif condition == 'Operant Training (FR3)':
        if testRunFlag == "Yes":
          doTraining(5, 3, False)
        else:
          doTraining(60, 3, False)
      elif condition == 'Operant Training (FR5)':
        if testRunFlag == "Yes":
          doTraining(5, 5, False)
        else:
          doTraining(60, 5, False)
      elif condition == 'Stim Pairing':
          reversal = False
          doStimPairing()
      elif condition == 'Experimental Phase':
          reversal = False
          doExperimentalPhase()
      elif condition == 'Experimental Reversal':
          reversal = True
          doExperimentalPhase()
      experimentEndTime = time.strftime("%H:%M")
    except:
      e = sys.exc_info()[0]
      endTime = time.strftime("%H:%M")

      writer.writerow(["", "", "",
                        "", "", "",
                        "", "", "", "",
                        "", "", "", 
                        endTime])
      writer.writerow([])
      datafile.close()

      if type(e) != type(SystemExit):
        logging.exception(e)
        raise
    else:
      logging.debug("Experiment finished cleanly")
      datafile.close()



#Called when the experiment starts.
if __name__ == "__main__":
    main()