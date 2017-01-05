import matplotlib.pyplot as plt

daysOfWeek = ['Sunday', 'Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday']

# short list for testing
behaviors = ['calorie']

# # full list
# behaviors = ['calorie', 'workout', 'meditation']

from pymongo import MongoClient
client = MongoClient()

db = client.wellnessdb
coll = db.weeks

userData = {}

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
        plt.plot(x, goals[i], '-g', label = 'Target')
        if actual != {}:
            plt.plot(x, actual[i], '-r', label = 'Logged')
            plt.ylim(0, max((max(goals[i]), max(actual[i])))*1.2)
        else:
            plt.ylim(0, max(goals[i])* 1.2)
        plt.legend()
        plt.show()
        plotNum += 1


def enterData(weekNum):
    """
    enables user input for planning or journal mode
    returns the target week and the actual week
    """
    if (weekNum, 'goal') not in userData.keys():
        userData[(weekNum, 'goal')] = week(weekNum, '2017','goal','kls')
    if (weekNum, 'actual') not in userData.keys():
        userData[(weekNum, 'actual')] = week(weekNum, '2017','actual','kls')
    while True:
        mode2 = input('Enter "p" to plan your week or "r" to record a journal entry.')
        if mode2 in ['p','r']:
            if mode2 == 'p':
                updates = planWeekAll()
                for i in updates:
                    userData[(weekNum, 'goal')].updateWeek(i[0], i[1])
            else:
                while True:
                    currentDay = input('Enter the day (Sunday-Saturday)')
                    if currentDay in daysOfWeek:
                        dayNum = daysOfWeek.index(currentDay)
                        break
                    else:
                        print('Please try again.')
                updates = journalAll(dayNum)
                for i in updates:
                    userData[(weekNum, 'actual')].updateSingle(i[0], dayNum, i[1])
            return userData[(weekNum, 'goal')], userData[(weekNum, 'actual')]
        else:
            print('Please try again.')

def loaddb():

    previousUserData= coll.find({"user": "kls"})

    for document in previousUserData:
        loadWeek = week(document["week"], document["year"], document["category"], document["user"])
        loadWeek.journal = document["journal"]
        userData[(document["week"],document["category"])] = loadWeek

    return userData
def initialize():
    """
    runs the user interface
    """
    userData = loaddb()
    print('Welcome to the wellness app.')
    while True:
        mode0 = input('Enter "s" select a week or "q" to quit.')
        if mode0 in ['s','q']:
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
                            enterData(weekNum)
                        elif mode1 == 'v':
                            try:
                                plotWeek(userData[(weekNum,'goal')].journal, (userData[(weekNum,'actual')].journal if (weekNum,'actual') in userData.keys() else {}))
                            except KeyError:
                                print('You have not logged any data yet. Please try writing to the journal first.')
                        else:
                            break
                    else:
                        print('Please try again.')
            else:
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
# # plot
# plotWeek(testWeek.journal,testWeek.journal)
# plotWeek(testWeek.journal)
#
# # journal entry
# journal('calorie',3)
#
# # db access
# cursor = coll.find({"user": "kls"})
# for document in cursor:
#     print(document)
#     print(document['year'])
#
# # loading data
# print(userGoals)
# print(userGoals[1].journal)
#
# # loading data (fcn)
# print(loaddb())

# initialization
initialize()