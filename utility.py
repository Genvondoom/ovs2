from datetime import datetime, timedelta


def getFirstLetters(string):
    word = string.split()

    result = ""
    temp = []
    for x in word:
        if x != "and":

            temp.append(x[0])

    return result.join(temp).upper()





def createElection(data):
    name, sch_dept, startingDate, startingtime, duration = data
    # category = dept, faculty, school, busa
    # date format= dd/mm/yy
    # time format = hh/mm
    # duration format hour:min
    time = datetime.strptime(startingtime, "%I:%M%p")
    date = datetime.strptime(startingDate, "%d/%m/%Y").strftime("%d/%m/%Y")
    limit = timedelta(hours= int(duration))
    # wok on duraton hours and miniutes
    stopTime = time + limit
    stopTime = stopTime.strftime('%I:%M%p')
    status = "active"
    temp = [name, sch_dept, date, startingtime, duration, stopTime, status]
    date = datetime.now().strftime("%m%d%y")

    electionId = f"{getFirstLetters(sch_dept)}{date}"
    temp.insert(0, electionId)
    return temp

def listToStingConverter(given_list):
    temp = ""
    for x in given_list:
        temp += f"{x}"
        if x != given_list[-1]:
            temp += ","

    return temp

def generateToken(electionid, matricNO):
    a = f"{electionid[:3]}{matricNO[3:]}{electionid[5:]}"
    return a


