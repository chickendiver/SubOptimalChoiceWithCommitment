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
    def __init__(self, xCoord, yCoord, name):
        self.radius = 50
        self.x = xCoord
        self.y = yCoord
        self.fillColour = "Gray"
        self.outlineColour = "Silver"
        self.name = name

    def set_fill (self, fillCol):
        self.fillColour = fillCol
        
    def set_outline (self, outlineCol):
        self.outlineColour = outlineCol
    
#Square Choice objects, of which there will be 3
class ChoiceStim:
    def __init__(self, xCoord, yCoord, name):
        self.height = 100
        self.width = 100
        self.x = xCoord
        self.y = yCoord
        self.fillColour = "Gray"
        self.outlineColour = "Silver"
        self.name = name
   
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
    myDlg = gui.Dlg(title="Sub-Optimal Choice with Commitment", labelButtonOK=' START ')
    myDlg.addField('Subject number:', 0)
    myDlg.addField('Session number:', 0)
    myDlg.addField('Condition:', choices = ['Autoshaping (FR1)', 'Operant Training (FR1)', 'Operant Training (FR3)', 'Operant Training (FR5)', 'Stim Pairing', 'Experimental Phase', 'Experimental Reversal'])
    myDlg.addField('Reward Duration:', 10)
    myDlg.addField('Stimulus Timeout:', 60)
    myDlg.addField('Is this a test?:', choices = ['Yes', 'No'])
    myDlg.addField('Research Assistant:', choices = ['Unlisted','Ariel','Jason', 'Jeff', 'Josh','Nuha'])
    myDlg.show()  # show dialog and wait for OK or Cancel
    
    if myDlg.OK:  # then the user pressed OK
        experimentParameters = myDlg.data
        print experimentParameters
    else:
        print 'user cancelled'
        userCancelled = True
        
def initializeStims():
    #Create new stimulus objects
    global leftChoice, centreChoice, rightChoice, leftInitLink, centreInitLink, rightInitLink, termLinkA, termLinkB, termLinkC, termLinkD, CA, CB, CC, InitA, InitB, InitC
    leftChoice = ChoiceStim(L_CHOICE_STIM_X, L_CHOICE_STIM_Y, "left blank")
    centreChoice = ChoiceStim(C_CHOICE_STIM_X, C_CHOICE_STIM_Y, "middle blank")
    rightChoice = ChoiceStim(R_CHOICE_STIM_X, R_CHOICE_STIM_Y, "right blank")
    leftInitLink =  InitialLinkStim(L_I_STIM_X, L_I_STIM_Y, "blankL")
    #Reserved for future use
    #centreInitLink = InitialLinkStim(C_I_STIM_X, C_I_STIM_Y)
    rightInitLink = InitialLinkStim(R_I_STIM_X, R_I_STIM_Y, "blankR")
    
    #Choice trial initializations
    termLinkA = InitialLinkStim((R_I_STIM_X), R_I_STIM_Y, "termA")
    termLinkA.set_fill("Orange")
    termLinkB = InitialLinkStim(R_I_STIM_X, R_I_STIM_Y, "termB")
    termLinkB.set_fill("Green")
    termLinkC = InitialLinkStim((R_I_STIM_X), R_I_STIM_Y, "termC")
    termLinkC.set_fill("Red")
    termLinkD = InitialLinkStim(R_I_STIM_X, R_I_STIM_Y, "termLinkD")
    termLinkD.set_fill("Purple")
    CA = ChoiceStim(R_CHOICE_STIM_X, R_CHOICE_STIM_Y, "A")
    CB = ChoiceStim(R_CHOICE_STIM_X, R_CHOICE_STIM_Y, "B")
    CC = ChoiceStim(R_CHOICE_STIM_X, R_CHOICE_STIM_Y, "C")
    InitA = InitialLinkStim(R_I_STIM_X, R_I_STIM_Y, "A")
    InitB = InitialLinkStim(R_I_STIM_X, R_I_STIM_Y, "B")
    InitC = InitialLinkStim(R_I_STIM_X, R_I_STIM_Y, "C")
    
def drawBlankLeftChoice():
    
    global win
    rect = visual.Rect(win, lineWidth = 4, width = leftChoice.width, height = leftChoice.height, pos = (leftChoice.x, leftChoice.y), units = "pix", lineColor = leftChoice.outlineColour, fillColor = leftChoice.fillColour)
    rect.draw()
   
def drawBlankCentreChoice():
    global win
    rect = visual.Rect(win, lineWidth = LINE_WIDTH, width = centreChoice.width, height = centreChoice.height, pos = (centreChoice.x, centreChoice.y), units = "pix", lineColor = centreChoice.outlineColour, fillColor = centreChoice.fillColour)
    rect.draw()

def drawBlankRightChoice():
    global win
    rect = visual.Rect(win, lineWidth = LINE_WIDTH, width = rightChoice.width, height = rightChoice.height, pos = (rightChoice.x, rightChoice.y), units = "pix", lineColor = rightChoice.outlineColour, fillColor = rightChoice.fillColour)
    rect.draw()
    
def drawBlankLeftIL():
    global win
    circ = visual.Circle(win, lineWidth = LINE_WIDTH, radius = leftInitLink.radius, pos = (leftInitLink.x, leftInitLink.y), units = "pix", lineColor = leftInitLink.outlineColour, fillColor = leftInitLink.fillColour)
    circ.draw()
    
def drawCentreInitialLink():
    global win
    circ = visual.Circle(win, lineWidth = LINE_WIDTH, radius = centreInitLink.radius, pos = (centreInitLink.x, centreInitLink.y), units = "pix", lineColor = centreInitLink.outlineColour, fillColor = centreInitLink.fillColour)
    circ.draw()
    
def drawBlankRightIL():
    global win
    circ = visual.Circle(win, lineWidth = LINE_WIDTH, radius = rightInitLink.radius, pos = (rightInitLink.x, rightInitLink.y), units = "pix", lineColor = rightInitLink.outlineColour, fillColor = rightInitLink.fillColour)
    circ.draw()
    
def drawInitialStims():
    drawBlankLeftChoice()
    drawBlankCentreChoice()
    drawBlankRightChoice()
    drawBlankLeftIL()
    #Reserved for future use
    #drawCentreInitialLink()
    drawBlankRightIL()
    win.flip()
    
def drawtermLinkA():
    global win, termLinkACirc

    drawBlankLeftChoice()
    drawBlankCentreChoice()
    drawBlankRightChoice()

    if termLinkA.x >= 0:
        drawBlankLeftIL()

    else:
        drawBlankRightIL()

    termLinkACirc = visual.Circle(win, lineWidth = LINE_WIDTH, radius = termLinkA.radius, pos = (termLinkA.x, termLinkA.y), units = "pix", lineColor = termLinkA.outlineColour, fillColor = termLinkA.fillColour)
    termLinkACirc.draw()
    win.flip()
    
def drawtermLinkB():
    global win, termLinkBCirc

    drawBlankLeftChoice()
    drawBlankCentreChoice()
    drawBlankRightChoice()

    if termLinkB.x >= 0:
        drawBlankLeftIL()

    else:
        drawBlankRightIL()

    termLinkBCirc = visual.Circle(win, lineWidth = LINE_WIDTH, radius = termLinkB.radius, pos = (termLinkB.x, termLinkB.y), units = "pix", lineColor = termLinkB.outlineColour, fillColor = termLinkB.fillColour)
    termLinkBCirc.draw()
    win.flip()
    
def drawtermLinkC():
    global win,termLinkCCirc

    drawBlankLeftChoice()
    drawBlankCentreChoice()
    drawBlankRightChoice()

    if termLinkC.x >= 0:
        drawBlankLeftIL()

    else:
        drawBlankRightIL()

    termLinkCCirc = visual.Circle(win, lineWidth = LINE_WIDTH, radius = termLinkC.radius, pos = (termLinkC.x, termLinkC.y), units = "pix", lineColor = termLinkC.outlineColour, fillColor = termLinkC.fillColour)
    termLinkCCirc.draw()
    win.flip()
    
def drawtermLinkD():
    global win, termLinkDCirc

    drawBlankLeftChoice()
    drawBlankCentreChoice()
    drawBlankRightChoice()

    if termLinkD.x >= 0:
        drawBlankLeftIL()

    else:
        drawBlankRightIL()

    termLinkDCirc = visual.Circle(win, lineWidth = LINE_WIDTH, radius = termLinkD.radius, pos = (termLinkD.x, termLinkD.y), units = "pix", lineColor = termLinkD.outlineColour, fillColor = termLinkD.fillColour)
    termLinkDCirc.draw()
    win.flip()
    
def drawCA():
    global win, CARect

    drawBlankLeftChoice()
    drawBlankCentreChoice()
    drawBlankRightChoice()
    drawBlankLeftIL()
    drawBlankRightIL()


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

    drawBlankLeftChoice()
    drawBlankCentreChoice()
    drawBlankRightChoice()
    drawBlankLeftIL()
    drawBlankRightIL()

    CBInnerRect = visual.Rect(win, lineWidth = LINE_WIDTH, width = 30, height = 30, pos = (CB.x, CB.y), units = "pix", lineColor = "Black", fillColor = "White")
    CBRect = visual.Rect(win, lineWidth = LINE_WIDTH, width = CB.width, height = CB.height, pos = (CB.x, CB.y), units = "pix", lineColor = CB.outlineColour, fillColor = "White")
    CBRect.draw()
    CBInnerRect.draw()
    win.flip()
    
def drawCC():
    global win, CCRect

    drawBlankLeftChoice()
    drawBlankCentreChoice()
    drawBlankRightChoice()
    drawBlankLeftIL()
    drawBlankRightIL()

    CCRect = visual.Rect(win, lineWidth = LINE_WIDTH, width = CC.width, height = CC.height, pos = (CC.x, CC.y), units = "pix", lineColor = CC.outlineColour, fillColor = "White")
    CCInnerCirc = visual.Circle(win, lineWidth = LINE_WIDTH, radius = 15, pos = (CC.x, CC.y), units = "pix", lineColor = "Black", fillColor = "Black")
    CCRect.draw()
    CCInnerCirc.draw()
    win.flip()
    
def drawInitA():
    global win, InitACirc

    drawBlankLeftChoice()
    drawBlankCentreChoice()
    drawBlankRightChoice()

    if InitA.x >= 0:
        drawBlankLeftIL()

    else:
        drawBlankRightIL()

    InitACirc = visual.Circle(win, lineWidth = LINE_WIDTH, radius = InitA.radius, pos = (InitA.x, InitA.y), units = "pix", lineColor = InitA.outlineColour, fillColor = "White")
    InitAVertLine = visual.Line(win, start = (InitA.x, (InitA.y + InitA.radius)), end = (InitA.x, (InitA.y - InitA.radius)), lineWidth = LINE_WIDTH, units = "pix", lineColor = "Black")
    InitACirc.draw()
    InitAVertLine.draw()
    win.flip()
    
def drawInitB():
    global win, InitBCirc

    drawBlankLeftChoice()
    drawBlankCentreChoice()
    drawBlankRightChoice()

    topStart = ((InitB.x - 35), (InitB.y + 20))
    topEnd = ((InitB.x + 35), (InitB.y + 20))
    midStart = ((InitB.x - InitB.radius), (InitB.y))
    midEnd = ((InitB.x + InitB.radius), (InitB.y))
    bottomStart = ((InitB.x - 35), (InitB.y - 20))
    bottomEnd = ((InitB.x + 35), (InitB.y - 20))

    if InitB.x >= 0:
        drawBlankLeftIL()

    else:
        drawBlankRightIL()

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

    drawBlankLeftChoice()
    drawBlankCentreChoice()
    drawBlankRightChoice()

    if InitC.x >= 0:
        drawBlankLeftIL()

    else:
        drawBlankRightIL()

    InitCCirc = visual.Circle(win, lineWidth = LINE_WIDTH, radius = InitC.radius, pos = (InitC.x, InitC.y), units = "pix", lineColor = InitC.outlineColour, fillColor = InitC.fillColour)
    InitCCirc.draw()
    win.flip()
    
def doTraining(interTrialInterval, peckRewardRatio, rewardForNoEffort, stimuli):
    global nPecksToReward, ITI, allTrialsFinished, datafile, writer, peckNum, row, rewardTime, stimDur
    if str(experimentParameters[5]) == "No":
        rewardTime = experimentParameters[3]
        stimDur = experimentParameters[4]
        ITI = interTrialInterval

    nPecksToReward = peckRewardRatio
    pecksOnTarget = 0
    allTrialsFinished = False
    peckNum = 0
    row = 0
    index = 0
    trialTime = 0
    stimType = ""
    victoryFlag = False
    stimSide = "R"
    

    random.shuffle(stimuli) #Present stimuli in a random order

    core.wait(1) #Give the CPU a bit of a break
    
    startTime = time.time() #Set a timer to record times for the log
    expTimer = core.CountdownTimer(FORTYFIVE_MINUTES)
    while(expTimer.getTime > 0):

        #core.wait(0.5) # TESTING
            
        if stimuli[index][1] == "termLinkA":
            stimType = "termLinkA"
            if stimuli[index][0] == "L":
                termLinkA.x *= -1
                stimSide = "L"
                
            drawtermLinkA()

            stimTimer = core.CountdownTimer(stimDur)
            while (stimTimer.getTime() > 0):
                    
                event.clearEvents()
                mouse.clickReset()
                #get bird's input. If it pecks the target, break and give the bird food. Otherwise, increase the peck count and keep looking for input
                if mouse.isPressedIn(termLinkACirc):
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
                termLinkA.x *= -1
                
           
        elif stimuli[index][1] == "termLinkB":
            stimType = "termLinkB"
            if stimuli[index][0] == "L":
                termLinkB.x *= -1
                stimSide = "L"
                
            drawtermLinkB()

            stimTimer = core.CountdownTimer(stimDur)
            while (stimTimer.getTime() > 0):
                    
                event.clearEvents()
                mouse.clickReset()
                #get bird's input. If it pecks the target, break give the bird food. Otherwise, increase the peck count and keep looking for input
                if mouse.isPressedIn(termLinkBCirc):
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
                termLinkB.x *= -1
            pass
            
        elif stimuli[index][1] == "termLinkC":
            stimType = "termLinkC"
            if stimuli[index][0] == "L":
                termLinkC.x *= -1
                stimSide = "L"
                
            drawtermLinkC()

            stimTimer = core.CountdownTimer(stimDur)
            while (stimTimer.getTime() > 0):
                    
                event.clearEvents()
                mouse.clickReset()
                #get bird's input. If it pecks the target, break give the bird food. Otherwise, increase the peck count and keep looking for input
                if mouse.isPressedIn(termLinkCCirc):
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
                termLinkC.x *= -1
                
            pass
            
        elif stimuli[index][1] == "termLinkD":
            stimType = "termLinkD"
            if stimuli[index][0] == "L":
                termLinkD.x *= -1
                stimSide = "L"
                
            drawtermLinkD()

            stimTimer = core.CountdownTimer(stimDur)
            while (stimTimer.getTime() > 0):
                    
                event.clearEvents()
                mouse.clickReset()
                #get bird's input. If it pecks the target, break give the bird food. Otherwise, increase the peck count and keep looking for input
                if mouse.isPressedIn(termLinkDCirc):
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
                termLinkD.x *= -1
                
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
            elif stimuli[index][0] == "C":
                CA.x = 0
                stimSide = "C"

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
                CB.x *= -1
                stimSide = "L"
            elif stimuli[index][0] == "C":
                CB.x = 0
                stimSide = "C"
                
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
            elif stimuli[index][0] == "C":
                CC.x = 0
                stimSide = "C"
                
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

        if ((rewardForNoEffort == True) or (victoryFlag == True and rewardForNoEffort == False)):
            giveReward(rewardTime) # CHANGE 0 TO REWARD TIME LATER

        displayBlankPanel(ITI) # 5 for testing, change to ITI after
        index += 1
        row += 1
        if index >= len(stimuli):
            index = 0
        trialTime = time.time() - startTime
        writer.writerow([row, peckNum, trialTime*60, stimType, 
                                  stimSide, victoryFlag, pecksOnTarget, 'Accuracy'])
        
        peckNum = 0
        victoryFlag = False
        pecksOnTarget = 0
        stimSide = "R"
    
    
def doStimPairing(interTrialInterval, forcedChoiceTrialCount, choiceTrialCount, timeout):
    global experimentParameters, stimDur, ITI, peckNum, terminalProbabilityCounter1, terminalProbabilityCounter2, termProbList1, termProbList2
    print("PHASE 3")

    # Start csv file

    if str(experimentParameters[5]) == "No":
        rewardTime = experimentParameters[3]
        stimDur = experimentParameters[4]
        ITI = interTrialInterval

    timeout = 5 ## TESTING

    initialLinks = randomizeInit(forcedChoiceTrialCount, choiceTrialCount)

    #80% is 1, 20% is 0
    termProbList1 = [1,1,1,1,1,1,1,1,0,0]
    termProbList2 = [1,1,1,1,1,1,1,1,0,0]

    terminalProbabilityCounter1 = 0
    terminalProbabilityCounter2 = 0
    nPecksToReward = 1
    initVictoryFlag = False
    termVictoryFlag = False
    peckNum = 0
    pecksOnTarget = 0
    trialCount = 0

    setTimer = core.CountdownTimer(FORTYFIVE_MINUTES)
    while(setTimer.getTime() > 0):

        while (trialCount < (forcedChoiceTrialCount + choiceTrialCount)):

            for i in range(0,len(initialLinks)):

                ## HANDLE THE FIRST INITIAL LINK
                if initialLinks[i][0].name == "A":
                    if initialLinks[i][1] == "L":
                        InitA.x *= -1
                        

                    drawInitA()

                    stimTimer = core.CountdownTimer(stimDur)
                    while (stimTimer.getTime() > 0):
                            
                        event.clearEvents()
                        mouse.clickReset()
                        if mouse.isPressedIn(InitACirc):
                            print("Clicked in target") # TESTING ONLY
                            peckNum += 1
                            pecksOnTarget += 1
                            event.clearEvents()
                            if pecksOnTarget == nPecksToReward:
                                initVictoryFlag = True
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

                    if initialLinks[i][1] == "L":
                        InitA.x *= -1

                ## HANDLE THE SECOND INITIAL LINK
                elif initialLinks[i][0].name == "B":
                    if initialLinks[i][1] == "L":
                        InitB.x *= -1
                        

                    drawInitB()

                    stimTimer = core.CountdownTimer(stimDur)
                    while (stimTimer.getTime() > 0):
                            
                        event.clearEvents()
                        mouse.clickReset()
                        if mouse.isPressedIn(InitBCirc):
                            print("Clicked in target") # TESTING ONLY
                            peckNum += 1
                            pecksOnTarget += 1
                            event.clearEvents()
                            if pecksOnTarget == nPecksToReward:
                                initVictoryFlag = True
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

                    if initialLinks[i][1] == "L":
                        InitB.x *= -1

                elif initialLinks[i][0].name == "choice":

                    drawInits() ##### Draw both initial links

                    pecksOnInitA = 0
                    pecksOnInitB = 0
                    stimTimer = core.CountdownTimer(stimDur)
                    while (stimTimer.getTime() > 0):
                            
                        event.clearEvents()
                        mouse.clickReset()

                        if mouse.isPressedIn(InitACirc):
                            print("Clicked in target A") # TESTING ONLY
                            peckNum += 1
                            pecksOnInitA += 1
                            event.clearEvents()
                            if pecksOnInitA == nPecksToReward:
                                initVictoryFlag = True
                                pecked = "A"
                                break

                        elif mouse.isPressedIn(InitBCirc):
                            print("Clicked in target B") # TESTING ONLY
                            peckNum += 1
                            pecksOnInitB += 1
                            event.clearEvents()
                            if pecksOnInitB == nPecksToReward:
                                initVictoryFlag = True
                                pecked = "B"
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

                if initVictoryFlag == True:

                        # Present terminal links

                        if initialLinks[i][0].name == "A" or initialLinks[i][0].name == "B":
                            if initialLinks[i][2] == "1":
                                termVictoryFlag, termStimPecked = displayTLink1(ITI, timeout, nPecksToReward)

                            elif initialLinks[i][2] == "2":
                                termVictoryFlag, termStimPecked = displayTLink2(ITI, timeout, nPecksToReward)

                        elif initialLinks[i][0].name == "choice":
                            for j in range (2,4):
                                if pecked == initialLinks[i][j][0].name:

                                    if initialLinks[i][j][2] == "1":
                                        termVictoryFlag, termStimPecked = displayTLink1(ITI, timeout, nPecksToReward)

                                    elif initialLinks[i][j][2] == "2":
                                        termVictoryFlag, termStimPecked = displayTLink2(ITI, timeout, nPecksToReward)

                        if termVictoryFlag == True:


                            if termStimPecked == "A":
                                birdAte = giveReward(1)
                            elif termStimPecked == "D":
                                birdAte = giveReward(0)
                            elif termStimPecked == "B":
                                bidAte = giveReward(.5)
                            elif termStimPecked == "C":
                                birdAte = giveReward(.5)

                        # If the peck the terminal link before timeout, give reward based on probability

                displayBlankPanel(ITI)

                #write to csv file
                pecksOnTarget = 0
                pecksOnInitB = 0
                pecksOnInitA = 0
                initVictoryFlag = False
                termVictoryFlag = False
                peckNum = 0

            trialCount += 1


    
def randomizeInit(forcedChoiceTrialCount, choiceTrialCount):
    global InitA, InitB
    print("Randomizing Initial Links")

    choiceInit = InitialLinkStim(0,0,"choice")
    initList = [InitA, InitB]
    sideList = ["L", "R"]
    termLinkList = ["1", "2"]
    outputList = []

    random.shuffle(initList)
    random.shuffle(sideList)
    random.shuffle(termLinkList)

    init1List = [initList[0], sideList[0], termLinkList[0]] 
    init2List = [initList[1], sideList[1], termLinkList[1]] 
    init3List = [choiceInit, "C", init1List, init2List]

    tempCounter = 0
    while (tempCounter < (forcedChoiceTrialCount/2)):

        outputList.append(init1List)
        outputList.append(init2List)
        tempCounter += 1
    tempCounter = 0

    while (tempCounter < choiceTrialCount):
        outputList.append(init3List)
        tempCounter += 1

    random.shuffle(outputList)

    return outputList

def displayTLink1(interTrialInterval, timeout, nPecksToReward):
    global peckNum, terminalProbabilityCounter1, termLinkACirc, termLinkDCirc, termProbList1
    #displayBlankPanel(interTrialInterval)
    print("Presenting Terminal Link 1")

    displayBlankPanel(.25) # Make it so that the animal doesn't peck at the same thing too quickly

    pecksOnTargetA = 0
    pecksOnTargetD = 0
    termVictoryFlag = False
    termStimPecked = ""

    if terminalProbabilityCounter1 >= 10:
        termProbabilityCounter1 = 0

    if terminalProbabilityCounter1 == 0:
        random.shuffle(termProbList1)

    if termProbList1[terminalProbabilityCounter1] == 0:
        #20% chance of getting term link B
        termLinkA.x *= -1
        drawtermLinkA()
        termLinkA.x *= -1

    elif termProbList1[terminalProbabilityCounter1] == 1:
        #80% chance of getting term link C
        drawtermLinkD()

    termLinkTimer = core.CountdownTimer(timeout)
    while (termLinkTimer.getTime() <= timeout):

        event.clearEvents()
        mouse.clickReset()
        if termProbList1[terminalProbabilityCounter1] == 0:
            if mouse.isPressedIn(termLinkACirc):
                print("Clicked in target A") # TESTING ONLY
                peckNum += 1
                pecksOnTargetA += 1 
                event.clearEvents()
                if pecksOnTargetA == nPecksToReward:
                    termVictoryFlag = True
                    termStimPecked = "A"
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
                
        elif termProbList1[terminalProbabilityCounter1] == 1:
            if mouse.isPressedIn(termLinkDCirc):
                print("Clicked in target D") # TESTING ONLY
                peckNum += 1
                pecksOnTargetD += 1
                event.clearEvents()
                if pecksOnTargetD == nPecksToReward:
                    termVictoryFlag = True
                    termStimPecked = "D"
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

    terminalProbabilityCounter1 += 1

    return termVictoryFlag, termStimPecked


def displayTLink2(interTrialInterval, timeout, nPecksToReward):
    global peckNum, terminalProbabilityCounter2, termLinkBCirc, termLinkCCirc, termProbList2
    #displayBlankPanel(interTrialInterval)
    print ("Presenting Terminal Link 2")

    displayBlankPanel(.25) # Make it so that the animal doesn't peck at the same thing too quickly

    pecksOnTargetB = 0
    pecksOnTargetC = 0
    termVictoryFlag = False
    termStimPecked = ""

    if terminalProbabilityCounter2 == 10:
        terminalProbabilityCounter2 = 0

    if terminalProbabilityCounter2 == 0:
        random.shuffle(termProbList2)

    if termProbList2[terminalProbabilityCounter2] == 0:
        #20% chance of getting term link B
        termLinkB.x *= -1
        drawtermLinkB()
        termLinkB.x *= -1

    elif termProbList2[terminalProbabilityCounter2] == 1:
        #80% chance of getting term link C
        drawtermLinkC()

    termLinkTimer = core.CountdownTimer(timeout)
    while (termLinkTimer.getTime() <= timeout):

        event.clearEvents()
        mouse.clickReset()
        if termProbList2[terminalProbabilityCounter2] == 0: 
            if mouse.isPressedIn(termLinkBCirc):
                print("Clicked in target B") # TESTING ONLY
                peckNum += 1
                pecksOnTargetB += 1
                event.clearEvents()
                if pecksOnTargetB == nPecksToReward:
                    termVictoryFlag = True
                    termStimPecked = "B"
                    break

            elif (mouse.getPressed()[0] == 1):
                while(mouse.getPressed()[0] == 1): 
                    if (mouse.getPressed()[0] == 0):
                        break
                    
                peckNum += 1
                event.clearEvents()
                
            if event.getKeys(["escape"]):
                print("User pressed escape")
                print(str(peckNum))
                exit()

        elif termProbList2[terminalProbabilityCounter2] == 1: 
            if mouse.isPressedIn(termLinkCCirc):
                print("Clicked in target C") # TESTING ONLY
                peckNum += 1
                pecksOnTargetC += 1 #IF THIS IS LEFT THE WAY IT IS, IT WILL ACCEPT PECKS TO BOTH TO SATISFY. UNACCEPTABLE. FIX
                event.clearEvents()
                if pecksOnTargetC == nPecksToReward:
                    termVictoryFlag = True
                    termStimPecked = "C"
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

    terminalProbabilityCounter2 += 1

    return termVictoryFlag, termStimPecked

def drawInits():
    global win, InitACirc, InitBCirc

    InitB.x *= -1

    topStart = ((InitB.x - 35), (InitB.y + 20))
    topEnd = ((InitB.x + 35), (InitB.y + 20))
    midStart = ((InitB.x - InitB.radius), (InitB.y))
    midEnd = ((InitB.x + InitB.radius), (InitB.y))
    bottomStart = ((InitB.x - 35), (InitB.y - 20))
    bottomEnd = ((InitB.x + 35), (InitB.y - 20))

    drawBlankLeftChoice()
    drawBlankCentreChoice()
    drawBlankRightChoice()

    #INIT A

    InitACirc = visual.Circle(win, lineWidth = LINE_WIDTH, radius = InitA.radius, pos = (InitA.x, InitA.y), units = "pix", lineColor = InitA.outlineColour, fillColor = "White")
    InitAVertLine = visual.Line(win, start = (InitA.x, (InitA.y + InitA.radius)), end = (InitA.x, (InitA.y - InitA.radius)), lineWidth = LINE_WIDTH, units = "pix", lineColor = "Black")

    #INITB

    InitBCirc = visual.Circle(win, lineWidth = LINE_WIDTH, radius = InitB.radius, pos = (InitB.x, InitB.y), units = "pix", lineColor = InitB.outlineColour, fillColor = "White")
    InitBTopLine = visual.Line(win, start = (topStart), end = (topEnd), lineWidth = LINE_WIDTH, units = "pix", lineColor = "Black")
    InitBMidLine = visual.Line(win, start = (midStart), end = (midEnd), lineWidth = LINE_WIDTH, units = "pix", lineColor = "Black")
    InitBBottomLine = visual.Line(win, start = (bottomStart), end = (bottomEnd), lineWidth = LINE_WIDTH, units = "pix", lineColor = "Black")
    
    InitACirc.draw()
    InitAVertLine.draw()
    InitBCirc.draw()
    InitBTopLine.draw()
    InitBMidLine.draw()
    InitBBottomLine.draw()

    InitB.x *= -1

    win.flip()

def drawTermLinksBC():
    global win, termLinkBCirc, termLinkCCirc

    drawBlankLeftChoice()
    drawBlankCentreChoice()
    drawBlankRightChoice()

    termLinkBCirc = visual.Circle(win, lineWidth = LINE_WIDTH, radius = termLinkB.radius, pos = (termLinkB.x * -1, termLinkB.y), units = "pix", lineColor = termLinkB.outlineColour, fillColor = termLinkB.fillColour)
    termLinkCCirc = visual.Circle(win, lineWidth = LINE_WIDTH, radius = termLinkC.radius, pos = (termLinkC.x, termLinkC.y), units = "pix", lineColor = termLinkC.outlineColour, fillColor = termLinkC.fillColour)
    termLinkBCirc.draw()
    termLinkCCirc.draw()
    win.flip()

def drawTermLinksAD():
    global win, termLinkACirc, termLinkDCirc

    drawBlankLeftChoice()
    drawBlankCentreChoice()
    drawBlankRightChoice()

    termLinkACirc = visual.Circle(win, lineWidth = LINE_WIDTH, radius = termLinkA.radius, pos = (termLinkA.x * -1, termLinkA.y), units = "pix", lineColor = termLinkA.outlineColour, fillColor = termLinkA.fillColour)
    termLinkDCirc = visual.Circle(win, lineWidth = LINE_WIDTH, radius = termLinkD.radius, pos = (termLinkD.x, termLinkD.y), units = "pix", lineColor = termLinkD.outlineColour, fillColor = termLinkD.fillColour)
    termLinkACirc.draw()
    termLinkDCirc.draw()
    win.flip()

def giveReward(probability):
    print("Giving a reward, with the probability of reinforcement of " + str(probability))

    #drawBlankPanel(ITI)

    birdAte = False

    return birdAte

def doExpPhase(Reversal, forcedChoiceTrialCount, choiceTrialCount):
    global experimentParameters, stimDur, ITI, peckNum, terminalProbabilityCounter1, terminalProbabilityCounter2, termProbList1, termProbList2
    print("PHASE 4")

    # Start csv file

    if str(experimentParameters[5]) == "No":
        rewardTime = experimentParameters[3]
        stimDur = experimentParameters[4]
        ITI = interTrialInterval

    timeout = 5 ## TESTING

    #80% is 1, 20% is 0
    termProbList1 = [1,1,1,1,1,1,1,1,0,0]
    termProbList2 = [1,1,1,1,1,1,1,1,0,0]

    terminalProbabilityCounter1 = 0
    terminalProbabilityCounter2 = 0
    nPecksToReward = 1
    choiceVictortFlag = False
    initVictoryFlag = False
    termVictoryFlag = False
    peckNum = 0
    pecksOnTarget = 0
    trialCount = 0

    choiceStims = randomizeChoiceStims(forcedChoiceTrialCount, choiceTrialCount)
    initStims = randomizeInit(2,1)

    setTimer = core.CountdownTimer(FORTYFIVE_MINUTES)
    while(setTimer.getTime() > 0):

        while (trialCount < (forcedChoiceTrialCount + choiceTrialCount)):

            for i in range(0,len(choiceStims)):

                ## HANDLE THE FIRST CHOICE STIM
                if choiceStims[i][0].name == "A":
                    if choiceStims[i][1] == "L":
                        CA.x *= -1
                    elif choiceStims[i][1] == "C":
                        lastX = CA.x
                        CA.x = 0
                        

                    drawCA()

                    stimTimer = core.CountdownTimer(stimDur)
                    while (stimTimer.getTime() > 0):
                            
                        event.clearEvents()
                        mouse.clickReset()
                        if mouse.isPressedIn(CARect):
                            print("Clicked in target") # TESTING ONLY
                            peckNum += 1
                            pecksOnTarget += 1
                            event.clearEvents()
                            if pecksOnTarget == nPecksToReward:
                                choiceVictoryFlag = True
                                peckedChoice = "A"
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

                    if choiceStims[i][1] == "L":
                        CA.x *= -1
                    elif choiceStims[i][1] == "C":
                        CA.x = lastX

                ## HANDLE THE SECOND CHOICE STIM
                elif choiceStims[i][0].name == "B":
                    if choiceStims[i][1] == "L":
                        CB.x *= -1
                    elif choiceStims[i][1] == "C":
                        lastX = CB.x
                        CB.x = 0
                        

                    drawCB()

                    stimTimer = core.CountdownTimer(stimDur)
                    while (stimTimer.getTime() > 0):
                            
                        event.clearEvents()
                        mouse.clickReset()
                        if mouse.isPressedIn(CBRect):
                            print("Clicked in target") # TESTING ONLY
                            peckNum += 1
                            pecksOnTarget += 1
                            event.clearEvents()
                            if pecksOnTarget == nPecksToReward:
                                choiceVictoryFlag = True
                                peckedChoice = "B"
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

                    if choiceStims[i][1] == "L":
                        CB.x *= -1
                    elif choiceStims[i][1] == "C":
                        CB.x = lastX

                ## HANDLE THE THIRD CHOICE STIM
                elif choiceStims[i][0].name == "C":
                    if choiceStims[i][1] == "L":
                        CC.x *= -1
                    elif choiceStims[i][1] == "C":
                        lastX = CC.x
                        CC.x = 0
                        

                    drawCC()

                    stimTimer = core.CountdownTimer(stimDur)
                    while (stimTimer.getTime() > 0):
                            
                        event.clearEvents()
                        mouse.clickReset()
                        if mouse.isPressedIn(CCRect):
                            print("Clicked in target") # TESTING ONLY
                            peckNum += 1
                            pecksOnTarget += 1
                            event.clearEvents()
                            if pecksOnTarget == nPecksToReward:
                                choiceVictoryFlag = True
                                peckedChoice = "C"
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

                    if choiceStims[i][1] == "L":
                        CB.x *= -1
                    elif choiceStims[i][1] == "C":
                        CB.x = lastX

                elif choiceStims[i][0].name == "choice":

                    drawChoices(choiceStims[i][1][0].name, choiceStims[i][1][0].name) ##### Draw both initial links

                    pecksOnChoiceA = 0
                    pecksOnChoiceB = 0
                    pecksOnChoiceC = 0
                    stimTimer = core.CountdownTimer(stimDur)
                    while (stimTimer.getTime() > 0):
                            
                        event.clearEvents()
                        mouse.clickReset()

                        if choiceStims[1][1][0].name == "A" or choiceStims[1][2][0].name == "A":

                            if mouse.isPressedIn(CARect):
                                print("Clicked in target A") # TESTING ONLY
                                peckNum += 1
                                pecksOnInitA += 1
                                event.clearEvents()
                                if pecksOnChoiceA == nPecksToReward:
                                    choiceVictoryFlag = True
                                    peckedChoice = "A"
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

                        if choiceStims[1][1][0].name == "B" or choiceStims[1][2][0].name == "B":
                            if mouse.isPressedIn(CBRect):
                                print("Clicked in target B") # TESTING ONLY
                                peckNum += 1
                                pecksOnInitB += 1
                                event.clearEvents()
                                if pecksOnChoiceB == nPecksToReward:
                                    choiceVictoryFlag = True
                                    peckedChoice = "B"
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

                        if choiceStims[1][1][0].name == "C" or choiceStims[1][2][0].name == "C":
                            if mouse.isPressedIn(CCRect):
                                print("Clicked in target C") # TESTING ONLY
                                peckNum += 1
                                pecksOnInitB += 1
                                event.clearEvents()
                                if pecksOnChoiceC == nPecksToReward:
                                    choiceVictoryFlag = True
                                    peckedChoice = "C"
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

                if initVictoryFlag == True: ## HAVE NOT EDITED THIS METHOD PAST THIS POINT. CONTINUE LATER.

                        # Present terminal links

                        if initialLinks[i][0].name == "A" or initialLinks[i][0].name == "B":
                            if initialLinks[i][2] == "1":
                                termVictoryFlag, termStimPecked = displayTLink1(ITI, timeout, nPecksToReward)

                            elif initialLinks[i][2] == "2":
                                termVictoryFlag, termStimPecked = displayTLink2(ITI, timeout, nPecksToReward)

                        elif initialLinks[i][0].name == "choice":
                            for j in range (2,4):
                                if pecked == initialLinks[i][j][0].name:

                                    if initialLinks[i][j][2] == "1":
                                        termVictoryFlag, termStimPecked = displayTLink1(ITI, timeout, nPecksToReward)

                                    elif initialLinks[i][j][2] == "2":
                                        termVictoryFlag, termStimPecked = displayTLink2(ITI, timeout, nPecksToReward)

                        if termVictoryFlag == True:


                            if termStimPecked == "A":
                                birdAte = giveReward(1)
                            elif termStimPecked == "D":
                                birdAte = giveReward(0)
                            elif termStimPecked == "B":
                                bidAte = giveReward(.5)
                            elif termStimPecked == "C":
                                birdAte = giveReward(.5)

                        # If the peck the terminal link before timeout, give reward based on probability

                displayBlankPanel(ITI)

                #write to csv file
                pecksOnTarget = 0
                pecksOnInitB = 0
                pecksOnInitA = 0
                initVictoryFlag = False
                termVictoryFlag = False
                peckNum = 0

            trialCount += 1

    # Match initial links with terminal link sets

    # Present choice stimuli randomly, accoring to spec

    # Present the matched initial link

    # Present the matched terminal link based on probability

def drawChoices(choice1, choice2):
    pass

def randomizeChoiceStims(forcedChoiceTrialCount, choiceTrialCount):
    global CA, CB, CC
    print("Randomizing Initial Links")

    choiceTrialStim = ChoiceStim(0,0,"choice")
    
    choiceList = [CA, CB, CC]
    sideList = ["L", "R", "C"]
    initList = ["A", "B", "choice"]
    outputList = []

    random.shuffle(choiceList)
    random.shuffle(sideList)
    random.shuffle(initList)

    choice1List = [choiceList[0], sideList[0], initList[0]] 
    choice2List = [choiceList[1], sideList[1], initList[1]]
    choice3List = [choiceList[2], sideList[2], initList[2]]
    choice4List = [choiceTrialStim, choice1List, choice2List]
    choice5List = [choiceTrialStim, choice1List, choice3List]
    choice6List = [choiceTrialStim, choice2List, choice3List]

    tempCounter = 0
    while (tempCounter < (forcedChoiceTrialCount/3)):

        outputList.append(choice1List)
        outputList.append(choice2List)
        outputList.append(choice3List)
        tempCounter += 1
    tempCounter = 0

    while (tempCounter < choiceTrialCount/3):
        outputList.append(choice4List)
        outputList.append(choice5List)
        outputList.append(choice6List)
        tempCounter += 1

    random.shuffle(outputList)

    return outputList
    
def displayBlankPanel(duration):
    drawInitialStims()
    core.wait(duration)
    pass
    
    
def main():
    global datafile, filename, writer, stimDur, rewardTime, ITI, experimentParameters
    initializeStims()
    getUserInput()
    
    if userCancelled == True:
        exit()
        
    setup()

    now = datetime.datetime.now()
    dateAndTime = str(now.year) + "/" + str(now.month) + "/" + str(now.day) + " at " + str(now.hour) + ":" + str(now.minute)
    print(dateAndTime)

    writer.writerow(['Subject Number', 'Date and Time Run', 'Session Number', 'Research Assistant'])
    writer.writerow([str(experimentParameters[0]), dateAndTime, str(experimentParameters[1]), experimentParameters[6]])

    writer.writerow([])

    if str(experimentParameters[5]) == "Yes":
        rewardTime = 0
        stimDur = 5
        ITI = 1
    elif str(experimentParameters[5]) == "No":
        mouse.setVisible = False
    
    stimuli = [["L", "termLinkA"], ["R", "termLinkA"], ["L","termLinkB"], ["R","termLinkB"], ["L","termLinkC"], ["R","termLinkC"], ["L","termLinkD"], ["R","termLinkD"],
               ["L","CA"], ["R","CA"], ["L","CB"], ["R","CB"], ["L","CC"], ["R","CC"],
               ["L","InitA"], ["R","InitA"], ["L","InitB"], ["R","InitB"], ["C", "CA"], ["C", "CB"], ["C", "CC"]]#, ["L","InitC"], ["R","InitC"]]

    if str(experimentParameters[2]) == "Autoshaping (FR1)":
        writer.writerow(['Trial Number', 'Total Pecks', 'Elapsed Time', 'Stimulus Presented', 
                          'Stimulus Side', 'Satisfied No. Pecks', 'No. Pecks on Target', 'Accuracy', 'Reaction Times'])

        doTraining(240, 1, True, stimuli)
        
    elif str(experimentParameters[2])[0:16] == "Operant Training":

        if str(experimentParameters[2])[17:] == "(FR1)":
            print("FIXED RATIO 1 OT")

            writer.writerow(["FR 1"])
            writer.writerow([])
            writer.writerow(['Trial Number', 'Total Pecks', 'Elapsed Time', 'Stimulus Presented', 
                          'Stimulus Side', 'Satisfied No. Pecks', 'No. Pecks on Target', 'Accuracy', 'Reaction Times'])

            doTraining(60, 1, False, stimuli)
        elif str(experimentParameters[2])[17:] == "(FR3)":
            print("FIXED RATIO 3 OT")

            writer.writerow(["FR 3"])
            writer.writerow([])
            writer.writerow(['Trial Number', 'Total Pecks', 'Elapsed Time', 'Stimulus Presented', 
                          'Stimulus Side', 'Satisfied No. Pecks', 'No. Pecks on Target', 'Accuracy', 'Reaction Times'])

            doTraining(60, 3, False, stimuli)
        elif str(experimentParameters[2])[17:] == "(FR5)":
            print("FIXED RATIO 5 OT")

            writer.writerow(["FR 5"])
            writer.writerow([])
            writer.writerow(['Trial Number', 'Total Pecks', 'Elapsed Time', 'Stimulus Presented', 
                          'Stimulus Side', 'Satisfied No. Pecks', 'No. Pecks on Target', 'Accuracy', 'Reaction Times'])

            doTraining(60, 5, False, stimuli)
        
    elif str(experimentParameters[2]) == "Stim Pairing":

        writer.writerow(['Trial Number', 'Total Pecks', 'Elapsed Time', 'Initial Link Presented', 'Initial Link side', 'Terminal Link Presented',
                         'Terminal Link Side', 'Reaction Times'])

        doStimPairing(60, 40, 20, 30)
        
    elif str(experimentParameters[2]) == "Experimental Phase":
        writer.writerow(['Trial Number', 'Total Pecks', 'Elapsed Time', 'Choice Stimulus Presented', 'Choice Stimulus Side', 'Initial Link Presented', 'Initial Link side', 'Terminal Link Presented',
                         'Terminal Link Side', 'Reaction Times'])

        doExpPhase(False, 30, 30)
        
    elif str(experimentParameters[2]) == "Experimental Reversal":
        writer.writerow(['Trial Number', 'Total Pecks', 'Elapsed Time', 'Choice Stimulus Presented', 'Choice Stimulus Side', 'Initial Link Presented', 'Initial Link side', 'Terminal Link Presented',
                         'Terminal Link Side', 'Reaction Times'])

        doExpPhase(True, 30, 30)
    

if __name__ == "__main__":
    main()
    datafile.close() 
