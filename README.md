# wellness

wellness.py is a journal for tracking and visualizing daily behaviors related to fitness/wellness.

## summary

by default, the program will track calorie, workout, and meditation values. these selections can be modified in wellness.py by adjusting the "behaviors" list.

for each week, the user can:
* set target values for each behavior
* log actual values achieved for each behavior
* visualize progress (target vs. actual) on plots

wellness.py prompts the user for input via terminal / shell.

the program includes backend support for multiple user profiles, but "currentUser" is currently hard-coded to a single value.

## dependencies

wellness.py uses MongoDB to store data between sessions.

the following packages are required:
* matplotlib
* pymongo