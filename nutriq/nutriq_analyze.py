import csv
import datetime
import sys
from os.path import expanduser
import matplotlib.pyplot as plt


def _get_size_count(size_str: str):
    size_str = size_str.lower()
    if size_str == "tiny":
        return 1
    elif size_str == "small":
        return 3
    elif size_str == "regular" or size_str == "medium":
        return 6
    elif size_str == "large":
        return 10
    elif size_str == "huge":
        return 12
    else:
        return 0


home = expanduser("~")
commands = sys.argv[1:]
research_data_loc = commands[0]
analysis_output = "my_food_data.csv"

if len(commands) < 2 or commands[1] == "":
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
    food_log_loc = commands[2]

diets = []
foods = {}

print("Using research log: " + research_data_loc)
print("Using food log: " + food_log_loc)

with open(research_data_loc, "r") as f:
    reader = csv.reader(f, delimiter=',', quotechar='"')
    for row in reader:
        if len(diets) == 0:
            diets = list(row)
            continue

        key = row[0] + "::" + row[1]
        foods[key] = {"name": row[0], "prep": row[1], "category": row[2],
                      "ok": [], "warning": [], "danger": [], "count": 0, "unknown": False}
        for i in range(3, len(row)):
            if row[i] == "2":
                foods[key]["danger"].append(diets[i])
            elif row[i] == "1":
                foods[key]["warning"].append(diets[i])
            else:
                foods[key]["ok"].append(diets[i])


# TODO food categories

with open(analysis_output, "w", encoding="utf-8") as csvfile:
    filewriter = csv.writer(csvfile, delimiter=",",
                            quotechar="\"", quoting=csv.QUOTE_MINIMAL)
    header = ["logDateTime", "logType", "mealType", "foodName", "foodPrep",
              "foodServingSize", "categories", "okDiets", "warningDiets",
              "dangerDiets"]
    filewriter.writerow(header)
    with open(food_log_loc, "r") as f:
        reader = csv.reader(f, delimiter=',', quotechar='"')
        has_seen_header = False
        for row in reader:
            if not has_seen_header:
                has_seen_header = True
                continue
            key = row[3] + "::" + row[4]
            size = _get_size_count(row[5])
            if key in foods:
                ok = ";".join(foods[key]["ok"])
                warning = ";".join(foods[key]["warning"])
                danger = ";".join(foods[key]["danger"])
                foods[key]["count"] += size
            else:
                ok = ""
                warning = ""
                danger = ""
                foods[key] = {"name": row[3], "prep": row[4], "category": None,
                              "ok": [], "warning": [], "danger": [],
                              "count": size, "unknown": True}
            row_to_write = row[:6]
            row_to_write.extend(["", ok, warning, danger])
            filewriter.writerow(row_to_write)


print("Saved file: " + analysis_output)

food_to_plot = {}

for food in sorted(foods.values(), key=lambda f: f["count"]):
    if food["count"] > 0:
        if food["name"] in food_to_plot:
            food_to_plot[food["name"]] += food["count"]
        else:
            food_to_plot[food["name"]] = food["count"]

food_labels = [food[:30] for food in sorted(
    food_to_plot.keys(), key=lambda f: food_to_plot[f])]
food_counts = [count for count in sorted(food_to_plot.values())]

fig, ax = plt.subplots(1)
ax.barh(food_labels[-50:], food_counts[-50:])
ax.set_xscale('log')
plt.tight_layout()
plt.margins(x=0.02, y=0.02)
fig.set_size_inches(6, 10)
plt.show()

print("Food labels not shown on graph:\n")
print(food_labels[:-50])
