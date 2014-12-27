from sys import platform as _platform
import time, csv, random, datetime
from psychopy import visual, core, parallel, gui, event
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


# Raises the hopper and turns the light on.
def dropLeftHopper():
  global portValue
  portValue = portValue or 0x10
  portValue = portValue or 0x04

  parallelPort.setData(portValue)

# Raises the hopper and turns the light on.
def raiseLeftHopper():
  global portValue
  portValue = portValue or not 0x10
  portValue = portValue or not 0x04

  parallelPort.setData(portValue)

def dropRightHopper():
  global portValue
  portValue = portValue or 0x20
  portValue = portValue or 0x08

  parallelPort.setData(portValue)

def raiseRightHopper():
  global portValue
  portValue = portValue or not 0x20
  portValue = portValue or not 0x08

  parallelPort.setData(portValue)

def turnOnHouseLight():
  global portValue
  portValue = portValue or 0x01

  parallelPort.setData(portValue)

def turnOffHouseLight():
  global portValue
  portValue = portValue or not 0x01

  parallelPort.setData(portValue)

def turnOnFan():
  global portValue
  portValue = portValue or 0x02

  parallelPort.setData(portValue)

def turnOffFan():
  global portValue
  portValue = portValue or not 0x02

  parallelPort.setData(portValue)

# Reads from left IR beam. Called after hopper is dropped
def readLeftHopperBeam():
  #return if beam broken

  if testRunFlag == "Yes":
    value = 0
  else:
    value = readPort.readPort(0x0201) & 0x10
  return value

# Reads from right IR beam. Called after hopper is dropped
def readRightHopperBeam():
  #return if beam broken
  if testRunFlag == "Yes":
    value = 0
  else:
    value = readPort.readPort(0x0201) & 0x20
  return value

def main():
    hopperTimer = core.CountdownTimer(10)

    turnOnHouseLight()
    turnOnFan()

    dropRightHopper()
    while (hopperTimer.getTime() > 0):
        if readRightHopperBeam() > 0:
          break

    ## 1 second of hopper access
    core.wait(1)
    raiseRightHopper()

    hopperTimer.reset()

    dropLeftHopper()
    while (hopperTimer.getTime() > 0):
        if readLeftHopperBeam() > 0:
          break

    ## 1 second of hopper access
    core.wait(1)
    raiseLeftHopper()

    turnOffHouseLight()
    turnOffFan()



if __name__ == "__main__":
    main()
