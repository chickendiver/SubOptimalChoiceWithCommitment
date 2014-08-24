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


TOP_LEFT_X = (-1*(screen_width/3))
TOP_LEFT_Y = (screen_height/3)

TOP_RIGHT_X = (screen_width/3)
TOP_RIGHT_Y = (screen_height/3)

BOTTOM_LEFT_X = (-1*(screen_width/3))
BOTTOM_LEFT_Y = (-1*(screen_height/3))

BOTTOM_RIGHT_X = (screen_width/3)
BOTTOM_RIGHT_Y = (-1*(screen_height/3))

class button:

    def __init__(self, name, x, y, width, height):
          self.x = x
          self.y = y
          self.width = width
          self.height = height
          self.fillColour = "Gray"
          self.outlineColour = "Silver"
          self.name = name

    def set_fill (self, fillCol):
          self.fillColour = fillCol
          
    def set_outline (self, outlineCol):
          self.outlineColour = outlineCol

    def draw(self):
          global win
          self.rect = visual.Rect(win, lineWidth = 4, width = self.width, height = self.height, 
                                  pos = (self.x, self.y), units = "pix", 
                                  lineColor = self.outlineColour, fillColor = self.fillColour)
          self.rect.draw()


def setup():
    global win, datafile, writer, mouse
    
    #initialize the window
    win = visual.Window(fullscr = True, rgb = [-1.000,-1.000,-1.000], units = "pix", winType = "pyglet")
    
    #setup input from the mouse
    mouse = event.Mouse(visible = True)
    core.checkPygletDuringWait = True


def initializeFourButtons():

    print("Initializing Buttons")
    top_left_button = button("TL", TOP_LEFT_X, TOP_LEFT_Y, 50, 50)
    bottom_left_button = button("BL", BOTTOM_LEFT_X, BOTTOM_LEFT_Y, 50, 50)
    top_right_button = button("TR", TOP_RIGHT_X, TOP_RIGHT_Y, 50, 50)
    bottom_right_button = button("BR", BOTTOM_RIGHT_X, BOTTOM_RIGHT_Y, 50, 50)

    buttonList = []
    buttonList.append(top_left_button)
    buttonList.append(top_right_button)
    buttonList.append(bottom_left_button)
    buttonList.append(bottom_right_button)

    return buttonList

    print("Buttons initialized")

def drawButtons(buttonList):
    print("Drawing Buttons")
    for i in range(0,len(buttonList)):
      buttonList[i].draw()
      print("Drawing: " + buttonList[i].name)
    win.flip()

def waitForClicks(buttonList):
    global targetFlag

    peckNum = 0
    targetPeckNum = 0
    targetPeckRequired = 1
    targetPecked = ""

    targetFlag = False
    while (targetFlag == False):
      event.clearEvents()
      mouse.clickReset()

      
      if (mouse.getPressed()[0] == 1):
          pos = mouse.getPos()
          '''
          if buttonList[0].rect.contains(pos):
            targetPeckNum += 1
            if targetPeckNum >= targetPeckRequired:
              targetFlag = True
              targetPecked = buttonList[0].name
              continue

          elif buttonList[1].rect.contains(pos):
            targetPeckNum += 1
            if targetPeckNum >= targetPeckRequired:
              targetFlag = True
              targetPecked = buttonList[1].name
              continue

          elif buttonList[2].rect.contains(pos):
            targetPeckNum += 1
            if targetPeckNum >= targetPeckRequired:
              targetFlag = True
              targetPecked = buttonList[2].name
              continue

          elif buttonList[3].rect.contains(pos):
            targetPeckNum += 1
            if targetPeckNum >= targetPeckRequired:
              targetFlag = True
              targetPecked = buttonList[3].name
              continue
          '''
          for i in range (0,len(buttonList)):
            if buttonList[i].rect.contains(pos):
              targetPeckNum += 1
              if targetPeckNum >= targetPeckRequired:
                targetFlag = True
                targetPecked = buttonList[i].name
                break
          
          
      while (mouse.getPressed()[0] == 1):
        if (mouse.getPressed()[0] == 0):
          break

      peckNum += 1

      if event.getKeys(["escape"]):
        print("User pressed escape")
        targetPecked = "EXIT"
        exit()


    return targetPecked

def dealWithButtonPress(targetPecked):
  global message 

  if targetPecked == "TR":
    message = visual.TextStim(win, text='TOP RIGHT')
    message.setAutoDraw(True)  # automatically draw every frame
    win.flip()
    dropRightHopper()
    core.wait(2.0)
    raiseRightHopper()
    core.wait(2.0)

  elif targetPecked == "TL":
    message = visual.TextStim(win, text='TOP LEFT')
    message.setAutoDraw(True)  # automatically draw every frame
    win.flip()
    dropLeftHopper()
    core.wait(2.0)
    raiseLeftHopper()
    core.wait(2.0)

  elif targetPecked == "BL":
    message = visual.TextStim(win, text='BOTTOM LEFT')
    message.setAutoDraw(True)  # automatically draw every frame
    win.flip()
    turnOnFan()
    core.wait(10)
    turnOffFan()
    core.wait(2.0)

  elif targetPecked == "BR":
    message = visual.TextStim(win, text='BOTTOM RIGHT')
    message.setAutoDraw(True)  # automatically draw every frame
    win.flip()
    turnOnHouseLight()
    core.wait(2.0)
    turnOffHouseLight()
    core.wait(2.0)


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


def main():
    global message

    setup()
    buttonList = initializeFourButtons()

    targetPecked  = ""
    while (True):
      drawButtons(buttonList)
      targetPecked = waitForClicks(buttonList)
      dealWithButtonPress(targetPecked)
      message. setText("")
      win.flip()


if __name__ == "__main__":
    main()
