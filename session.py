from datetime import datetime, timedelta
import pytz

def sessionInputIntegrityCheck(msg):
    components = msg.split(' ')
    print(components)
    #Variable to pass
    #sessionID, h, m, AM/PM, TZ, month, day
    args = []
    #Session Name
    try:
        args.append(components[0])
    except IndexError:
        print("Error: Syntax incorrect. Expected: <sessionID> <hour:minutes> <AM/PM> <Timezone> <Month/Day>")
        return "Error: Syntax incorrect. Expected: <sessionID> <hour:minutes> <AM/PM> <Timezone> <Month/Day>"    
    #Check time
    try:
        if components[1].find(':') >= 0:
            time = components[1].split(':')
            args.append(time[0])
            args.append(time[1])
        else:
            try:
                int(components[1])
                components[1] = components[1] + ":00"
                time = components[1].split(':')
                args.append(time[0])
                args.append(time[1])
            except ValueError:
                print("Error: Where time is expected, a number was not found.")
                return "Error: Where time is expected, a number was not found."
    except IndexError:
        print("Error: Syntax incorrect. Expected: <sessionID> <hour:minutes> <AM/PM> <Timezone> <Month/Day>")
        return "Error: Syntax incorrect. Expected: <sessionID> <hour:minutes> <AM/PM> <Timezone> <Month/Day>"        
    #Check AM/PM
    try:
        if components[2].find('AM') >= 0 or components[2].find('am') >= 0 or components[2].find('Am') >= 0:
            args.append('AM')
            print("Morning.")
        elif components[2].find('PM') >= 0 or components[2].find('pm') >= 0 or components[2].find('Pm') >= 0:
            args.append('PM')
            print("Evening.")
        else:
            print("Error: Received: ", components[2], " Expected: AM or PM. Using PM by default")
            args.append('PM')
    except IndexError:
        print("Error: Syntax incorrect. Expected: <sessionID> <hour:minutes> <AM/PM> <Timezone> <Month/Day>")
        return "Error: Syntax incorrect. Expected: <sessionID> <hour:minutes> <AM/PM> <Timezone> <Month/Day>"  
    #Check timezone
    try:
        if components[3].find('CT') >= 0 or components[3].find('ct') >= 0:
            args.append('CT')
            print("Central Daylight Time")
        elif components[3].find('CST') >= 0 or components[3].find('cst') >= 0:
            args.append('CST')
            print("Central Standard Time")
        elif components[3].find('PT') >= 0 or components[3].find('pt') >= 0:
            args.append('PT')
            print("Pacific Daylight Time")
        elif components[3].find('PST') >= 0 or components[3].find('pst') >= 0:
            args.append('PST')
            print("Pacific Standard Time")
        elif components[3].find('MST') >= 0 or components[3].find('mst') >= 0:
            args.append('MST')
            print("Mountain Standard Time")
        elif components[3].find('EST') >= 0 or components[3].find('est') >= 0 or components[3].find('ET') >= 0 or components[3].find('et') >= 0:
            args.append('EST')
            print("Eastern Standard Time")
        elif components[3].find('MDT') >= 0 or components[3].find('mdt') >= 0 or components[3].find('MT') >= 0 or components[3].find('mt') >= 0:
            args.append('MDT')
            print("Mountain Time")
        else:
            args.append(components[3])
            print("What time zone is this?: ", components[3])
    except IndexError:
        print("Error: Syntax incorrect. Expected: <sessionID> <hour:minutes> <AM/PM> <Timezone> <Month/Day>")
        return "Error: Syntax incorrect. Expected: <sessionID> <hour:minutes> <AM/PM> <Timezone> <Month/Day>" 
    #Check month/day
    try:
        if components[4].find('/') >= 0:
            date = components[4].split('/')
            args.append(date[0])
            args.append(date[1])
    except IndexError:
        print("/ not used for date. Maybe a - instead?")
        try:
            if components[4].find('-') >= 0:
                date = components[4].split('-')
                args.append(date[0])
                args.append(date[1])
        except IndexError:
            print("- not used either, perhaps they used a space?")
            try:
                args.append(components[4])
                args.append(components[5])
            except IndexError:
                try:
                    if components[3].find('/') >= 0:
                        date = components[3].split('/')
                        if int(date[0]) >= 12:
                            args.append(date[0])
                        else:
                            return "Error: Month is higher than 12."
                        if int(data[1]) <= 31:
                            args.append(date[1])
                        else:
                            return "Error: Day is higher than 31."
                except IndexError:
                    print("Error: Date value doesn't seem to be where expected.")
                    return "Error: Date value doesn't seem to be where expected."
    print(args)
    verified = args[0]+' '+args[1]+':'+args[2]+' '+args[3]+' '+args[4]+' '+args[5]+'/'+args[6]
    print(verified)
    return verified

def sessionLogInput(msg):
    components = msg.split(' ')
    try:
        file = open("nethys_sessionlist.dat", 'r+')
    except FileNotFoundError:
        file = open("nethys_sessionlist.dat", 'w')
        file.close
        file = open("nethys_sessionlist.dat", 'r+')
    file.read()
    eof = file.tell()
    file.seek(0)
    x = 1
    while x == 1:
        pos = file.tell()
        line = file.readline()
        if line.find(str(components[0] + ',')) >= 0:
            file.seek(pos)
            file.readline()
            recreate = file.read()
            file.seek(pos)
            file.write(recreate)
            x = 0
        elif eof == pos:
            x = 0
    file.write('[')
    c = 0
    while c < len(components):
        file.write(components[c])
        if c != len(components) - 1:
            file.write(',')
        c += 1
    file.write(']\n')
    file.close()

def sessionRemove(msg):
    try:
        file = open("nethys_sessionlist.dat", 'r+')
    except FileNotFoundError:
        return "No session files found. use !session to add a session."
    file.read()
    eof = file.tell()
    file.seek(0)
    while True:
        pos = file.tell()
        line = file.readline()
        if line.find(str(msg + ',')) >= 0:
            recreate = file.read()
            print(recreate)
            file.seek(pos)
            file.truncate(pos)
            file.write(recreate)
            file.seek(pos)
            break
        elif eof == pos:
            return str(msg + " not found in my Archives to remove. Don't waste my time, mortal.")
            break
    file.close()
    return str(msg + " was removed successfully.")
  
def sessionListCleanup():
    now = pytz.utc.localize(datetime.utcnow())
    utc = pytz.utc
    eastern = pytz.timezone('US/Eastern')
    pacific = pytz.timezone('US/Pacific')
    central = pytz.timezone('US/Central')
    mountain = pytz.timezone('US/Central')
    print(now)
    file = open("nethys_sessionlist.dat", 'r+')
    file.read()
    eof = file.tell()
    file.seek(0)
    while True:
        pos = file.tell()
        line = file.readline()
        line = line.replace('[', '')
        line = line.replace(']', '')
        line = line.replace('\n', '')
        print('line: ',line)
        contents = line.split(',')
        print('contents: ',contents)
        try:
            time = contents[1].split(':')
            hour = int(time[0])
            minutes = int(time[1])
            date = contents[4].split('/')
            month = int(date[0])
            day = int(date[1])
        except IndexError:
            file.close()
            return "All old sessions have been cleared from my Archives."
        if line.find('AM') >= 0:
            hour = int(hour)
        elif line.find('PM') >= 0:
            if int(hour) == 12:
                hour = 12
            else:
                hour = int(hour) + 12
        print('hour: ', hour)
        print('min: ', minutes)
        print(contents[3])
        if contents[3] == 'CST' or contents[3] == 'CT' or contents[3] == 'CDT':
            time = central.localize(datetime(now.year, month, day, hour, minutes, 0, 0))
        elif contents[3] == 'PST' or contents[3] == 'PT' or contents[3] == 'PDT':
            time = pacific.localize(datetime(now.year, month, day, hour, minutes, 0, 0))
        elif contents[3] == 'MST' or contents[3] == 'MT' or contents[3] == 'MDT':
            time = mountain.localize(datetime(now.year, month, day, hour, minutes, 0, 0))
        elif contents[3] == 'EST' or contents[3] == 'ET' or contents[3] == 'EDT':
            time = eastern.localize(datetime(now.year, month, day, hour, minutes, 0, 0))
        else:
            time = None
        print(time)
        if time < now:
            print('DO WORK')
            recreate = file.read()
            print(recreate)
            file.seek(pos)
            file.truncate(pos)
            file.write(recreate)
            file.seek(pos)
        elif eof == pos:
            file.close()
            return "All old sessions have been cleared from my Archives."

def sessionReadData(msg):
    try:
        file = open("nethys_sessionlist.dat", 'r+')
    except FileNotFoundError:
        file = open("nethy_sessionlist.dat", 'w')
        file.close
        file = open("nethys_sessionlist.dat", 'r+')
    file.read()
    eof = file.tell()
    file.seek(0)
    x = 1
    while x == 1:
        pos = file.tell()
        line = file.readline()
        if line.find(msg) >= 0:
            print(line)
            file.close()
            return line
        elif eof == pos:
            file.close()
            return "No session by the name exists."

def sessionQuery(msg):
    #sessionID 0, time 1, AM/PM 2, TZ 3, month/day 4
    data = sessionReadData(msg)
    data = data.replace('[', '')
    data = data.replace(']', ' ')
    data = data.split(",")
    print(data)
    try:
        data[4] = data[4].replace('\n', '')
        reply = ':small_blue_diamond: **'+data[0]+'** '+"is scheduled for "+data[4]+'@ '+data[1]+' '+data[2]+' '+data[3]
        print(reply)
        return reply
    except IndexError:
        return str(msg + " doesn't exist in my records.")

def sessionQueryAll():
    sessions = []
    try:
        for line in open("nethys_sessionlist.dat", 'r'):
            sessionID = line.split(',')
            msg = sessionID[0].replace('[', '')
            sessions.append(sessionQuery(msg))
        prettify = ''
        for s in sessions:
            edited = s.replace("orange", "blue")
            prettify = prettify + edited + '\n'
        if len(prettify) == 0:
            return "No session found in the list."
        else:
            return prettify
    except FileNotFoundError:
        return "No session list was found. Use !session to create a session"

def session(msg):
    integrityCheck = sessionInputIntegrityCheck(msg)
    if integrityCheck.find("Error: ") >= 0:
        return integrityCheck
    else:
        sessionLogInput(integrityCheck)
        msg = msg.split(' ')
        return sessionQuery(msg[0])

def sessionVote(msg):
    msg = split(' ')
    sessionID = msg[0]
    
    return ":scroll:"