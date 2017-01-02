import pylab

daysOfWeek = ['Sunday', 'Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday']
behaviors = ['calorie', 'workout', 'meditation']

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
    prompts the user to enter goals for the week
    returns a list of goals
    """
    i = 0
    goals = []
    while i < 7:
        day = daysOfWeek[i]
        while True:
            target = raw_input('Please enter %s goal for %s' % (behavior, day))
            try:
                target = int(target)
                break
            except ValueError:
                print 'Please enter a number'
        goals.append(target)
        i += 1
    return goals


def planWeekAll():
    """
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
        actualValue = raw_input('Please enter %s value for %s' % (behavior, day))
        try:
            actualValue = int(actualValue)
            break
        except ValueError:
            print 'Please enter a number'
    return actualValue


def diaryAll(dayNum):
    """
    returns a list of tuples representing all behaviors and diary entries for one day
    """
    actualList = []
    for behavior in behaviors:
        actualList.append((behavior, diary(behavior,dayNum)))
    return actualList


def plotWeek(goals,actual):
    x = range(1,8)
    pylab.plot(x, goals, '-g', label = 'Target')
    pylab.plot(x, actual, '-r', label = 'Logged')
    pylab.ylim(0, max((max(goals), max(actual)))*1.2)
    pylab.legend()
    pylab.show()


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
        mode2 = raw_input('Enter "p" to plan your week or "r" to record a diary entry.')
        if mode2 in ['p','r']:
            if mode2 == 'p':
                updates = planWeekAll()
                for i in updates:
                    userGoals[weekNum].updateWeek(i[0], i[1])
            else:
                while True:
                    currentDay = raw_input('Enter the day (Sunday-Saturday)')
                    if currentDay in daysOfWeek:
                        dayNum = daysOfWeek.index(currentDay)
                        break
                    else:
                        print 'Please try again.'
                updates = diaryAll(dayNum)
                for i in updates:
                    userActuals[weekNum].updateSingle(i[0], dayNum, i[1])
            return (userActuals[weekNum], userGoals[weekNum])
        else:
            print 'Please try again.'


def initialize():
    """
    runs the user interface
    """
    print 'Welcome to the wellness app.'
    while True:
        weekNum = raw_input('Enter the week number (1-52)')
        try:
            weekNum = int(weekNum)
            if weekNum in range(1, 53):
                break
            else:
                print 'Please try again.'
        except ValueError:
            print 'Please try again.'
    while True:
        mode1 = raw_input('Enter "d" to access your diary, "v" to see progress, or "q" to quit.')
        if mode1 in ['d', 'v', 'q']:
            if mode1 == 'd':
                weeks = enterData(weekNum)
            elif mode1 == 'v':
                for i in behaviors:
                    try:
                        plotWeek(weeks[0].diary[i], weeks[1].diary[i])
                    except UnboundLocalError:
                        print 'You have not logged any data yet. Please try the diary.'
                        break
            else:
                print "Bye!"
                break
        else:
            print 'Please try again.'


# # TESTS
#
# # building / updating a week
# testWeek = week(1,2017)
# print testWeek
# testWeek.updateWeek('calorie', [1000,1000,1000,1000,2000,2000,1000])
# print testWeek.diary
# testWeek.updateSingle('calorie',5,3000)
# print testWeek.diary
#
# # entering goals
# planWeek("workout")
# planWeek("calorie")
#
# # plot
# goal1=[2000,1000,1000,1000,1000,1000,1200]
# actual1=[2000,2000,1500,800,1000,800,1200]
# plotWeek(goal1,actual1)
#
# # diary entry
# diary('calorie',3)

# initialization
initialize()