import csv
import datetime
import sys
from os.path import expanduser

home = expanduser("~")
dates = {}
commands = sys.argv[1:]

if len(commands) < 1 or commands[0] == "":
    for i in range(100, -1, -1):
        try:
            if i == 0:
                base_name = "yourLog.csv"
            else:
                base_name = "yourLog-" + str(i) + ".csv"
            food_log_loc = home + "/Downloads/" + base_name
            open(food_log_loc, "r")
            break
        except Exception:
            try:
                food_log_loc = base_name
                open(food_log_loc, "r")
                break
            except Exception:
                if i == 0:
                    print(
                        "yourLog.csv file not found in Downloads or current directory.")
                    exit(1)
                else:
                    pass
else:
    food_log_loc = commands[0]

max_ordinal = 0
min_ordinal = 999999999

print("Using food log: " + food_log_loc)

with open(food_log_loc, "r") as f:
    reader = csv.reader(f, delimiter=',', quotechar='"')
    for row in reader:
        try:
            date = datetime.datetime.fromisoformat(row[0])
        except Exception:
            continue
        date_day = datetime.date(date.year, date.month, date.day)
        if date_day in dates:
            day_meals = dates[date_day]
        else:
            day_meals = []
            if min_ordinal > date.toordinal():
                min_ordinal = date.toordinal()
            if max_ordinal < date.toordinal():
                max_ordinal = date.toordinal()
        meal = row[2]
        if meal not in day_meals:
            day_meals.append(meal)
        dates[date_day] = day_meals

for date_ordinal in range(min_ordinal + 1, max_ordinal - 1):
    test_date = datetime.date.fromordinal(date_ordinal)
    if test_date not in dates:
        dates[test_date] = []

for day in sorted(dates):
    n_meals = len(dates[day])
    if n_meals == 0:
        print(day.strftime("%Y-%m-%d") + " has no meals recorded!")
    elif n_meals < 4:
        meals = dates[day]
        meals.reverse()
        if "Breakfast" in meals and "Lunch" in meals and "Dinner" in meals:
            # print(day.strftime("%Y-%m-%d") + " is missing Snack")
            continue
        else:
            print(day.strftime("%Y-%m-%d") + " has only "
                  + str(n_meals) + " meals recorded: " + str(meals))
