from sys import platform as _platform
from psychopy import visual, core, gui, event
import time, csv, random

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
  
L_CHOICE_STIM_X = (-1*(screen_width/3))
L_CHOICE_STIM_Y = (screen_width/16)
  
C_CHOICE_STIM_X = 0
C_CHOICE_STIM_Y = (screen_width/16)
  
R_CHOICE_STIM_X = (screen_width/3)
R_CHOICE_STIM_Y = (screen_width/16)
  
L_I_STIM_X = (-1*(screen_width/3))
L_I_STIM_Y = (-1*(screen_width/16))
  
  #Middle circular stimulus for future use
'''C_I_STIM_X = 0
C_I_STIM_Y = (-1*(screen_width/16))'''
  
R_I_STIM_X = (screen_width/3)
R_I_STIM_Y = (-1*(screen_width/16))

LINE_WIDTH = 4

FORTYFIVE_MINUTES = 2700 #seconds

 # --------------------------------------------------------------------------- 
  
  # Circular Initial/Terminal Link objects, of which there will be 2 (1L, 1R)
class InitialLinkStim :
    def __init__(self, xCoord, yCoord):
        self.radius = 50
        self.x = xCoord
        self.y = yCoord
        self.fillColour = "Gray"
        self.outlineColour = "Silver"
    def set_fill (self, fillCol):
        self.fillColour = fillCol
        
    def set_outline (self, outlineCol):
        self.outlineColour = outlineCol
    
#Square Choice objects, of which there will be 3
class ChoiceStim:
    def __init__(self, xCoord, yCoord):
        self.height = 100
        self.width = 100
        self.x = xCoord
        self.y = yCoord
        self.fillColour = "Gray"
        self.outlineColour = "Silver"
   
    def set_fill (self, fillCol):
        self.fillColour = fillCol
        
    def set_outline (self, outlineCol):
        self.outlineColour = outlineCol
    
def setup():
    global win, datafile, writer, mouse
    
    #initialize the window
    win = visual.Window(fullscr = True, rgb = [-1.000,-1.000,-1.000], units = "pix", winType = "pyglet")
    
    #create the CSV (Excel) file for writing data
    filename = (time.strftime("%d_%m_%Y")) + '_' + str(experimentParameters[0]) + '_data.csv'
    datafile = open(filename, 'wb')
    writer = csv.writer(datafile, delimiter=',')
    
    #setup input from the mouse
    mouse = event.Mouse(visible = True)
    core.checkPygletDuringWait = True
    
 
def testScrn():
    message = visual.TextStim(win, text='hello')
    message.setAutoDraw(True)  # automatically draw every frame
    win.flip()
    core.wait(2.0)
    message.setText('world')  # change properties of existing stim
    win.flip()
    core.wait(2.0)
    
def getUserInput():
    global experimentParameters
    global userCancelled
    userCancelled = False
    myDlg = gui.Dlg(title="Sub-Optimal Choice with Commitment")
    myDlg.addField('Subject number:', 0)
    myDlg.addField('Session number:', 0)
    myDlg.addField('Condition:', choices = ['Autoshaping (FR1)', 'Operant Training (FR1)', 'Operant Training (FR3)', 'Operant Training (FR5)', 'Phase 3', 'Phase 4', 'Phase 4 Reversal'])
    myDlg.addField('Reward Duration:', 10)
    myDlg.addField('Stimulus Timeout:', 60)
    myDlg.addField('Is this a test?:', choices = ['Yes', 'No'])
    myDlg.show()  # show dialog and wait for OK or Cancel
    
    if myDlg.OK:  # then the user pressed OK
        experimentParameters = myDlg.data
        print experimentParameters
    else:
        print 'user cancelled'
        userCancelled = True
        
def initializeStims():
    #Create new stimulus objects
    global leftChoice, centreChoice, rightChoice, leftInitLink, centreInitLink, rightInitLink, IA, IB, IC, ID, CA, CB, CC, InitA, InitB, InitC
    leftChoice = ChoiceStim(L_CHOICE_STIM_X, L_CHOICE_STIM_Y)
    centreChoice = ChoiceStim(C_CHOICE_STIM_X, C_CHOICE_STIM_Y)
    rightChoice = ChoiceStim(R_CHOICE_STIM_X, R_CHOICE_STIM_Y)
    leftInitLink =  InitialLinkStim(L_I_STIM_X, L_I_STIM_Y)
    #Reserved for future use
    #centreInitLink = InitialLinkStim(C_I_STIM_X, C_I_STIM_Y)
    rightInitLink = InitialLinkStim(R_I_STIM_X, R_I_STIM_Y)
    
    #Choice trial initializations
    IA = InitialLinkStim(R_I_STIM_X, R_I_STIM_Y)
    IA.set_fill("Orange")
    IB = InitialLinkStim(R_I_STIM_X, R_I_STIM_Y)
    IB.set_fill("Green")
    IC = InitialLinkStim(R_I_STIM_X, R_I_STIM_Y)
    IC.set_fill("Red")
    ID = InitialLinkStim(R_I_STIM_X, R_I_STIM_Y)
    ID.set_fill("Purple")
    CA = ChoiceStim(L_CHOICE_STIM_X, L_CHOICE_STIM_Y)
    CB = ChoiceStim(C_CHOICE_STIM_X, C_CHOICE_STIM_Y)
    CC = ChoiceStim(R_CHOICE_STIM_X, R_CHOICE_STIM_Y)
    InitA = InitialLinkStim(R_I_STIM_X, R_I_STIM_Y)
    InitB = InitialLinkStim(R_I_STIM_X, R_I_STIM_Y)
    InitC = InitialLinkStim(R_I_STIM_X, R_I_STIM_Y)
    
def drawLeftChoice():
    
    global win
    rect = visual.Rect(win, lineWidth = 4, width = leftChoice.width, height = leftChoice.height, pos = (leftChoice.x, leftChoice.y), units = "pix", lineColor = leftChoice.outlineColour, fillColor = leftChoice.fillColour)
    rect.draw()
   
def drawCentreChoice():
    global win
    rect = visual.Rect(win, lineWidth = LINE_WIDTH, width = centreChoice.width, height = centreChoice.height, pos = (centreChoice.x, centreChoice.y), units = "pix", lineColor = centreChoice.outlineColour, fillColor = centreChoice.fillColour)
    rect.draw()

def drawRightChoice():
    global win
    rect = visual.Rect(win, lineWidth = LINE_WIDTH, width = rightChoice.width, height = rightChoice.height, pos = (rightChoice.x, rightChoice.y), units = "pix", lineColor = rightChoice.outlineColour, fillColor = rightChoice.fillColour)
    rect.draw()
    
def drawLeftInitialLink():
    global win
    circ = visual.Circle(win, lineWidth = LINE_WIDTH, radius = leftInitLink.radius, pos = (leftInitLink.x, leftInitLink.y), units = "pix", lineColor = leftInitLink.outlineColour, fillColor = leftInitLink.fillColour)
    circ.draw()
    
def drawCentreInitialLink():
    global win
    circ = visual.Circle(win, lineWidth = LINE_WIDTH, radius = centreInitLink.radius, pos = (centreInitLink.x, centreInitLink.y), units = "pix", lineColor = centreInitLink.outlineColour, fillColor = centreInitLink.fillColour)
    circ.draw()
    
def drawRightInitialLink():
    global win
    circ = visual.Circle(win, lineWidth = LINE_WIDTH, radius = rightInitLink.radius, pos = (rightInitLink.x, rightInitLink.y), units = "pix", lineColor = rightInitLink.outlineColour, fillColor = rightInitLink.fillColour)
    circ.draw()
    
def drawInitialStims():
    drawLeftChoice()
    drawCentreChoice()
    drawRightChoice()
    drawLeftInitialLink()
    #Reserved for future use
    #drawCentreInitialLink()
    drawRightInitialLink()
    win.flip()
    
def drawIA():
    global win, IACirc

    drawLeftChoice()
    drawCentreChoice()
    drawRightChoice()

    if IA.x >= 0:
        drawLeftInitialLink()

    else:
        drawRightInitialLink()

    IACirc = visual.Circle(win, lineWidth = LINE_WIDTH, radius = IA.radius, pos = (IA.x, IA.y), units = "pix", lineColor = IA.outlineColour, fillColor = IA.fillColour)
    IACirc.draw()
    win.flip()
    
def drawIB():
    global win, IBCirc

    drawLeftChoice()
    drawCentreChoice()
    drawRightChoice()

    if IB.x >= 0:
        drawLeftInitialLink()

    else:
        drawRightInitialLink()

    IBCirc = visual.Circle(win, lineWidth = LINE_WIDTH, radius = IB.radius, pos = (IB.x, IB.y), units = "pix", lineColor = IB.outlineColour, fillColor = IB.fillColour)
    IBCirc.draw()
    win.flip()
    
def drawIC():
    global win,ICCirc

    drawLeftChoice()
    drawCentreChoice()
    drawRightChoice()

    if IC.x >= 0:
        drawLeftInitialLink()

    else:
        drawRightInitialLink()

    ICCirc = visual.Circle(win, lineWidth = LINE_WIDTH, radius = IC.radius, pos = (IC.x, IC.y), units = "pix", lineColor = IC.outlineColour, fillColor = IC.fillColour)
    ICCirc.draw()
    win.flip()
    
def drawID():
    global win, IDCirc

    drawLeftChoice()
    drawCentreChoice()
    drawRightChoice()

    if ID.x >= 0:
        drawLeftInitialLink()

    else:
        drawRightInitialLink()

    IDCirc = visual.Circle(win, lineWidth = LINE_WIDTH, radius = ID.radius, pos = (ID.x, ID.y), units = "pix", lineColor = ID.outlineColour, fillColor = ID.fillColour)
    IDCirc.draw()
    win.flip()
    
def drawCA():
    global win, CARect

    drawLeftChoice()
    drawCentreChoice()
    drawRightChoice()
    drawLeftInitialLink()
    drawRightInitialLink()


    topRight = (CA.x + (CA.width/2), CA.y + (CA.height/2))
    bottomLeft = (CA.x - (CA.width/2), CA.y - (CA.height/2))
    topLeft = (CA.x - (CA.width/2), CA.y + (CA.height/2))
    bottomRight = (CA.x + (CA.width/2), CA.y - (CA.height/2))

    CARect = visual.Rect(win, lineWidth = LINE_WIDTH, width = CA.width, height = CA.height, pos = (CA.x, CA.y), units = "pix", lineColor = CA.outlineColour, fillColor = "White")
    CALine1 = visual.Line(win, start = (topRight), end = (bottomLeft), lineWidth = LINE_WIDTH, units = "pix", lineColor = "Black")
    CALine2 = visual.Line(win, start = (bottomRight), end = (topLeft), lineWidth = LINE_WIDTH, units = "pix", lineColor = "Black")
    CARect.draw()
    CALine1.draw()
    CALine2.draw()
    win.flip()
    
def drawCB():
    global win, CBRect

    drawLeftChoice()
    drawCentreChoice()
    drawRightChoice()
    drawLeftInitialLink()
    drawRightInitialLink()

    CBInnerRect = visual.Rect(win, lineWidth = LINE_WIDTH, width = 30, height = 30, pos = (CB.x, CB.y), units = "pix", lineColor = "Black", fillColor = "White")
    CBRect = visual.Rect(win, lineWidth = LINE_WIDTH, width = CB.width, height = CB.height, pos = (CB.x, CB.y), units = "pix", lineColor = CB.outlineColour, fillColor = "White")
    CBRect.draw()
    CBInnerRect.draw()
    win.flip()
    
def drawCC():
    global win, CCRect

    drawLeftChoice()
    drawCentreChoice()
    drawRightChoice()
    drawLeftInitialLink()
    drawRightInitialLink()

    CCRect = visual.Rect(win, lineWidth = LINE_WIDTH, width = CC.width, height = CC.height, pos = (CC.x, CC.y), units = "pix", lineColor = CC.outlineColour, fillColor = "White")
    CCInnerCirc = visual.Circle(win, lineWidth = LINE_WIDTH, radius = 15, pos = (CC.x, CC.y), units = "pix", lineColor = "Black", fillColor = "Black")
    CCRect.draw()
    CCInnerCirc.draw()
    win.flip()
    
def drawInitA():
    global win, InitACirc

    drawLeftChoice()
    drawCentreChoice()
    drawRightChoice()

    if InitA.x >= 0:
        drawLeftInitialLink()

    else:
        drawRightInitialLink()

    InitACirc = visual.Circle(win, lineWidth = LINE_WIDTH, radius = InitA.radius, pos = (InitA.x, InitA.y), units = "pix", lineColor = InitA.outlineColour, fillColor = "White")
    InitAVertLine = visual.Line(win, start = (InitA.x, (InitA.y + InitA.radius)), end = (InitA.x, (InitA.y - InitA.radius)), lineWidth = LINE_WIDTH, units = "pix", lineColor = "Black")
    InitACirc.draw()
    InitAVertLine.draw()
    win.flip()
    
def drawInitB():
    global win, InitBCirc

    drawLeftChoice()
    drawCentreChoice()
    drawRightChoice()

    topStart = ((InitB.x - 35), (InitB.y + 20))
    topEnd = ((InitB.x + 35), (InitB.y + 20))
    midStart = ((InitB.x - InitB.radius), (InitB.y))
    midEnd = ((InitB.x + InitB.radius), (InitB.y))
    bottomStart = ((InitB.x - 35), (InitB.y - 20))
    bottomEnd = ((InitB.x + 35), (InitB.y - 20))

    if InitB.x >= 0:
        drawLeftInitialLink()

    else:
        drawRightInitialLink()

    InitBCirc = visual.Circle(win, lineWidth = LINE_WIDTH, radius = InitB.radius, pos = (InitB.x, InitB.y), units = "pix", lineColor = InitB.outlineColour, fillColor = "White")
    InitBTopLine = visual.Line(win, start = (topStart), end = (topEnd), lineWidth = LINE_WIDTH, units = "pix", lineColor = "Black")
    InitBMidLine = visual.Line(win, start = (midStart), end = (midEnd), lineWidth = LINE_WIDTH, units = "pix", lineColor = "Black")
    InitBBottomLine = visual.Line(win, start = (bottomStart), end = (bottomEnd), lineWidth = LINE_WIDTH, units = "pix", lineColor = "Black")
    InitBCirc.draw()
    InitBTopLine.draw()
    InitBMidLine.draw()
    InitBBottomLine.draw()
    win.flip()
    
def drawInitC():
    global win, InitCCirc

    drawLeftChoice()
    drawCentreChoice()
    drawRightChoice()

    if InitC.x >= 0:
        drawLeftInitialLink()

    else:
        drawRightInitialLink()

    InitCCirc = visual.Circle(win, lineWidth = LINE_WIDTH, radius = InitC.radius, pos = (InitC.x, InitC.y), units = "pix", lineColor = InitC.outlineColour, fillColor = InitC.fillColour)
    InitCCirc.draw()
    win.flip()

def raiseHopper():
    print("Hopper raised")
    
def giveReward(duration):
    print("Reward Given for duration of " + str(duration) + " seconds")
    raiseHopper()
    drawLeftChoice()
    drawCentreChoice()
    drawRightChoice()
    drawLeftInitialLink()
    drawRightInitialLink()
    win.flip()
    core.wait(duration)
    
def doAutoshaping():
    global nPecksToReward, ITI, allTrialsFinished, datafile, writer, peckNum, row, stimuli, rewardTime, stimDur
    if str(experimentParameters[5]) == "No":
        rewardTime = experimentParameters[3]
        stimDur = experimentParameters[4]
        ITI = 240

    nPecksToReward = 1
    pecksOnTarget = 0
    allTrialsFinished = False
    peckNum = 0
    row = 0
    index = 0
    trialTime = 0
    stimType = ""
    victoryFlag = False
    
    # FINDING A BETTER WAY TO DRAW THESE STIMULI WILL BE HELPFUL.
    # START HERE.
    writer.writerow([row, 'Subject Number', 'Trial Number', 'Total Pecks', 'Elapsed Time', 'Stimulus Presented', 
                          'Stimulus Side', 'Satisfied No. Pecks', 'No. Pecks on Target', 'Accuracy'])

    stimuli = [[["L", "IA"], ["R", "IA"], ["L","IB"], ["R","IB"], ["L","IC"], ["R","IC"], ["L","ID"], ["R","ID"],
             ["L","CA"], ["R","CA"], ["L","CB"], ["R","CB"], ["L","CC"], ["R","CC"],
             [["L","InitA"], ["R","InitA"]], ["L","InitB"], ["R","InitB"]]#, ["L","InitC"], ["R","InitC"]]

    random.shuffle(stimuli) #Present stimuli in a random order

    core.wait(1) #Give the CPU a bit of a break
    
    startTime = time.time() #Set a timer to record times for the log
    expTimer = core.CountdownTimer(FORTYFIVE_MINUTES)
    while(expTimer.getTime > 0):

        #core.wait(0.5) # TESTING
            
        if stimuli[index][1] == "IA":
            stimType = "IA"
            if stimuli[index][0] == "L":
                IA.x *= -1
                stimSide = "L"
                
            drawIA()

            stimTimer = core.CountdownTimer(stimDur)
            while (stimTimer.getTime() > 0):
                    
                event.clearEvents()
                mouse.clickReset()
                #get bird's input. If it pecks the target, break and give the bird food. Otherwise, increase the peck count and keep looking for input
                if mouse.isPressedIn(IACirc):
                    print("Clicked in target") # TESTING ONLY
                    peckNum += 1
                    pecksOnTarget += 1
                    event.clearEvents()
                    if pecksOnTarget == nPecksToReward:
                        victoryFlag = True
                        break
                        
                elif (mouse.getPressed()[0]):
                    while(mouse.getPressed()[0]): # waits for the mouse button to raise before counting another peck
                        if (not mouse.getPressed()[0]):
                            event.clearEvents()
                            break
                        
                    peckNum += 1
                    event.clearEvents()
                    continue
                    
                if event.getKeys(["escape"]):
                    print("User pressed escape")
                    print(str(peckNum))
                    event.clearEvents()
                    exit()
                
            # Reset the stimulus to be placed on the right
            if stimuli[index][0] == "L":
                IA.x *= -1
                
           
        elif stimuli[index][1] == "IB":
            stimType = "IB"
            if stimuli[index][0] == "L":
                IB.x *= -1
                stimSide = "L"
                
            drawIB()

            stimTimer = core.CountdownTimer(stimDur)
            while (stimTimer.getTime() > 0):
                    
                event.clearEvents()
                mouse.clickReset()
                #get bird's input. If it pecks the target, break give the bird food. Otherwise, increase the peck count and keep looking for input
                if mouse.isPressedIn(IBCirc):
                    print("Clicked in target") # TESTING ONLY
                    peckNum += 1
                    pecksOnTarget += 1
                    event.clearEvents()
                    if pecksOnTarget == nPecksToReward:
                        victoryFlag = True
                        break
                        
                elif (mouse.getPressed()[0] == 1):
                    while(mouse.getPressed()[0] == 1): # waits for the mouse button to raise before counting another peck
                        if (mouse.getPressed()[0] == 0):
                            break
                        
                    peckNum += 1
                    event.clearEvents()
                    
                if event.getKeys(["escape"]):
                    print("User pressed escape")
                    print(str(peckNum))
                    exit()
            
            # Reset the stimulus
            if stimuli[index][0] == "L":
                IB.x *= -1
            pass
            
        elif stimuli[index][1] == "IC":
            stimType = "IC"
            if stimuli[index][0] == "L":
                IC.x *= -1
                stimSide = "L"
                
            drawIC()

            stimTimer = core.CountdownTimer(stimDur)
            while (stimTimer.getTime() > 0):
                    
                event.clearEvents()
                mouse.clickReset()
                #get bird's input. If it pecks the target, break give the bird food. Otherwise, increase the peck count and keep looking for input
                if mouse.isPressedIn(ICCirc):
                    print("Clicked in target") # TESTING ONLY
                    peckNum += 1
                    pecksOnTarget += 1
                    event.clearEvents()
                    if pecksOnTarget == nPecksToReward:
                        victoryFlag = True
                        break
                        
                elif (mouse.getPressed()[0] == 1):
                    while(mouse.getPressed()[0] == 1): # waits for the mouse button to raise before counting another peck
                        if (mouse.getPressed()[0] == 0):
                            break
                        
                    peckNum += 1
                    event.clearEvents()
                    
                if event.getKeys(["escape"]):
                    print("User pressed escape")
                    print(str(peckNum))
                    exit()
            
            # Reset the stimulus
            if stimuli[index][0] == "L":
                IC.x *= -1
                
            pass
            
        elif stimuli[index][1] == "ID":
            stimType = "ID"
            if stimuli[index][0] == "L":
                ID.x *= -1
                stimSide = "L"
                
            drawID()

            stimTimer = core.CountdownTimer(stimDur)
            while (stimTimer.getTime() > 0):
                    
                event.clearEvents()
                mouse.clickReset()
                #get bird's input. If it pecks the target, break give the bird food. Otherwise, increase the peck count and keep looking for input
                if mouse.isPressedIn(IDCirc):
                    print("Clicked in target") # TESTING ONLY
                    peckNum += 1
                    pecksOnTarget += 1
                    event.clearEvents()
                    if pecksOnTarget == nPecksToReward:
                        victoryFlag = True
                        break
                        
                elif (mouse.getPressed()[0] == 1):
                    while(mouse.getPressed()[0] == 1): # waits for the mouse button to raise before counting another peck
                        if (mouse.getPressed()[0] == 0):
                            break
                        
                    peckNum += 1
                    event.clearEvents()
                    
                if event.getKeys(["escape"]):
                    print("User pressed escape")
                    print(str(peckNum))
                    exit()
            
            # Reset the stimulus
            if stimuli[index][0] == "L":
                ID.x *= -1
                
        elif stimuli[index][1] == "InitA":
            stimType = "InitA"
            if stimuli[index][0] == "L":
                InitA.x *= -1
                stimSide = "L"
                
            drawInitA()

            stimTimer = core.CountdownTimer(stimDur)
            while (stimTimer.getTime() > 0):
                    
                event.clearEvents()
                mouse.clickReset()
                #get bird's input. If it pecks the target, break give the bird food. Otherwise, increase the peck count and keep looking for input
                if mouse.isPressedIn(InitACirc):
                    print("Clicked in target") # TESTING ONLY
                    peckNum += 1
                    pecksOnTarget += 1
                    event.clearEvents()
                    if pecksOnTarget == nPecksToReward:
                        victoryFlag = True
                        break
                        
                elif (mouse.getPressed()[0] == 1):
                    while(mouse.getPressed()[0] == 1): # waits for the mouse button to raise before counting another peck
                        if (mouse.getPressed()[0] == 0):
                            break
                        
                    peckNum += 1
                    event.clearEvents()
                    
                if event.getKeys(["escape"]):
                    print("User pressed escape")
                    print(str(peckNum))
                    exit()
            
            # Reset the stimulus
            if stimuli[index][0] == "L":
                InitA.x *= -1


        elif stimuli[index][1] == "InitB":
            stimType = "InitB"
            if stimuli[index][0] == "L":
                InitB.x *= -1
                stimSide = "L"
                
            drawInitB()

            stimTimer = core.CountdownTimer(stimDur)
            while (stimTimer.getTime() > 0):
                    
                event.clearEvents()
                mouse.clickReset()
                #get bird's input. If it pecks the target, break give the bird food. Otherwise, increase the peck count and keep looking for input
                if mouse.isPressedIn(InitBCirc):
                    print("Clicked in target") # TESTING ONLY
                    peckNum += 1
                    pecksOnTarget += 1
                    event.clearEvents()
                    if pecksOnTarget == nPecksToReward:
                        victoryFlag = True
                        break
                        
                elif (mouse.getPressed()[0] == 1):
                    while(mouse.getPressed()[0] == 1): # waits for the mouse button to raise before counting another peck
                        if (mouse.getPressed()[0] == 0):
                            break
                        
                    peckNum += 1
                    event.clearEvents()
                    
                if event.getKeys(["escape"]):
                    print("User pressed escape")
                    print(str(peckNum))
                    exit()
            
            # Reset the stimulus
            if stimuli[index][0] == "L":
                InitB.x *= -1

        elif stimuli[index][1] == "InitC":
            stimType = "InitC"
            if stimuli[index][0] == "L":
                InitC.x *= -1
                stimSide = "L"
                
            drawInitC()

            stimTimer = core.CountdownTimer(stimDur)
            while (stimTimer.getTime() > 0):
                    
                event.clearEvents()
                mouse.clickReset()
                #get bird's input. If it pecks the target, break give the bird food. Otherwise, increase the peck count and keep looking for input
                if mouse.isPressedIn(InitCCirc):
                    print("Clicked in target") # TESTING ONLY
                    peckNum += 1
                    pecksOnTarget += 1
                    event.clearEvents()
                    if pecksOnTarget == nPecksToReward:
                        victoryFlag = True
                        break
                        
                elif (mouse.getPressed()[0] == 1):
                    while(mouse.getPressed()[0] == 1): # waits for the mouse button to raise before counting another peck
                        if (mouse.getPressed()[0] == 0):
                            break
                        
                    peckNum += 1
                    event.clearEvents()
                    
                if event.getKeys(["escape"]):
                    print("User pressed escape")
                    print(str(peckNum))
                    exit()
            
            # Reset the stimulus
            if stimuli[index][0] == "L":
                InitC.x *= -1

        elif stimuli[index][1] == "CA":
            stimType = "CA"
            if stimuli[index][0] == "L":
                CA.x *= -1
                stimSide = "L"
                
            drawCA()

            stimTimer = core.CountdownTimer(stimDur)
            while (stimTimer.getTime() > 0):
                    
                event.clearEvents()
                mouse.clickReset()
                #get bird's input. If it pecks the target, break give the bird food. Otherwise, increase the peck count and keep looking for input
                if mouse.isPressedIn(CARect):
                    print("Clicked in target") # TESTING ONLY
                    peckNum += 1
                    pecksOnTarget += 1
                    event.clearEvents()
                    if pecksOnTarget == nPecksToReward:
                        victoryFlag = True
                        break
                        
                elif (mouse.getPressed()[0] == 1):
                    while(mouse.getPressed()[0] == 1): # waits for the mouse button to raise before counting another peck
                        if (mouse.getPressed()[0] == 0):
                            break
                        
                    peckNum += 1
                    event.clearEvents()
                    
                if event.getKeys(["escape"]):
                    print("User pressed escape")
                    print(str(peckNum))
                    exit()
                
            # Reset the stimulus to be placed on the right
            if stimuli[index][0] == "L":
                CA.x *= -1

        elif stimuli[index][1] == "CB":
            stimType = "CB"
            if stimuli[index][0] == "L":
                CA.x *= -1
                stimSide = "L"
                
            drawCB()

            stimTimer = core.CountdownTimer(stimDur)
            while (stimTimer.getTime() > 0):
                    
                event.clearEvents()
                mouse.clickReset()
                #get bird's input. If it pecks the target, break give the bird food. Otherwise, increase the peck count and keep looking for input
                if mouse.isPressedIn(CBRect):
                    print("Clicked in target") # TESTING ONLY
                    peckNum += 1
                    pecksOnTarget += 1
                    event.clearEvents()
                    if pecksOnTarget == nPecksToReward:
                        victoryFlag = True
                        break
                        
                elif (mouse.getPressed()[0] == 1):
                    while(mouse.getPressed()[0] == 1): # waits for the mouse button to raise before counting another peck
                        if (mouse.getPressed()[0] == 0):
                            break
                        
                    peckNum += 1
                    event.clearEvents()
                    
                if event.getKeys(["escape"]):
                    print("User pressed escape")
                    print(str(peckNum))
                    exit()
                
            # Reset the stimulus to be placed on the right
            if stimuli[index][0] == "L":
                CB.x *= -1

        elif stimuli[index][1] == "CC":
            stimType = "CC"
            if stimuli[index][0] == "L":
                CC.x *= -1
                stimSide = "L"
                
            drawCC()

            stimTimer = core.CountdownTimer(stimDur)
            while (stimTimer.getTime() > 0):
                    
                event.clearEvents()
                mouse.clickReset()
                #get bird's input. If it pecks the target, break give the bird food. Otherwise, increase the peck count and keep looking for input
                if mouse.isPressedIn(CCRect):
                    print("Clicked in target") # TESTING ONLY
                    peckNum += 1
                    pecksOnTarget += 1
                    event.clearEvents()
                    if pecksOnTarget == nPecksToReward:
                        victoryFlag = True
                        break
                        
                elif (mouse.getPressed()[0] == 1):
                    while(mouse.getPressed()[0] == 1): # waits for the mouse button to raise before counting another peck
                        if (mouse.getPressed()[0] == 0):
                            break
                        
                    peckNum += 1
                    event.clearEvents()
                    
                if event.getKeys(["escape"]):
                    print("User pressed escape")
                    print(str(peckNum))
                    exit()
                
            # Reset the stimulus to be placed on the right
            if stimuli[index][0] == "L":
                CC.x *= -1


        if event.getKeys(["escape"]):
            print("User pressed escape")
            print(str(peckNum))
            exit()

        giveReward(rewardTime) # CHANGE 0 TO REWARD TIME LATER
        displayBlankPanel(ITI) # 5 for testing, change to ITI after
        index += 1
        row += 1
        if index >= len(stimuli):
            index = 0
        trialTime = time.time() - startTime
        writer.writerow([row, str(experimentParameters[0]), row, peckNum, trialTime*60, stimType, 
                                  stimSide, victoryFlag, pecksOnTarget, 'Accuracy'])
        
        peckNum = 0
        victoryFlag = False
        pecksOnTarget = 0
        stimSide = "R"

def doOperantTraining():
    global nPecksToReward, ITI, stimDur
    ITI = 60
    stimDur = 10
    if str(experimentParameters[2])[17:] == "(FR1)":
        print("FIXED RATIO 1 OT")
        nPecksToReward = 1
    if str(experimentParameters[2])[17:] == "(FR3)":
        print("FIXED RATIO 3 OT")
        nPecksToReward = 3
    if str(experimentParameters[2])[17:] == "(FR5)":
        print("FIXED RATIO 5 OT")
        nPecksToReward = 5
    pass
    
def doPhase3():
    print("PHASE 1")
    
def doPhase4():
    print("PHASE 4")
    
def doPhase4Reversal():
    print("PHASE 4 REVERSAL")
    
def displayBlankPanel(duration):
    global ITI
    drawInitialStims()
    core.wait(duration)
    pass
    
    
def main():
    global datafile, filename, writer, stimDur, rewardTime, ITI
    initializeStims()
    getUserInput()
    
    if userCancelled == True:
        exit()
        
    setup()

    if str(experimentParameters[5]) == "Yes":
        rewardTime = 0
        stimDur = 1
        ITI = 1
    elif str(experimentParameters[5]) == "No":
        mouse.setVisible = False
    
    if str(experimentParameters[2]) == "Autoshaping (FR1)":
        doAutoshaping()
        
    elif str(experimentParameters[2])[0:16] == "Operant Training":
        doOperantTraining()
        
    elif str(experimentParameters[2]) == "Phase 3":
        doPhase3()
        
    elif str(experimentParameters[2]) == "Phase 4":
        doPhase4()
        
    elif str(experimentParameters[2]) == "Phase 4 Reversal":
        doPhase4Reversal()
    
    
    #testScrn()

if __name__ == "__main__":
    main()
    datafile.close() 
