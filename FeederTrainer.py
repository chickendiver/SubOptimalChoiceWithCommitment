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