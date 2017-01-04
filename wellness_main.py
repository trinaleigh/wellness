import matplotlib.pyplot as plt

daysOfWeek = ['Sunday', 'Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday']

# short list for testing
behaviors = ['calorie']

# # full list
# behaviors = ['calorie', 'workout', 'meditation']

userGoals = {}
userActuals = {}

class week(object):
    """
    represents a single week and associated targets
    """

    def __init__(self, weekNumber, year):
        self.name = 'Week ' + str(weekNumber) + ' ' + str(year)
        self.weekNumber = weekNumber
        self.year = year
        # create empty placeholders for the behaviors we want to track:
        self.diary = {}
        for i in behaviors:
            self.diary[i] = [0]*7

    def updateWeek(self, behavior, userVals):
        """
        enters behavior values for the week
        """
        if len(userVals) != 7:
            raise ValueError('Weekly behavior input should include 7 values')
        self.diary[behavior] = userVals

    def updateSingle(self, behavior, dayOfWeek, singleVal):
        """
        updates a single day's value
        """
        self.diary[behavior][dayOfWeek] = singleVal

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


def diary(behavior, dayNum):
    """
    prompts the user for diary entry
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


def diaryAll(dayNum):
    """
    calls diary for all behaviors
    returns a list of tuples representing all behaviors and diary entries for one day
    """
    actualList = []
    for behavior in behaviors:
        actualList.append((behavior, diary(behavior,dayNum)))
    return actualList


def plotWeek(goals,actual):
    """
    takes target week and actual week
    plots all behaviors
    """
    x = range(1, 8)
    plotNum = 1
    for i in behaviors:
        plt.figure(plotNum)
        plt.plot(x, goals[i], '-g', label = 'Target')
        plt.plot(x, actual[i], '-r', label = 'Logged')
        plt.ylim(0, max((max(goals[i]), max(actual[i])))*1.2)
        plt.legend()
        plt.show()
        plotNum += 1


def enterData(weekNum):
    """
    enables user input for planning or diary mode
    returns the target week and the actual week
    """
    if weekNum not in userGoals.keys():
        userGoals[weekNum] = week(weekNum, '2017')
    if weekNum not in userActuals.keys():
        userActuals[weekNum] = week(weekNum, '2017')
    while True:
        mode2 = input('Enter "p" to plan your week or "r" to record a diary entry.')
        if mode2 in ['p','r']:
            if mode2 == 'p':
                updates = planWeekAll()
                for i in updates:
                    userGoals[weekNum].updateWeek(i[0], i[1])
            else:
                while True:
                    currentDay = input('Enter the day (Sunday-Saturday)')
                    if currentDay in daysOfWeek:
                        dayNum = daysOfWeek.index(currentDay)
                        break
                    else:
                        print('Please try again.')
                updates = diaryAll(dayNum)
                for i in updates:
                    userActuals[weekNum].updateSingle(i[0], dayNum, i[1])
            return userGoals[weekNum], userActuals[weekNum]
        else:
            print('Please try again.')


def initialize():
    """
    runs the user interface
    """
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
                    mode1 = input('Enter "w" to write to your diary, "v" to view progress, or "b" to go back.')
                    if mode1 in ['w', 'v', 'b']:
                        if mode1 == 'w':
                            enterData(weekNum)
                        elif mode1 == 'v':
                            try:
                                plotWeek(userGoals[weekNum].diary, userActuals[weekNum].diary)
                            except KeyError:
                                print('You have not logged any data yet. Please try writing to the diary first.')
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
# testWeek = week(1,2017)
# print(testWeek)
# testWeek.updateWeek('calorie', [1000,1000,1000,1000,2000,2000,1000])
# print(testWeek.diary)
# testWeek.updateSingle('calorie',5,3000)
# print(testWeek.diary)
#
# # entering goals
# planWeek("workout")
# planWeek("calorie")
#
# # plot
# plotWeek(testWeek.diary,testWeek.diary)
#
# # diary entry
# diary('calorie',3)
#
# initialization
initialize()