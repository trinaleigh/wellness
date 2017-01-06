import matplotlib.pyplot as plt

daysOfWeek = ['Sunday', 'Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday']

# # short list for testing
# behaviors = ['calorie']

# full list
behaviors = ['calorie', 'workout', 'meditation']

testUser = 'kls'

from pymongo import MongoClient
client = MongoClient()

db = client.wellnessdb
coll = db.weeks

class week(object):
    """
    represents a single week and associated targets
    """

    def __init__(self, weekNumber, year, category, currentUser):
        self.name = 'Week ' + str(weekNumber) + ' ' + str(year)
        self.weekNumber = weekNumber
        self.year = year
        self.category = category
        self.user = currentUser
        # create empty placeholders for the behaviors we want to track:
        self.journal = {}
        for i in behaviors:
            self.journal[i] = [0]*7

    def updateWeek(self, behavior, userVals):
        """
        enters behavior values for the week
        """
        if len(userVals) != 7:
            raise ValueError('Weekly behavior input should include 7 values')
        self.journal[behavior] = userVals

    def updateSingle(self, behavior, dayOfWeek, singleVal):
        """
        updates a single day's value
        """
        self.journal[behavior][dayOfWeek] = singleVal

    def __str__(self):
        return self.name


def planWeek(behavior):
    """
    given a single behavior, prompts the user to enter goals for the week
    returns a list of goals
    """
    i = 0
    goals = []
    while i < 7:
        day = daysOfWeek[i]
        while True:
            target = input('Please enter %s goal for %s' % (behavior, day))
            try:
                target = int(target)
                break
            except ValueError:
                print('Please enter a number')
        goals.append(target)
        i += 1
    return goals


def planWeekAll():
    """
    calls planWeek for all behaviors
    returns a list of tuples representing all behaviors and target values
    """
    goalList = []
    for behavior in behaviors:
        goalList.append((behavior, planWeek(behavior)))
    return goalList


def journal(behavior, dayNum):
    """
    prompts the user for journal entry
    returns a value for the given behavior and day
    """
    day = daysOfWeek[dayNum]
    while True:
        actualValue = input('Please enter %s value for %s' % (behavior, day))
        try:
            actualValue = int(actualValue)
            break
        except ValueError:
            print('Please enter a number')
    return actualValue


def journalAll(dayNum):
    """
    calls journal for all behaviors
    returns a list of tuples representing all behaviors and journal entries for one day
    """
    actualList = []
    for behavior in behaviors:
        actualList.append((behavior, journal(behavior,dayNum)))
    return actualList


def plotWeek(goals,actual={}):
    """
    takes target week and actual week
    plots all behaviors
    """
    x = range(1, 8)
    plotNum = 1
    for i in behaviors:
        plt.figure(plotNum)
        plt.plot(x, goals[i], '-', color='#3FAEB2', label='Target',linewidth=4.0)
        plt.title('progress for goal: ' + i)
        plt.xlabel('days of week')
        plt.xticks(x, daysOfWeek)
        plt.xlim(0,8)
        plt.ylabel(i + ' count')
        if actual != {}:
            plt.bar(x, actual[i], width=0.2, align='center', label='Actual', color = '#DE1A64')
            plt.ylim(0, max((max(goals[i]), max(actual[i])))*1.2)
        else:
            plt.ylim(0, max(goals[i]) * 1.2)
        plt.legend()
        plt.show()
        plotNum += 1


def enterData(weekNum,userData,addLog,changeLog):
    """
    enables user input for planning or journal mode
    returns updated userData dictionary
    """
    newData = userData
    newAdds = addLog
    newChanges = changeLog

    while True:
        mode2 = input('Enter "p" to plan your week or "r" to record a journal entry.')

        if mode2 in ['p', 'r']:
            if mode2 == 'p':
                # generate new week (if necessary) and log changes for db updates later
                if (weekNum, 'goal') not in newData.keys():
                    newData[(weekNum, 'goal')] = week(weekNum, '2017', 'goal', testUser)
                    newAdds.append((weekNum, 'goal'))
                elif (weekNum, 'goal') not in newChanges and (weekNum, 'goal') not in newAdds:
                    newChanges.append((weekNum, 'goal'))

                # prompt user and apply updates to the week
                updates = planWeekAll()
                for i in updates:
                    newData[(weekNum, 'goal')].updateWeek(i[0], i[1])

            else:
                while True:
                    # generate new week (if necessary) and log changes for db updates later
                    if (weekNum, 'actual') not in newData.keys():
                        newData[(weekNum, 'actual')] = week(weekNum, '2017', 'actual', testUser)
                        newAdds.append((weekNum, 'actual'))
                    elif (weekNum, 'actual') not in newChanges and (weekNum, 'goal') not in newAdds:
                        newChanges.append((weekNum, 'actual'))

                    # prompt user and apply updates to the week
                    currentDay = input('Enter the day (Sunday-Saturday)')
                    if currentDay in daysOfWeek:
                        dayNum = daysOfWeek.index(currentDay)
                        break
                    else:
                        print('Please try again.')
                updates = journalAll(dayNum)
                for i in updates:
                    newData[(weekNum, 'actual')].updateSingle(i[0], dayNum, i[1])


            return newData, newAdds, newChanges
        else:
            print('Please try again.')


def loaddb():

    previousUserData= coll.find({"user": testUser})

    userData = {}

    for document in previousUserData:
        loadWeek = week(document["week"], document["year"], document["category"], document["user"])
        loadWeek.journal = document["journal"]
        userData[(document["week"],document["category"])] = loadWeek

    return userData


def writeData(addLog,changeLog,userData):

    updateTotal = []

    for i in addLog:
        thisRecord = {}
        thisRecord['week'] = userData[i].weekNumber
        thisRecord['year'] = userData[i].year
        thisRecord['category'] = userData[i].category
        thisRecord['user'] = userData[i].user
        thisRecord['journal'] = userData[i].journal
        # insert new records to mongodb
        result = coll.insert_one(thisRecord)
        updateTotal.append(result)

    for i in changeLog:
        # need to update instead of insert
        result = coll.update_one({"user": testUser, "week": userData[i].weekNumber, "year": userData[i].year,
                                  "category": userData[i].category}, {"$set": {"journal": userData[i].journal}})
        updateTotal.append(result)

    return updateTotal

def initialize():
    """
    runs the user interface
    """
    userData = loaddb()
    addLog = []
    changeLog = []

    print('Welcome to the wellness app.')
    while True:
        mode0 = input('Enter "s" select a week or "q" to quit.')
        if mode0 in ['s', 'q']:
            if mode0 == 's':
                while True:
                    weekNum = input('Enter the week number (1-52)')
                    try:
                        weekNum = int(weekNum)
                        if weekNum in range(1, 53):
                            break
                        else:
                            print('Please try again.')
                    except ValueError:
                        print('Please try again.')
                while True:
                    mode1 = input('Enter "w" to write to your journal, "v" to view progress, or "b" to go back.')
                    if mode1 in ['w', 'v', 'b']:
                        if mode1 == 'w':
                            userData, addLog, changeLog = enterData(weekNum, userData, addLog, changeLog)
                        elif mode1 == 'v':
                            try:
                                plotWeek(userData[(weekNum, 'goal')].journal, (userData[(weekNum, 'actual')].journal if
                                                                               (weekNum, 'actual') in userData.keys() else {}))
                            except KeyError:
                                print('You have not logged any data yet. Please try writing to the journal first.')
                        else:
                            break
                    else:
                        print('Please try again.')
            else:
                print("Updates: ")
                print(writeData(addLog, changeLog, userData))
                print('Bye!')
                break
        else:
            print('Please try again.')



# # TESTS
#
# # building / updating a week
# testWeek = week(1,2017,'goal','kls')
# print(testWeek)
# testWeek.updateWeek('calorie', [1000,1000,1000,1000,2000,2000,1000])
# print(testWeek.journal)
# testWeek.updateSingle('calorie',5,3000)
# print(testWeek.journal)
#
# # entering goals
# planWeek("workout")
# planWeek("calorie")
#
# # plotting - goals only and goals / actuals
# testWeek1 = week(1,2017,'goal','kls')
# testWeek1.updateWeek('calorie', [1000,1000,1000,1000,2000,2000,1000])
# testWeek1.updateWeek('workout', [1,1,1,1,1,1,1])
# testWeek1.updateWeek('meditation', [0,0,0,1,0,0,1])
#
#
# testWeek2 = week(1,2017,'actual','kls')
# testWeek2.updateWeek('calorie', [2000,2000,1000,1000,2000,1200,1200])
#
# # plotWeek(testWeek1.journal)
#
# plotWeek(testWeek1.journal,testWeek2.journal)
#
# # journal entry
# journal('calorie',3)
# # loading data
# print(userData)
# print(userData[1].journal)
#
# # loading data (fcn)
# print(loaddb())
#
# # logging change
# testWeek = week(1,2017,'goal','kls')
# testUserData={(1,'goal'): testWeek}
# testChangeLog = [(1,'goal')]
# writeData(testChangeLog,testUserData)
#
# # db access
# cursor = coll.find({"user": "kls"})
# for document in cursor:
#     print(document)
#     print(document['year'])

# initialization
initialize()
