import random
import re

pattern = r"a-zA-Z"

def roll_version_two(msg):
    print('Input: ', msg)
    msgs = re.split("\+|\-", msg)
    mods = re.findall("\+|\-", msg)
    output = []
    results = []
    customtext = ''
    returntext = ''
    #print("mods: ", mods)
    #print("msgs: ", msgs)
    for m in msgs:
        rolls = []
        x = m.split('d')
        try:
            amount_of_rolls = int(x[0])
            sides = int(x[1])
            for a in range(amount_of_rolls):
                rolls.append(random.randrange(1, sides+1))
                roll = 0
                for r in rolls:
                    roll += r
            output.append(rolls)
            results.append(roll)
        except IndexError:
            if m.find(' ') > 0:
                split_point = m.find(' ')
                additional_argument = m[0:split_point]
                customtext += m[split_point+1:]
            else:
                rolls.append(m)
                output.append(rolls)
                results.append(m)
        except ValueError:
            split_point = m.find(' ')
            additional_argument = m[0:split_point+1]
            customtext += m[split_point+1:]
            if additional_argument.find('d') > 0:
                x = additional_argument.split('d')
                amount_of_rolls = int(x[0])
                sides = int(x[1])
                for a in range(amount_of_rolls):
                    rolls.append(random.randrange(1, sides+1))
                    roll = 0
                    for r in rolls:
                        roll += r
                output.append(rolls)
                results.append(roll)
            else:
                split_point = m.find(' ')
                additional_argument = m[0:split_point]
                rolls.append(additional_argument)
                output.append(rolls)
                results.append(additional_argument)
            
    #print(output)
    #print("results: ", results)
    for r in range(len(results)):
        if r == 0:
            returntext += "> "
        for o in range(len(output[r])):
            if o == 0:
                returntext += "("
            if len(output[r]) != 1:
                if o == 0:
                    returntext += "["
                returntext += str(output[r][o])
                if o < len(output[r])-1:
                    returntext += "+"
                else:
                    returntext += "] = "
        returntext += f"**{str(results[r])}**)"
        try:
            returntext += f" {mods[r]} "
        except:
            returntext += ""
    total = int(results[0])
    for m in range(len(mods)):
        if mods[m] == '+':
            total += int(results[m+1])
        elif mods[m] == '-':
            total -= int(results[m+1])
    returntext += f" = **{str(total)}**"
    if len(customtext) > 0: 
        returntext += f"\n> {customtext}"
    print(returntext)
    return returntext

def roll_version_one(msg):
    print('Input: ', msg)
    msgs = msg.split(' ') #split the message by spaces into list msgs
    print(msgs)
    x = msgs[0].split('d') #split the first item in the list by d into list x
    rollAmt = x[0] #get first item from x which represents the amount of rolls
    sides = x[1] #get the second item from x which represents the sides of the dice
    rolls = [] #instantiate a list called rolls to hold all of the rolls
    x = 0 #create a counter utilizing x which is no longer needed for the above use
    while x < int(rollAmt): #loop through the amount of rolls
        rolls.append(random.randrange(1, int(sides))) #get a random number based on the number of sides on the die
        roll = 0 #instantiate roll to add up all of the rolls
        for r in rolls: #loop through rolls
            roll = roll + r #add up all of the rolls
        x += 1 #increment counter by 1
    try: #Try needed in case no + or - modifiers are added to roll
        x = 2 #reset counter to start at the position in list msgs to add/subtract to/from the rolls
        mod = 0 #instantiate mod to add/subtract to later
        while x <= len(msgs): #loop through msgs to find modifiers to add/subtract
            if msgs[x-1] == '+':
                try:
                    mod = mod + int(msgs[x])
                except ValueError:
                    return "Number expected after {} space. Recieved: {}".format(x, msgs[x])
            elif msgs[x-1] == '-':
                try:
                    mod = mod - int(msgs[x])
                except ValueError:
                    return "Number expected after {} space. Recieved: {}".format(x, msgs[x])
            x += 1
        result = roll + mod #add the positive or negative number of modifiers to the roll
    except IndexError: #just print the rolls and the total of the rolls, no modifier found
        print("{} = {}".format(rolls, roll))
        return "{} = {}".format(rolls, roll)
    x = 2 #reset the counter again to start at the position in list msgs to add the modifiers for replying purposes
    reply = str(rolls) #take the string form of the list rolls
    string = ""
    while x <= len(msgs): #loop through msgs to add + # or - # for replying purposes
        if msgs[x-1] == '+':
            reply = reply + ' + ' + msgs[x]
        elif msgs[x-1] == '-':
            reply = reply + ' - ' + msgs[x]
        else:
            try:
                string += f" **{msgs[x-1]} {msgs[x]}**"
            except IndexError:
                string += f" **{msgs[x-1]}**"
        x += 2
    print("{} = {} <--- {}".format(reply, result, string))
    return("{} = {} <--- {}".format(reply, result, string))

def roll(msg):
    print("Input: ", msg)
    #Initilize workspace variables
    args = re.split(r"\+|\-", msg)
    modifiers = re.findall(r"\+|\-", msg)
    arg_results = process_arguments(args)
    output_rolls = arg_results[0]
    roll_results = arg_results[1]
    custom_text = arg_results[2]
    return_text = ''
    """
    print(output_rolls)
    print(roll_results)
    print(custom_text)
    print(modifiers)
    """
    for r in range(len(roll_results)):
        if r == 0:
            return_text += "> "
        return_text += "("
        if len(output_rolls[r]) > 1:
            for o in range(len(output_rolls[r])):
                if o == 0:
                    return_text += "*["
                return_text += str(output_rolls[r][o])
                if o != len(output_rolls[r])-1:
                    return_text += "+"
                if o == len(output_rolls[r])-1:
                    return_text += "]*"
            return_text += f" = **{roll_results[r]}**)"
        else:
            return_text += f"**{output_rolls[r][0]}**)"
        try:
            return_text += f" {modifiers[r]} "
        except:
            total = total_roll_results(roll_results, modifiers)
            return_text += f" = **__{total}__**"
    for text in custom_text:
        if re.match(r"[a-zA-Z ]", text):
            return_text += f"\n> {text}"
    print(return_text)
    return return_text
    
def total_roll_results(roll_results, modifiers):
    total = roll_results[0]
    for m in range(len(modifiers)):
        if modifiers[m] == '+':
            total += int(roll_results[m+1])
        elif modifiers[m] == '-':
            total -= int(roll_results[m+1])
    return str(total)

def process_arguments(args):
    output_rolls = []
    roll_results = []
    custom_text = []
    for a in args:
        isRoll = check_if_roll(a) #Check what type of argument has been passed
        print(isRoll)
        if isRoll[0] == 'roll': #Roll will go through the roll dice function and add the rolls and the result of the rolls added up.
            dice_roll = roll_the_dice(a)
            output_rolls.append(dice_roll[0])
            roll_results.append(dice_roll[1])
        elif isRoll[0] == 'int': #Int will just add the number to the rolls and the result lists.
            dice_roll = [int(a)]
            output_rolls.append(dice_roll)
            roll_results.append(int(a))
        elif isRoll[0] == 'text': #Text will just be added to the custom text
            custom_text.append(isRoll[1])
        elif isRoll[0] == 'rolltext': #Roll and text will be seperated by | and the roll will be rolled and added to lists as well as the custom text will be added
            roll_check_elements = isRoll[1].split('|')
            dice_roll = roll_the_dice(roll_check_elements[0])
            output_rolls.append(dice_roll[0])
            roll_results.append(dice_roll[1])
            custom_text.append(roll_check_elements[1])
        elif isRoll[0] == 'textroll': #Roll and text will be seperated by | and the roll will be rolled and added to lists as well as the custom text will be added
            roll_check_elements = isRoll[1].split('|')
            dice_roll = roll_the_dice(roll_check_elements[0])
            output_rolls.append(dice_roll[0])
            roll_results.append(dice_roll[1])
            custom_text.append(roll_check_elements[1])
        elif isRoll[0] == 'inttext': #Int and text wil be seperated by | and the int will be added to the lists and custom text will be added
            roll_check_elements = isRoll[1].split('|')
            dice_roll = [int(roll_check_elements[0])]
            output_rolls.append(dice_roll)
            roll_results.append(int(roll_check_elements[0]))
            custom_text.append(roll_check_elements[1])
        else:
            custom_text.append(isRoll[1])
    
    results = []
    results.append(output_rolls)
    results.append(roll_results)
    results.append(custom_text)
    return results

def check_if_roll(arg):
    roll_pattern = r"\s+\d+d\d+|\d+d\d+\s+|\d+d\d+"
    rolltext_pattern = r"^\d+d\d+[a-zA-Z~!@#$%^&*()_=\[\]|:;\"',<.>/?`\\\d ]+"
    textroll_pattern = r"^[a-zA-Z~!@#$%^&*()_=\[\]|:;\"',<.>/?`\\\d ]+\d+d\d+"
    text_pattern = r"[a-zA-Z]+"
    int_pattern = r"\s\d+|\d+"
    result = ''
    element = ''
    if re.match(r"^\d+d\d+$", arg):
        result = "roll"
        element = arg
    elif re.match(rolltext_pattern, arg):
        result = "rolltext"
        roll = re.search(roll_pattern, arg)
        element = roll.group(0).replace(' ', '') + "|"
        arg = re.sub(roll_pattern, '', arg, 1)
        arg = arg.strip()
        element += arg
    elif re.match(textroll_pattern, arg):
        result = "textroll"
        roll = re.search(roll_pattern, arg)
        element = roll.group(0).replace(' ', '') + "|"
        arg = re.sub(roll_pattern, '', arg, 1)
        arg = arg.strip()
        element += arg
    elif re.match(text_pattern, arg):
        result = "text"
        arg = arg.replace(' ', '')
        element = arg
    elif re.match(int_pattern, arg):
        number = re.search(int_pattern, arg)
        if re.search(text_pattern, arg):
            result = "inttext"
            element = number.group(0) + "|"
            arg = re.sub(int_pattern, '', arg, 1)
            arg = arg.replace(' ', '', 1)
            element += arg
        else:
            result = "int"
            element = arg
    else:
        arg = arg.replace(' ', '', 1)
        element = arg
    return [result, element]

def roll_the_dice(arg):
    arg = arg.split('d')
    roll_amount = int(arg[0])
    sides = int(arg[1])
    rolls = []
    for a in range(roll_amount):
        rolls.append(random.randrange(1, sides+1))
        roll = 0
        for r in rolls:
            roll += r
    return [rolls, roll]
       
#while True:
#    print(check_if_roll(input(":")))
#    roll(input(":"))