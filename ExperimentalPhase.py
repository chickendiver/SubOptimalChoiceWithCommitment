from sys import platform as _platform
from psychopy import visual, core, gui, event, parallel
import time, csv, random, datetime

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

LINE_WIDTH = 4

EXPERIMENT_TIME = 2700 #seconds = 45min

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

          

class InitialLinkStim:
  def __init__(self, name):
          self.x = 0
          self.y = I_STIM_Y
          self.radius = 50
          self.fillColour = "Gray"
          self.outlineColour = "Silver"
          self.name = name
          self.termStims = []

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

          # FIX/TEST: IS DRAWING BLANKS HERE NECESSARY?
          drawBlanksNoFlip(listOfBlanks)

          if result == 0:
            termStimShown = self.termStims[0]
            self.termStims[0].draw()
          else:
            termStimShown = self.termStims[1]
            self.termStims[1].draw()

          return termStimShown

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
        
  def set_outline (self, outlineCol):
        self.outlineColour = outlineCol

  def set_chanceOfReinforcement(self, chance):
        self.chanceOfReinforcement = chance

  def set_x (self, x):
        self.x = x

  def set_y (self, y):
        self.y = y

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
          

def rollForTermResult(initialLink):
    global termResults1, termResults2, rolledBefore, index1, index2

    if not rolledBefore:
      termResults1 = [0,0,0,0,0,0,0,0,1,1,
                      1,1,1,1,1,1,1,1,1,1,
                      1,1,1,1,1,1,1,1,1,1,
                      1,1,1,1,1,1,1,1,1,1]

      termResults2 = [0,0,0,0,0,0,0,0,1,1,
                      1,1,1,1,1,1,1,1,1,1,
                      1,1,1,1,1,1,1,1,1,1,
                      1,1,1,1,1,1,1,1,1,1]
      random.shuffle(termResults1)
      random.shuffle(termResults2)
      index1 = 0
      index2 = 0

    rolledBefore = True

    if initialLink.name == "InitA":
      result = termResults1[index1]
      index1 += 1

      if index1 == len(termResults1):
        rolledBefore = False

    elif initialLink.name == "InitB":
      result = termResults2[index2]
      index2 += 1

      if index2 == len(termResults2):
        rolledBefore = False

    return result

def rollDiceForFiftyFifty():
    global rolledFFBefore, FFResults, FFIndex

    if not rolledFFBefore:
        FFResults = [0,0,0,0,0,0,0,0,0,0,
                     0,0,0,0,0,0,0,0,0,0,
                     1,1,1,1,1,1,1,1,1,1,
                     1,1,1,1,1,1,1,1,1,1]

        random.shuffle(FFResults)
        FFIndex = -1

    rolledFFBefore = True

    FFIndex += 1

    if FFIndex == len(FFResults):
      random.shuffle(FFResults)
      FFIndex = -1

    return FFResults[FFIndex]


def setup():
    global win, mouse, rolledBefore, parallelPort

    print("\nSetting up...")
    
    #initialize the window
    win = visual.Window(fullscr = True, rgb = [-1.000,-1.000,-1.000], units = "pix", winType = "pyglet")
    
    #setup input from the mouse
    mouse = event.Mouse(visible = True)
    core.checkPygletDuringWait = True

    #parallelPort = parallel.ParallelPort(address=0x0378)

    rolledBefore = False
    rolledFFBefore = False

def createStimuli():
    global blankLeftChoiceStim, blankCentreChoiceStim, blankRightChoiceStim
    global blankLeftTermStim, blankRightTermStim, choiceA, choiceB, choiceC
    global initA, initB, termLinkA, termLinkB, termLinkC, termLinkD
    global listOfBlanks

    print("\nCreating stimuli...")

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

def matchStimuli(contingency, reversal):

    print("\nMatching Stimuli...")

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
          termLinkA.set_chanceOfReinforcement(0.5)
          termLinkB.set_chanceOfReinforcement(0.5)
          termLinkC.set_chanceOfReinforcement(1)
          termLinkD.set_chanceOfReinforcement(0)

        elif reversal == True:
          termLinkA.set_chanceOfReinforcement(1)
          termLinkB.set_chanceOfReinforcement(0)
          termLinkC.set_chanceOfReinforcement(0.5)
          termLinkD.set_chanceOfReinforcement(0.5)


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
          termLinkA.set_chanceOfReinforcement(0.5)
          termLinkB.set_chanceOfReinforcement(1)
          termLinkC.set_chanceOfReinforcement(0)
          termLinkD.set_chanceOfReinforcement(0.5)

        elif reversal == True:
          termLinkA.set_chanceOfReinforcement(0)
          termLinkB.set_chanceOfReinforcement(0.5)
          termLinkC.set_chanceOfReinforcement(0.5)
          termLinkD.set_chanceOfReinforcement(1)

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
          termLinkA.set_chanceOfReinforcement(1)
          termLinkB.set_chanceOfReinforcement(0)
          termLinkC.set_chanceOfReinforcement(0.5)
          termLinkD.set_chanceOfReinforcement(0.5)

        elif reversal == True:
          termLinkA.set_chanceOfReinforcement(0.5)
          termLinkB.set_chanceOfReinforcement(0.5)
          termLinkC.set_chanceOfReinforcement(1)
          termLinkD.set_chanceOfReinforcement(0)

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
          termLinkA.set_chanceOfReinforcement(0)
          termLinkB.set_chanceOfReinforcement(0.5)
          termLinkC.set_chanceOfReinforcement(0.5)
          termLinkD.set_chanceOfReinforcement(1)

        elif reversal == True:
          termLinkA.set_chanceOfReinforcement(0.5)
          termLinkB.set_chanceOfReinforcement(1)
          termLinkC.set_chanceOfReinforcement(0)
          termLinkD.set_chanceOfReinforcement(0.5)

        choiceA.add_initStim(initA)
        choiceB.add_initStim(initB)
        choiceC.add_initStim(initA)
        choiceC.add_initStim(initB)

        initA.add_termStim(termLinkD)
        initA.add_termStim(termLinkA)
        initB.add_termStim(termLinkB)
        initB.add_termStim(termLinkC)

def makeChoiceStimList():
    print("Randomizing choice stimuli...")

    choiceList = []

    choiceList1 = [choiceA, choiceB]
    choiceList2 = [choiceA, choiceC]
    choiceList3 = [choiceB, choiceC]

    for i in range(0,10):
      choiceList.append([choiceA])
      choiceList.append([choiceB])
      choiceList.append([choiceC])
      choiceList.append(choiceList1)
      choiceList.append(choiceList2)
      choiceList.append(choiceList3)

    random.shuffle(choiceList)

    return choiceList

def drawBlanksNoFlip(stimuli):
    for i in range(0,len(stimuli)):
        stimuli[i].draw()

def drawStims(stimuli):
    print("Drawing stimuli...")

    if len(stimuli) != len(listOfBlanks):
        drawBlanksNoFlip(listOfBlanks)

    for i in range(0,len(stimuli)):
      stimuli[i].draw()

    win.flip()

def waitForClicks(stimuli):

    print("Waiting for clicks...")
    peckNum = 0
    targetPeckNum = 0
    targetPeckRequired = 1 #FIX: MAKE ADJUSTABLE
    targetPecked = ""

    targetFlag = False
    stimTimer = core.CountdownTimer(stimDur)
    
    while ((stimTimer.getTime > 0) and (targetFlag == False)):

      event.clearEvents('mouse')
      #mouse.clickReset()

      if (mouse.getPressed()[0] == 1):
          pos = mouse.getPos()

          for i in range (0,len(stimuli)):
            if stimuli[i].boundingBox.contains(pos):
              targetPeckNum += 1
              if targetPeckNum >= targetPeckRequired:
                targetFlag = True
                targetPecked = stimuli[i]
                break
          
      while (mouse.getPressed()[0] == 1):
        if (mouse.getPressed()[0] == 0):
          break

      peckNum += 1

      if event.getKeys(["escape"]):
        print("User pressed escape")
        exit()


    return targetPecked, targetFlag

def displayEndScreen():
  print("Displaying end screen")
  #FIX: Display "EXPERIMENT HAS FINISHED, 45 MINUTES HAVE ELAPSED"
  

def giveReward(probability):
  print("Reward given")

def dropLeftHopper():
  parallelPort.setPin(16, 1) #Drops hopper
  parallelPort.setPin(4, 1) #Turns on hopper light

def raiseLeftHopper():
  parallelPort.setPin(16, 0) #Raises hopper
  parallelPort.setPin(4, 0) #Turns off hopper light

def dropRightHopper():
  parallelPort.setPin(32, 1) #Drops hopper
  parallelPort.setPin(8, 1) #Turns on hopper light

def raiseRightHopper():
  parallelPort.setPin(32, 0) #Raises hopper
  parallelPort.setPin(8, 0) #Turns off hopper light

def turnOnHouseLight():
  parallelPort.setPin(1, 1)

def turnOffHouseLight():
  parallelPort.setPin(1, 0)

def turnOnFan():
  parallelPort.setPin(2, 1)

def turnOffFan():
  parallelPort.setPin(2, 0)

def readLeftHopperBeam():
  #return if beam broken
  pass

def readRightHopperBeam():
  #return if beam broken
  pass


def doExperimentalPhase():
    print("Starting experimental phase...")

    createStimuli()
    matchStimuli(contingency, reversal)
    stimList = makeChoiceStimList()

    startTime = time.time()
    expTimer = core.CountdownTimer(EXPERIMENT_TIME)

    for i in range(0,len(stimList)):
        if (expTimer.getTime <= 0):
          break
        drawStims(stimList[i])
        cStimPecked, cClickFlag = waitForClicks(stimList[i])
        if cClickFlag == True:
          drawStims(cStimPecked.initStims)
          iStimPecked, iClickFlag = waitForClicks(cStimPecked.initStims)
          if iClickFlag == True:
            termStimShown = iStimPecked.drawTermLinks()
            win.flip()
            core.wait(termDur)
            
            giveReward(termStimShown.chanceOfReinforcement)

            drawStims(listOfBlanks) #Display blank stimuli for duration of ITI
            core.wait(ITI)

    endTime = time.time()

    while (expTimer.getTime > 0):
      drawStims(listOfBlanks)

    displayEndScreen() #FIX: NEEDS TO BE WRITTEN

def makeInitStimList():
    print("Randomizing init stimuli...")

    initList = []

    initList1 = [initA, initB]

    for i in range(0,20):
      initList.append([initA])
      initList.append([initB])
      initList.append(initList1)

    random.shuffle(initList)

    return initList


def doStimPairing():
    createStimuli()
    matchStimuli(contingency, reversal)
    stimList = makeInitStimList()

    startTime = time.time()
    expTimer = core.CountdownTimer(EXPERIMENT_TIME)

    for i in range(0,len(stimList)):
        if (expTimer.getTime <= 0):
          break
        drawStims(stimList[i])
        iStimPecked, iClickFlag = waitForClicks(stimList[i])
        if iClickFlag == True:
          termStimShown = iStimPecked.drawTermLinks()
          win.flip()
          core.wait(termDur)
          
          giveReward(termStimShown.chanceOfReinforcement)

          drawStims(listOfBlanks) #Display blank stimuli for duration of ITI
          core.wait(ITI)

    endTime = time.time()

    while (expTimer.getTime > 0):
      drawStims(listOfBlanks)

    displayEndScreen() #FIX: NEEDS TO BE WRITTEN

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

  stimList = [LChoiceA, CChoiceA, RChoiceA, # FIX: ADD MORE TRIALS TO THIS LIST ACCORDING TO THE SPEC
              LChoiceB, CChoiceB, RChoiceB,
              LChoiceC, CChoiceC, RChoiceC,
              LinitA, RinitA,
              LinitB, RinitB,
              LtermLinkA, RtermLinkA,
              LtermLinkB, RtermLinkB,
              LtermLinkC, RtermLinkC,
              LtermLinkD, RtermLinkD]

  random.shuffle(stimList)
  return stimList

def doTraining(ITI, pecksToReward, rewardIfNotPecked):
  stimList = generateListOfAllStims()

  for i in range(0, let(stimList)):
    stimList[i].draw()
    stimPecked, clickFlag = waitForClicks(stimList[i])

    if rewardIfNotPecked or clickFlag:
      giveReward(1)

    drawStims(listOfBlanks) #Display blank stimuli for duration of ITI
    core.wait(ITI)

def getUserInput():
    userCancelled = False
    myDlg = gui.Dlg(title="Sub-Optimal Choice with Commitment", labelButtonOK=' START ')
    myDlg.addField('Subject number:', 0)
    myDlg.addField('Session number:', 0)
    myDlg.addField('Condition:', choices = ['Autoshaping (FR1)', 'Operant Training (FR1)', 'Operant Training (FR3)', 'Operant Training (FR5)', 'Stim Pairing', 'Experimental Phase', 'Experimental Reversal'])
    #myDlg.addField('Contingency:', choices = ['1', '2', '3', '4'])
    myDlg.addField('Reward Duration:', 10)
    myDlg.addField('Stimulus Timeout:', 60)
    myDlg.addField('Is this a test?:', choices = ['Yes', 'No'])
    myDlg.addField('Research Assistant:')#, choices = ['Unlisted','Ariel','Jason', 'Jeff', 'Josh','Nuha'])
    myDlg.show()  # show dialog and wait for OK or Cancel
    
    if myDlg.OK:  # then the user pressed OK
        experimentParameters = myDlg.data
        print experimentParameters
    else:
        print 'user cancelled'
        userCancelled = True

    return experimentParameters, userCancelled


def main():
    global ITI, stimDur, contingency, reversal, termDur

    userResponses, userCancelled = getUserInput()

    termDur = 5
    reversal = False
    contingency = "4"
    stimDur = 5
    ITI = 5

    #FIX: ADD A GUI INPUT HERE

    setup()
    doExperimentalPhase()
    doStimPairing()
    doTraining(240, 1, True)
    doTraining(60, 1, False)
    doTraining(60, 3, False)
    doTraining(60, 5, False)

if __name__ == "__main__":
    main()