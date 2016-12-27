import pylab

class week(object):
    """
    represents a single week and associated targets
    """

    def __init__(self, name, weekNumber, year):
        self.name =  "Week " + str(weekNumber) + " " + str(year)
        self.weekNumber = weekNumber
        self.year = year
        # create empty placeholders for the behaviors we want to track:
        self.calories = [0]*7
        self.workouts = [0]*7
        self.meditation = [0]*7

    def updateBehavior(self, userVals, listCategory):
        """
        enters behavior values for the week
        """
        if len(userVals) != 7:
            raise ValueError('Weekly behavior input should include 7 values')

        if listCategory == "calories":
            self.calories = userVals
        elif listCategory == "workouts":
            self.workouts = userVals
        else:
            self.meditation = userVals

    def updateSingle(self, singleVal, listCategory, dayOfWeek):
        """
        updates a single day's value
        """

        if listCategory == "calories":
            self.calories[dayOfWeek] = singleVal
        elif listCategory == "workouts":
            self.workouts[dayOfWeek] = singleVal
        else:
            self.meditation[dayOfWeek] = singleVal

    def __str__(self):
        return self.name


# # TESTS
# #
# # test building / updating a week
# testWeek = week("test",1,2017)
# print testWeek
# testWeek.updateBehavior([1000,1000,1000,1000,2000,2000,1000],"calories")
# print testWeek.calories
# testWeek.updateSingle(3000,"calories",5)
# print testWeek.calories
