import pylab


class week(object):
    """
    represents a single week and associated targets
    """

    def __init__(self, weekNumber, year):
        self.name = "Week " + str(weekNumber) + " " + str(year)
        self.weekNumber = weekNumber
        self.year = year
        # create empty placeholders for the behaviors we want to track:
        self.calories = [0]*7
        self.workouts = [0]*7
        self.meditation = [0]*7

    def updateWeek(self, userVals, behavior):
        """
        enters behavior values for the week
        """
        if len(userVals) != 7:
            raise ValueError('Weekly behavior input should include 7 values')
        if behavior == "calorie":
            self.calories = userVals
        elif behavior == "workout":
            self.workouts = userVals
        else:
            self.meditation = userVals

    def updateSingle(self, singleVal, behavior, dayOfWeek):
        """
        updates a single day's value
        """
        if behavior == "calorie":
            self.calories[dayOfWeek] = singleVal
        elif behavior == "workout":
            self.workouts[dayOfWeek] = singleVal
        else:
            self.meditation[dayOfWeek] = singleVal

    def __str__(self):
        return self.name


def planWeek(behavior):
    """
    prompts the user to enter goals for the week
    """
    daysOfWeek = ["Sunday", "Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday"]
    i = 0
    goals = []
    while i < 7:
        day = daysOfWeek[i]
        while True:
            target = raw_input("Please enter %s goal for %s" % (behavior, day))
            try:
                target = int(target)
                break
            except ValueError:
                print 'Please enter a number'
        goals.append(target)
        i += 1
    return goals


def plotWeek(goals,actual):
    x=range(1,8)
    pylab.plot(x, goals, '-g', label = "Target")
    pylab.plot(x, actual, '-r', label = "Logged")
    pylab.ylim(0,max((max(goals),max(actual)))*1.2)
    pylab.legend()
    pylab.show()



# # TESTS
#
# # building / updating a week
# testWeek = week(1,2017)
# print testWeek
# testWeek.updateWeek([1000,1000,1000,1000,2000,2000,1000],"calorie")
# print testWeek.calories
# testWeek.updateSingle(3000,"calorie",5)
# print testWeek.calories
#
# # entering goals
# planWeek("workout")
# planWeek("calorie")
#
# # plot
# goal1=[2000,1000,1000,1000,1000,1000,1200]
# actual1=[2000,2000,1500,800,1000,800,1200]
# plotWeek(goal1,actual1)

