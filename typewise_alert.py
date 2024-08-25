coolingTypes = {"PASSIVE_COOLING":35, "HI_ACTIVE_COOLING":45,"MED_ACTIVE_COOLING":40}

def infer_breach(value, lowerLimit, upperLimit):
  if value < lowerLimit:
    return 'TOO_LOW'
  if value > upperLimit:
    return 'TOO_HIGH'
  return 'NORMAL'

def get_upper_limit(coolingType):
  return coolingTypes[coolingType]
  
def classify_temperature_breach(coolingType, temperatureInC):
  lowerLimit = 0
  upperLimit = get_upper_limit(coolingType)
  return infer_breach(temperatureInC, lowerLimit, upperLimit)

def check_and_alert(alertTarget, batteryChar, temperatureInC):
  breachType = classify_temperature_breach(batteryChar['coolingType'], temperatureInC)
  if alertTarget == 'TO_CONTROLLER':
    send_to_controller(breachType)
  elif alertTarget == 'TO_EMAIL':
    send_to_email(breachType)

def send_to_controller(breachType):
  header = 0xfeed
  message = f'{header}, {breachType}'
  print_message(message)

def send_to_email(breachType):
  recepient = "a.b@c.com"
  if breachType == 'TOO_LOW':
    message = f'To: {recepient}\nHi, the temperature is too low'
    print_message(message)
  elif breachType == 'TOO_HIGH':
    message = f'To: {recepient}\nHi, the temperature is too high'
    print_message(message)
    
def print_message(message):
    print(message)
