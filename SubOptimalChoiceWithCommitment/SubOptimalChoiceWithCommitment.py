from sys import platform as _platform
from psychopy import visual, core, gui

if _platform == "linux" or _platform == "linux2":
    # linux
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

  
  # Const positions of all the stimuli locations
  # -------------------------------------------------------------------------------
  
L_CHOICE_STIM_X = (-1*(screen_width/3))
L_CHOICE_STIM_Y = (screen_width/16)
  
C_CHOICE_STIM_X = 0
C_CHOICE_STIM_Y = (screen_width/16)
  
R_CHOICE_STIM_X = (screen_width/3)
R_CHOICE_STIM_Y = (screen_width/16)
  
L_I_STIM_X = (-1*(screen_width/3))
L_I_STIM_Y = (-1*(screen_width/16))
  
'''C_I_STIM_X = 0
C_I_STIM_Y = (-1*(screen_width/16))'''
  
R_I_STIM_X = (screen_width/3)
R_I_STIM_Y = (-1*(screen_width/16))

LINE_WIDTH = 4

 # --------------------------------------------------------------------------- 
  
  # Circular Initial/Terminal Link objects, of which there will be 2 (1L, 1R)
class InitialLinkStim :
    def __init__(self, xCoord, yCoord):
        self.radius = 50
        self.x = xCoord
        self.y = yCoord
        self.fillColour = "Gray"
        self.outlineColour = "White"
        
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
        self.outlineColour = "White"
   
    def set_fill (self, fillCol):
        self.fillColour = fillCol
        
    def set_outline (self, outlineCol):
        self.outlineColour = outlineCol
    
def setup():
    global win
    win = visual.Window(fullscr = True, rgb = [-1.000,-1.000,-1.000])
 
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
    myDlg.addField('Condition:', choices = ['Autoshaping', 'Operant Training', 'Signalled A', 'Signalled B', 'Signalled C'])
    myDlg.addField('Reward Duration:', 10)
    myDlg.addField('Stimulus Timeout:', 60)
    myDlg.show()  # show dialog and wait for OK or Cancel
    
    if myDlg.OK:  # then the user pressed OK
        experimentParameters = myDlg.data
        print experimentParameters
    else:
        print 'user cancelled'
        userCancelled = True
        
def initializeStims():
    #Create new stimulus objects
    global leftChoice, centreChoice, rightChoice, leftInitLink, centreInitLink, rightInitLink
    leftChoice = ChoiceStim(L_CHOICE_STIM_X, L_CHOICE_STIM_Y)
    centreChoice = ChoiceStim(C_CHOICE_STIM_X, C_CHOICE_STIM_Y)
    rightChoice = ChoiceStim(R_CHOICE_STIM_X, R_CHOICE_STIM_Y)
    leftInitLink =  InitialLinkStim(L_I_STIM_X, L_I_STIM_Y)
    #centreInitLink = InitialLinkStim(C_I_STIM_X, C_I_STIM_Y)
    rightInitLink = InitialLinkStim(R_I_STIM_X, R_I_STIM_Y)
    
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
    #drawCentreInitialLink()
    drawRightInitialLink()
    win.flip()
    core.wait(2.0)
    
def main():
    initializeStims()
    getUserInput()
    
    if userCancelled == True:
        exit()
        
    setup()
    drawInitialStims()
    #testScrn()
    

if __name__ == "__main__":
    main()
 