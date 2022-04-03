import datetime
import time
import tkinter as tk
from tkinter import messagebox
from tkinter.constants import W
import tkinter.font as fnt
from tkinter.ttk import Button, Entry, Frame, Label
import traceback
from nutriq_add_meals import get_driver, connect_to_base, log_meal
from meal_components import Breakfast, MainMeal, Snack

_input = None


def _update_list_get_text(_list: list, list_string: str, mod: str, mode: int) -> str:
    if mode == 0 and mod in _list:
        _list.remove(mod)
    elif mode == 1 and mod not in _list:
        _list.append(mod)
    if list_string == "":
        if mode == 1:
            list_string = mod
    elif mode == 0:
        if "\n" + mod in list_string:
            list_string = list_string.replace("\n" + mod, "")
        elif mod + "\n" in list_string:
            list_string = list_string.replace(mod + "\n", "")
        else:
            list_string = ""
    else:
        list_string += "\n" + mod

    return list_string


class EffectiveDate():
    def __init__(self):
        self.date = self.get_effective_date().toordinal()

    def get(self) -> datetime.datetime:
        return datetime.datetime.fromordinal(self.date)

    def to_string(self) -> str:
        return self.get().strftime("%B %d, %Y")

    def increment(self) -> None:
        self.date += 1

    def decrement(self) -> None:
        self.date -= 1

    def get_effective_date(self) -> datetime.datetime:
        if datetime.datetime.now().hour < 7:
            return datetime.date.today() - datetime.timedelta(days=1)
        else:
            return datetime.date.today()


class DateDownButton(Button):
    def __init__(self, effective_date, referenceLabel, **k):
        super().__init__(**k)
        self.effective_date = effective_date
        self.referenceLabel = referenceLabel

    def decrementDateAndUpdateLabelText(self) -> None:
        self.effective_date.decrement()
        self.referenceLabel['text'] = self.effective_date.to_string()


class DateUpButton(Button):
    def __init__(self, effective_date, referenceLabel, **k):
        super().__init__(**k)
        self.effective_date = effective_date
        self.referenceLabel = referenceLabel

    def incrementDateAndUpdateLabelText(self) -> None:
        self.effective_date.increment()
        self.referenceLabel['text'] = self.effective_date.to_string()


class MealField(tk.Checkbutton):
    def __init__(self, v, referenceLabel, referenceList, **k):
        super().__init__(**k)
        self.v = v
        self.referenceLabel = referenceLabel
        self.referenceList = referenceList

    def clear(self) -> None:
        self.v.set(0)
        self.updateLabelText()

    def clearAll(self) -> None:
        self.v.set(0)
        if len(self.referenceList) > 0:
            self.referenceList.clear()
        if str(self.referenceLabel['text']) != "":
            self.referenceLabel['text'] = ""

    def updateLabelText(self) -> None:
        self.referenceLabel['text'] = _update_list_get_text(
            self.referenceList,
            str(self.referenceLabel['text']),
            str(self['text']),
            self.v.get())


class App():
    def __init__(self, master):
        self.breakfast = []
        self.lunch = []
        self.dinner = []
        self.snack = []
        self.master = master
        frameBreakfast = Frame(self.master)
        frameBreakfast.columnconfigure(0, weight=1)
        frameBreakfast.grid(column=0, row=0)
        self.label1 = Label(frameBreakfast, text="Breakfast")
        self.label1.grid(pady=10)
        self.labelBreakfastComponents = Label(frameBreakfast, text="")

        self.buttonsBreakfast = {}
        for name, member in Breakfast.__members__.items():
            var = tk.IntVar()
            if member.is_default_food():
                var.set(1)
            self.buttonsBreakfast[member] = {"var": var}

        counter = 1
        for member in self.buttonsBreakfast:
            var = self.buttonsBreakfast[member]["var"]
            c = MealField(var,
                          self.labelBreakfastComponents, self.breakfast,
                          master=frameBreakfast, text=member.value, variable=var,
                          onvalue=1, offvalue=0, font=fnt.Font(size=6))
            c.configure(command=c.updateLabelText)
            c.grid(column=0, row=counter, sticky=W)
            self.buttonsBreakfast[member]["button"] = c
            if var.get() == 1:
                c.updateLabelText()
            counter += 1

        self.submitNewBreakfastFoodBox = Entry(frameBreakfast,
                                               text="Add other foods...",
                                               width=30,
                                               font=fnt.Font(size=8))
        self.submitNewBreakfastFoodBox.grid(column=0, row=counter, sticky=W)
        self.submitNewBreakfastFoodButton = Button(master=frameBreakfast,
                                                   text="Add food",
                                                   command=self.submitNewBreakfastFood)
        self.submitNewBreakfastFoodButton.grid(column=0, row=counter + 1)
        self.clearBreakfastButton = Button(master=frameBreakfast,
                                           text="Clear all",
                                           command=self.clearAllBreakfast)
        self.clearBreakfastButton.grid(column=0, row=counter + 2)
        self.clearNonchecksBreakfastButton = Button(master=frameBreakfast,
                                                    text="Clear nonchecks",
                                                    command=self.clearNonchecksBreakfast)
        self.clearNonchecksBreakfastButton.grid(column=0, row=counter + 3)
        self.labelBreakfastComponents.grid(column=0, row=counter + 4, pady=10)

        frameLunch = Frame(self.master)
        frameLunch.columnconfigure(0, weight=1)
        frameLunch.grid(column=1, row=0)
        self.label2 = Label(frameLunch, text="Lunch")
        self.label2.grid(pady=10)
        self.labelLunchComponents = Label(frameLunch, text="")

        self.buttonsLunch = {}
        for name, member in MainMeal.__members__.items():
            self.buttonsLunch[member] = {"var": tk.IntVar()}

        counter = 1
        for member in self.buttonsLunch:
            var = self.buttonsLunch[member]["var"]
            c = MealField(var,
                          self.labelLunchComponents, self.lunch,
                          master=frameLunch, text=member.value, variable=var,
                          onvalue=1, offvalue=0, font=fnt.Font(size=6))
            c.configure(command=c.updateLabelText)
            c.grid(column=0, row=counter, sticky=W)
            self.buttonsLunch[member]["button"] = c
            counter += 1

        self.submitNewLunchFoodBox = Entry(frameLunch,
                                           text="Add other foods...",
                                           width=30,
                                           font=fnt.Font(size=8))
        self.submitNewLunchFoodBox.grid(column=0, row=counter, sticky=W)
        self.submitNewLunchFoodButton = Button(master=frameLunch,
                                               text="Add food",
                                               command=self.submitNewLunchFood)
        self.submitNewLunchFoodButton.grid(column=0, row=counter + 1)
        self.clearLunchButton = Button(master=frameLunch,
                                       text="Clear all",
                                       command=self.clearAllLunch)
        self.clearLunchButton.grid(column=0, row=counter + 2)
        self.clearNonchecksLunchButton = Button(master=frameLunch,
                                                text="Clear nonchecks",
                                                command=self.clearNonchecksLunch)
        self.clearNonchecksLunchButton.grid(column=0, row=counter + 3)
        self.labelLunchComponents.grid(column=0, row=counter + 4, pady=10)

        frameDinner = Frame(self.master)
        frameDinner.columnconfigure(0, weight=1)
        frameDinner.grid(column=2, row=0)
        self.label3 = Label(frameDinner, text="Dinner")
        self.label3.grid(pady=10)
        self.labelDinnerComponents = Label(frameDinner, text="")

        self.buttonsDinner = {}
        for name, member in MainMeal.__members__.items():
            self.buttonsDinner[member] = {"var": tk.IntVar()}

        counter = 1
        for member in self.buttonsDinner:
            var = self.buttonsDinner[member]["var"]
            c = MealField(var,
                          self.labelDinnerComponents, self.dinner,
                          master=frameDinner, text=member.value, variable=var,
                          onvalue=1, offvalue=0, font=fnt.Font(size=6))
            c.configure(command=c.updateLabelText)
            c.grid(column=0, row=counter, sticky=W)
            self.buttonsDinner[member]["button"] = c
            counter += 1

        self.submitNewDinnerFoodBox = Entry(frameDinner,
                                            text="Add other foods...", width=30, font=fnt.Font(size=8))
        self.submitNewDinnerFoodBox.grid(column=0, row=counter, sticky=W)
        self.submitNewDinnerFoodButton = Button(master=frameDinner,
                                                text="Add food", command=self.submitNewDinnerFood)
        self.submitNewDinnerFoodButton.grid(column=0, row=counter + 1)
        self.clearDinnerButton = Button(master=frameDinner,
                                        text="Clear all", command=self.clearAllDinner)
        self.clearDinnerButton.grid(column=0, row=counter + 2)
        self.clearNonchecksDinnerButton = Button(master=frameDinner,
                                                 text="Clear nonchecks", command=self.clearNonchecksDinner)
        self.clearNonchecksDinnerButton.grid(column=0, row=counter + 3)
        self.labelDinnerComponents.grid(column=0, row=counter + 4, pady=10)

        frameSnack = Frame(self.master)
        frameSnack.columnconfigure(0, weight=1)
        frameSnack.grid(column=3, row=0)
        self.label3 = Label(frameSnack, text="Snack")
        self.label3.grid(pady=10)
        self.labelSnackComponents = Label(frameSnack, text="")

        self.buttonsSnack = {}
        for name, member in Snack.__members__.items():
            var = tk.IntVar()
            if member.is_default_food():
                var.set(1)
            self.buttonsSnack[member] = {"var": var}

        counter = 1
        for member in self.buttonsSnack:
            var = self.buttonsSnack[member]["var"]
            c = MealField(var,
                          self.labelSnackComponents, self.snack,
                          master=frameSnack, text=member.value, variable=var,
                          onvalue=1, offvalue=0, font=fnt.Font(size=6))
            c.configure(command=c.updateLabelText)
            c.grid(column=0, row=counter, sticky=W)
            self.buttonsSnack[member]["button"] = c
            if var.get() == 1:
                c.updateLabelText()
            counter += 1

        self.submitNewSnackFoodBox = Entry(frameSnack,
                                           text="Add other foods...", width=30, font=fnt.Font(size=8))
        self.submitNewSnackFoodBox.grid(column=0, row=counter, sticky=W)
        self.submitNewSnackFoodButton = Button(master=frameSnack,
                                               text="Add food", command=self.submitNewSnackFood)
        self.submitNewSnackFoodButton.grid(column=0, row=counter + 1)
        self.clearSnackButton = Button(master=frameSnack,
                                       text="Clear all", command=self.clearAllSnack)
        self.clearSnackButton.grid(column=0, row=counter + 2)
        self.clearNonchecksSnackButton = Button(master=frameSnack,
                                                text="Clear nonchecks", command=self.clearNonchecksSnack)
        self.clearNonchecksSnackButton.grid(column=0, row=counter + 3)
        self.labelSnackComponents.grid(column=0, row=counter + 4, pady=10)

        frameControls = Frame(self.master)
        frameControls.columnconfigure(0, weight=1)
        frameControls.grid(column=0, row=1)
        buttonRun = Button(master=frameControls,
                           text="Save foods to Nutri-Q", command=self.run_add_meals)
        buttonRun.grid(column=0, row=0)

        frameLogin = Frame(self.master)
        frameLogin.columnconfigure(0, weight=1)
        frameLogin.grid(column=1, row=1)
        buttonLogin = Button(master=frameLogin,
                             text="Log in to Nutri-Q", command=self.login_to_nutriq)
        buttonLogin.grid(column=0, row=0)

        frameDate = Frame(self.master)
        frameDate.columnconfigure(0, weight=1)
        frameDate.columnconfigure(1, weight=1)
        frameDate.columnconfigure(2, weight=1)
        frameDate.grid(column=2, row=1)

        self.effectiveDate = EffectiveDate()
        self.dateLabel = Label(frameDate,
                               text=self.effectiveDate.to_string() + " (effective today)", width=30)
        self.dateLabel.grid(column=1, row=0)

        self.dateUpButton = DateUpButton(self.effectiveDate,
                                         self.dateLabel, master=frameDate, text=">")
        self.dateUpButton.configure(
            command=self.dateUpButton.incrementDateAndUpdateLabelText)
        self.dateUpButton.grid(column=2, row=0)

        self.dateDownButton = DateDownButton(self.effectiveDate,
                                             self.dateLabel, master=frameDate, text="<")
        self.dateDownButton.configure(
            command=self.dateDownButton.decrementDateAndUpdateLabelText)
        self.dateDownButton.grid(column=0, row=0)

    def submitNewBreakfastFood(self) -> None:
        food_component = self.submitNewBreakfastFoodBox.get()
        self.submitNewBreakfastFoodBox.delete(0, len(food_component))
        if food_component == "" or food_component == "Add other foods...":
            return

        self.labelBreakfastComponents['text'] = _update_list_get_text(
            self.breakfast,
            str(self.labelBreakfastComponents['text']),
            food_component,
            1)

    def submitNewLunchFood(self) -> None:
        food_component = self.submitNewLunchFoodBox.get()
        self.submitNewLunchFoodBox.delete(0, len(food_component))
        if food_component == "" or food_component == "Add other foods...":
            return

        self.labelLunchComponents['text'] = _update_list_get_text(
            self.lunch,
            str(self.labelLunchComponents['text']),
            food_component,
            1)

    def submitNewDinnerFood(self) -> None:
        food_component = self.submitNewDinnerFoodBox.get()
        self.submitNewDinnerFoodBox.delete(0, len(food_component))
        if food_component == "" or food_component == "Add other foods...":
            return

        self.labelDinnerComponents['text'] = _update_list_get_text(
            self.dinner,
            str(self.labelDinnerComponents['text']),
            food_component,
            1)

    def submitNewSnackFood(self) -> None:
        food_component = self.submitNewSnackFoodBox.get()
        self.submitNewSnackFoodBox.delete(0, len(food_component))
        if food_component == "" or food_component == "Add other foods...":
            return

        self.labelSnackComponents['text'] = _update_list_get_text(
            self.snack,
            str(self.labelSnackComponents['text']),
            food_component,
            1)

    def clearAllBreakfast(self) -> None:
        for buttonWrapper in self.buttonsBreakfast.values():
            buttonWrapper["button"].clearAll()

    def clearAllLunch(self) -> None:
        for buttonWrapper in self.buttonsLunch.values():
            buttonWrapper["button"].clearAll()

    def clearAllDinner(self) -> None:
        for buttonWrapper in self.buttonsDinner.values():
            buttonWrapper["button"].clearAll()

    def clearAllSnack(self) -> None:
        for buttonWrapper in self.buttonsSnack.values():
            buttonWrapper["button"].clearAll()

    def clearNonchecksBreakfast(self) -> None:
        findex = 0
        while findex < len(self.breakfast):
            food_component = self.breakfast[findex]
            for name, member in Breakfast.__members__.items():
                if member.value == food_component:
                    findex += 1
                    break
            else:
                self.labelBreakfastComponents['text'] = _update_list_get_text(
                    self.breakfast,
                    str(self.labelBreakfastComponents['text']),
                    food_component,
                    0)

    def clearNonchecksLunch(self) -> None:
        findex = 0
        while findex < len(self.lunch):
            food_component = self.lunch[findex]
            for name, member in MainMeal.__members__.items():
                if member.value == food_component:
                    findex += 1
                    break
            else:
                self.labelLunchComponents['text'] = _update_list_get_text(
                    self.lunch,
                    str(self.labelLunchComponents['text']),
                    food_component,
                    0)

    def clearNonchecksDinner(self) -> None:
        findex = 0
        while findex < len(self.dinner):
            food_component = self.dinner[findex]
            for name, member in MainMeal.__members__.items():
                if member.value == food_component:
                    findex += 1
                    break
            else:
                self.labelDinnerComponents['text'] = _update_list_get_text(
                    self.dinner,
                    str(self.labelDinnerComponents['text']),
                    food_component,
                    0)

    def clearNonchecksSnack(self) -> None:
        findex = 0
        while findex < len(self.snack):
            food_component = self.snack[findex]
            for name, member in Snack.__members__.items():
                if member.value == food_component:
                    findex += 1
                    break
            else:
                self.labelSnackComponents['text'] = _update_list_get_text(
                    self.snack,
                    str(self.labelSnackComponents['text']),
                    food_component,
                    0)

    def to_add_breakfast(self):
        if len(self.breakfast) == 0:
            return False
        for food_name in self.breakfast:
            try:
                food = Breakfast.fromValue(food_name)
                if food is None or not food.is_default_food():
                    return True
            except Exception:
                return True
        return False

    def to_add_snack(self):
        if len(self.snack) == 0:
            return False
        for food_name in self.snack:
            try:
                food = Snack.fromValue(food_name)
                if food is None or not food.is_default_food():
                    return True
            except Exception:
                return True
        return False

    def alert(self, title, message, kind="info", hidemain=True):
        if kind not in ("error", "warning", "info"):
            raise ValueError("Unsupported alert kind.")

        show_method = getattr(messagebox, "show{}".format(kind))
        show_method(title, message)

    def login_to_nutriq(self, hang=True):
        browser = get_driver(False)
        if not connect_to_base(browser):
            browser.close()
        while hang:
            try:
                browser.current_url
            except Exception:
                hang = False
            except KeyboardInterrupt:
                exit()
            time.sleep(2)
        return browser

    def run_add_meals(self) -> None:
        if not (self.to_add_breakfast() or len(self.lunch) > 0
                or len(self.dinner) > 0 or self.to_add_snack()):
            self.alert("Invalid Selection",
                       "Please select or add any non-default food for a valid food selection.",
                       kind="warning")
            return

        run_date = self.effectiveDate.get()
        print("Using date " + str(run_date.month) + "/" + str(run_date.day))

        try:
            browser = self.login_to_nutriq(False)
            if self.to_add_breakfast():
                log_meal(browser, run_date, "Breakfast", -1, self.breakfast)
                self.clearAllBreakfast()
            if len(self.lunch) > 0:
                log_meal(browser, run_date, "Lunch", -1, self.lunch)
                self.clearAllLunch()
            if len(self.dinner) > 0:
                log_meal(browser, run_date, "Dinner", -1, self.dinner)
                self.clearAllDinner()
            if self.to_add_snack():
                log_meal(browser, run_date, "Snack", -1, self.snack)
                self.clearAllSnack()
            browser.close()
        except KeyboardInterrupt:
            pass
        except Exception:
            traceback.print_exc()
            browser.close()


if __name__ == "__main__":
    root = tk.Tk()
    root.title(" Nutri-Q Meals Manager ")
    root.geometry("1400x950")
    # root.attributes('-fullscreen', True)
    root.resizable(1, 1)
    root.columnconfigure(0, weight=1)
    root.columnconfigure(1, weight=1)
    root.columnconfigure(2, weight=1)
    root.columnconfigure(3, weight=1)
    root.rowconfigure(0, weight=8)
    root.rowconfigure(1, weight=1)
    app = App(root)
    root.mainloop()
    exit()
