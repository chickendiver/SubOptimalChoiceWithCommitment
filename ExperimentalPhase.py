from sys import platform as _platform
from psychopy import visual, core, gui, event
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
          if self.name == "ChoiceA":
            #self.boundingBox
            pass
          elif self.name == "ChoiceB":
            pass
          elif self.name == "ChoiceC":
            pass
          else:
            pass

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
          if self.name == "InitA":
            pass
          elif self.name == "InitB":
            pass
          else:
            pass

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
          if self.name == "TermA":
            pass
          elif self.name == "TermB":
            pass
          elif self.name == "TermC":
            pass
          elif self.name == "TermD":
            pass
          else:
            pass

def setup():
    global win, mouse
    
    #initialize the window
    win = visual.Window(fullscr = True, rgb = [-1.000,-1.000,-1.000], units = "pix", winType = "pyglet")
    
    #setup input from the mouse
    mouse = event.Mouse(visible = True)
    core.checkPygletDuringWait = True

def createStimuli():
    global blankLeftChoiceStim, blankCentreChoiceStim, blankRightChoiceStim
    global blankLeftTermStim, blankRightTermStim, choiceA, choiceB, choiceC
    global initA, initB, termLinkA, termLinkB, termLinkC, termLinkD

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
    if contingency == "1":
        choiceA.set_x(L_X)
        choiceB.set_x(R_X)

        initA.set_x(L_X)
        initB.set_x(R_x)

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
        choiceC.add_initStim(initA, initB)

        initA.add_termStim(termLinkA, termLinkB)
        initB.add_termStim(termLinkC, termLinkD)

    elif contingency == "2":
        choiceA.set_x(R_X)
        choiceB.set_x(L_X)

        initA.set_x(L_X)
        initB.set_x(R_x)

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
        choiceC.add_initStim(initA, initB)

        initA.add_termStim(termLinkA, termLinkD)
        initB.add_termStim(termLinkB, termLinkC)
        
    elif contingency == "3":
        choiceA.set_x(L_X)
        choiceB.set_x(R_X)

        initA.set_x(R_X)
        initB.set_x(L_x)

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
        choiceC.add_initStim(initA, initB)

        initA.add_termStim(termLinkA, termLinkB)
        initB.add_termStim(termLinkC, termLinkD)

    elif contingency == "4":
        choiceA.set_x(R_X)
        choiceB.set_x(L_X)

        initA.set_x(R_X)
        initB.set_x(L_x)

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
        choiceC.add_initStim(initA, initB)

        initA.add_termStim(termLinkA, termLinkD)
        initB.add_termStim(termLinkB, termLinkC)

def makeChoiceStimList():
    choiceList = []

    choiceList1 = [choiceA, choiceB]
    choiceList2 = [choiceA, choiceC]
    choiceList3 = [choiceB, choiceC]

    for i in range(0,10):
      choiceList.append(choiceA)
      choiceList.append(choiceB)
      choiceList.append(choiceC)
      choiceList.append(choiceList1)
      choiceList.append(choiceList2)
      choiceList.append(choiceList3)

    random.shuffle(choiceList)

    return choiceList

def drawStims(stimuli):
    for i in range(0,len(stimuli)):
      stimuli[i].draw()

    win.flip()

def waitForClicks(stimuli):
    peckNum = 0
    targetPeckNum = 0
    targetPeckRequired = 1
    targetPecked = ""

    targetFlag = False
    # FIX: ADD TIMER HERE
    while (targetFlag == False):
      event.clearEvents()
      mouse.clickReset()

      
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

def doExperimentalPhase():
    createStimuli()
    matchStimuli(contingency, reversal)
    stimList = makeChoiceStimList()

    # SET EXPERIMENT TIMER IN A WHILE LOOP HERE
    for i in range(0,len(stimList)):
        drawStims(stimList[i])
        cStimPecked, cClickFlag = waitForClicks(stimList[i])
        if cClickFlag == True:
          drawStims(cStimPecked.initStims)
          iStimPecked, iClickFlag = waitForClicks(cStimPecked.initStims)
          if iClickFlag == True:
            drawStims(iStimPecked.termStims) #FIX: MAKE THIS SO THAT THE INITIAL LINK HAS A FUNCTION TO DRAW TERM STIMS
            #Give reward
            #Wait for an ITI

    # DISPLAY BLANK STIMS UNTIL TIMER RUNS OUT

    #AFTER TIMER RUNS OUT, DISPLAY RESULTS SCREEN

def main():

    setup()
    doExperimentalPhase()

if __name__ == "__main__":
    main()
