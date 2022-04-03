from enum import Enum


class Breakfast(Enum):
    EGGS__HARDBOILED = "Eggs - Hardboiled"
    OATMEAL_WITH_RAISINS = "Oatmeal with raisins"
    GLUTEN_FREE_WAFFLES = "Gluten free waffles"
    HASH_BROWNS__EGGS = "Hash browns & eggs"
    PUFFED_RICE_CEREAL = "Puffed rice cereal"
    UNSWEET_ICED_TEA = "Unsweet iced tea"
    MIXED_FRUIT = "Mixed Fruit"
    WATERMELON = "Watermelon"
    STRAWBERRIES = "Strawberries"
    BLACKBERRIES = "Blackberr"
    ALMONDS_WHOLE = "Almonds - Whole"
    RASPBERRIES = "Raspberr"
    BLUEBERRIES = "Blueberr"
    ORANGE_JUICE = "Orange Juice"

    def is_default_food(self) -> bool:
        return (self is Breakfast.UNSWEET_ICED_TEA
                or self is Breakfast.MIXED_FRUIT
                or self is Breakfast.EGGS__HARDBOILED)

    def fromValue(string: str):
        for name, member in Breakfast.__members__.items():
            if string == member.value:
                return member


class MainMeal(Enum):
    FIFTEEN_BEAN_SOUP = "15 Bean Soup"
    AMYS_BAHN_MI_VEGGIE_WRAP = "Amy's Bahn Mi Veggie Wrap"
    AMYS_GLUTEN_FREE_BURRITO = "Amy's Gluten Free Burrito"
    APPLESAUCE = "Applesauce"
    AVOCADO_GREEK_SALAD = "Avocado Greek Salad"
    BAKED_POTATO = "Baked potato"
    BELL_PEPPER = "Bell Pepper"
    BLT = "BLT"
    BROWN_RICE = "Brown Rice"
    BUTTERNUT_SQUASH_SOUP = "Butternut squash soup"
    CHICK_FIL_A_MARKET_SALAD = "Chick Fil-A Market Salad"
    CHICKEN__SKINLESS = "Chicken - Skinless"
    CHICKEN_KEBAB = "Chicken Kebab"
    CHICKEN_CAESAR_SALAD = "Chicken caesar salad"
    # CHICKEN_WITH_MIXED_VEGETABLES = "Chicken with mixed vegetables"
    CHICKEN_WITH_MIXED_VEGETABLES_AND_RICE = "Chicken with mixed vegetables and rice"
    COCONUT_WATER = "Coconut water"
    # CRAB_CAKE = "Crab Cake"
    EDEN_CAJUN_RICE__BEANS = "Eden cajun rice & beans"
    EGG_SALAD_SANDWICH = "Egg salad sandwich"
    GLUTEN_FREE_BREAD = "Gluten Free Bread"
    GREEN_BEANS = "Green Beans"
    GREEK_SALAD = "Greek Salad"
    # MIXED_FRUIT = "Mixed Fruit"
    MONTE_POLLINO_TUSCAN_BEAN_SOUP_WITH_KALE = "Monte Pollino Tuscan Bean Soup with Kale"
    MUJADARA = "Mujadara"
    NEILLYS_ZESTY_RICE__RED_BEANS_MIX = "Neilly's Zesty Rice & Red Beans Mix"
    PACIFIC_FOODS_CREAMY_PLANT_BASED_BROTH = "Pacific Foods Creamy Plant Based Broth"
    RICE__BEANS = "Rice & Beans"
    RICE_PIZZA = "Rice Pizza"
    RIGHT_FOODS_DR_MCDOUGALLS_BLACK_BEAN_SOUP = "Right Foods Dr. Mcdougall's Black Bean Soup"
    SHAKSHUKA = "Shakshuka"
    SPAGHETTI = "Spaghetti"
    SPAGHETTI_CHICKPEA_BANZA = "Spaghetti Chickpea Banza"
    TROPICAL_SMOOTHIE__SMOOTHIE = "Tropical Smoothie - Smoothie"
    TROPICAL_SMOOTHIE__CHICKEN_WRAP = "Tropical Smoothie - Chicken Wrap"
    TUNA_MELT = "Tuna Melt"
    WILD_RICE_CHERRY_ONION = "Wild Rice Cherry Onion"
    WHITE_RICE = "White Rice"
    TOMATOES = "Tomatoes"
    TURKEY_PEPPERONI = "Turkey Pepperoni"
    # POTATOES = "Potatoes"
    POTATO_CHIPS = "Potato chips"
    SWEET_POTATO = "Sweet Potato"


class Snack(Enum):
    FIFTEEN_BEAN_SOUP = "15 Bean Soup"
    AMYS_VEGETABLE_BARLEY_SOUP = "Amy's Vegetable Barley Soup"
    DRIED_CRANBERRIES = "Dried Cranberries"
    DRIED_MANGO_SLICES = "Dried mango slices"
    KASHI_COCONUT_ALMOND_BAR = "Kashi coconut almond bar"
    OATMEAL = "Oatmeal"
    OAT_BROWNIE = "Oat Brownie"
    OFF_THE_BEATEN_PATH_RICE__PEA_CRACKERS = "Off the Beaten Path Rice & Pea Crackers"
    POPCORN_CHIPS_WITH_SEA_SALT = "Popcorn chips with sea salt"
    SIETE_CHIPS = "Siete chips"
    TERRA_VEGETABLE_CHIPS = "Terra Vegetable Chips"
    WHENEVER_BAR_OAT_BLUEBERRY_LEMON = "Whenever Bar - Oat Blueberry Lemon"

    def is_default_food(self) -> bool:
        return (self is Snack.DRIED_MANGO_SLICES)

    def fromValue(string: str):
        for name, member in Snack.__members__.items():
            if string == member.value:
                return member


class MealType(Enum):
    BREAKFAST = "Breakfast"
    LUNCH = "Lunch"
    DINNER = "Dinner"
    SNACK = "Snack"

    def fromValue(string: str):
        for name, mealtype in MealType.__members__.items():
            if string == mealtype.value:
                return mealtype

    def get_standard_meal_time(self):
        if self is MealType.SNACK:
            return Mealtime(9, 30, "PM")
        elif self is MealType.BREAKFAST:
            return Mealtime(9, 30, "AM")
        elif self is MealType.LUNCH:
            return Mealtime(1, 15, "PM")
        elif self is MealType.DINNER:
            return Mealtime(6, 30, "PM")
        raise AssertionError(
            "Failed to infer time of meal with mealtype " + self.name)

    def get_base_foods(self):
        base_foods = []

        if self is MealType.BREAKFAST:
            base_foods.append(Food("Banana", 2))
            base_foods.append(Food("Turmeric - Ground", 2))
            base_foods.append(Food("Naproxen", 1))
            base_foods.append(Food("Salt", 1))

        elif self is MealType.LUNCH:
            base_foods.append(Food("Water", 2))

        elif self is MealType.DINNER:
            base_foods.append(Food("Water", 2))

        elif self is MealType.SNACK:
            base_foods.append(Food("Turmeric - Ground", 2))
            base_foods.append(Food("Sleepytime tea", 2))
            base_foods.append(Food("Mixed nuts", 1))
            base_foods.append(Food("Naproxen", 1))
            base_foods.append(Food("Salt", 1))
            base_foods.append(Food("Water", 2))

        return base_foods


class MatchType(Enum):
    EXACT = 1
    PARTIAL = 2
    SPACED = 3


class Food:
    def __init__(self, name, quantity, *modifiers):
        self.name = name
        self.validate_quantity(quantity)
        self.quantity = quantity
        self.prep_type = None
        self.match_type = None
        if len(modifiers) > 0:
            self.prep_type = modifiers[0]
            if len(modifiers) > 1:
                self.match_type = modifiers[1]

    def validate_quantity(self, quantity) -> None:
        if quantity not in [0, 1, 2, 3, 4]:
            raise AssertionError("Invalid quantity "
                                 + quantity + " for food " + self.name)

    def set_prep_type(self, prep_type) -> None:
        self.prep_type = prep_type

    def set_match_type(self, match_type) -> None:
        self.match_type = match_type

    def get_quantity_string(self) -> str:
        if self.quantity == 0:
            return "Tiny"
        elif self.quantity == 1:
            return "Small"
        elif self.quantity == 2:
            return "Regular"
        elif self.quantity == 3:
            return "Large"
        elif self.quantity == 4:
            return "Huge"

        raise AssertionError("Invalid quantity " + self.quantity)


def get_food_details(food) -> tuple:
    if ": Cooked" in food:
        return (food[0:(food.index(":"))], "Cooked")
    elif ": Raw" in food:
        return (food[0:(food.index(":"))], "Raw")
    else:
        return (food, None)


def is_small_food(food) -> bool:
    food_lower = food.lower()
    return food_lower in [
        "almonds - whole",
        "cilantro",
        "clementine",
        "coconut water",
        "dried mango slices",
        "elderberry",
        "lime",
        "onion",
        "soy sauce",
        "vinegar",
        ]


def is_exact_match_food(food) -> bool:
    food_lower = food.lower()
    return food_lower in [
        "apple",
        "apples",
        "butter",
        "gluten free waffles",
        "honey",
        "orange",
        "oranges",
        "sugar",
        "turkey",
        ]


def is_food_to_pluralize(food) -> bool:
    food_lower = food.lower()
    return food_lower in [
        "apple",
        "orange",
        ]


def is_raw_food(food) -> bool:
    food_lower = food.lower()
    return food_lower in [
        "bell pepper",
        "bell peppers"
        ]


def is_after_spaced_match_food(food) -> bool:
    food_lower = food.lower()
    return food_lower in [
        "butter",
        ]


class CompositeFood:
    def __init__(self, name):
        self.name = name
        self.foods = []

    def set_foods(self, foods):
        self.foods = foods

    def add_food(self, food):
        self.foods.append(food)

    def add_tinys(self, tinys):
        self._add_tinys(None, tinys)

    def add_smalls(self, smalls):
        self._add_smalls(None, smalls)

    def add_mediums(self, mediums):
        self._add_mediums(None, mediums)

    def add_larges(self, larges):
        self._add_larges(None, larges)

    def _add_tinys(self, prep, tinys):
        self.add_foods_of_size(0, prep, tinys)

    def _add_smalls(self, prep, smalls):
        self.add_foods_of_size(1, prep, smalls)

    def _add_mediums(self, prep, mediums):
        self.add_foods_of_size(2, prep, mediums)

    def _add_larges(self, prep, larges):
        self.add_foods_of_size(3, prep, larges)

    def add_foods_of_size(self, size, prep, food_parts):
        if (isinstance(food_parts, list)):
            for food in food_parts:
                if is_exact_match_food(food):
                    print("Using exact match for food component: " + food)
                    if prep is None:
                        self.foods.append(
                            Food(food, size, "", MatchType.EXACT))
                    else:
                        self.foods.append(
                            Food(food, size, prep, MatchType.EXACT))
                elif prep is None:
                    self.foods.append(Food(food, size))
                else:
                    self.foods.append(Food(food, size, prep))
        elif (isinstance(food_parts, str)):
            if prep is None:
                self.foods.append(Food(food_parts, size))
            else:
                self.foods.append(Food(food_parts, size, prep))


class Mealtime:
    def __init__(self, hour, minute, meridian):
        self.hour = hour
        self.minute = minute
        self.meridian = meridian

    def __eq__(self, other):
        return (self.hour == other.hour
                and self.minute == other.minute
                and self.meridian == other.meridian)


"""
Asian  chicken salad
    "Chicken - Skinless",
    "Cucumber",
    "Carrot",
    "Cabbage",
    "Pear",
    "Coconut water",
    "Cashew",
    "Thai peanut",
    "Ginger",
    "Lettuce",
"""

"""
Nourish bowl
    "Broccoli",
    "Cabbage",
    "Carrots",
    "Kohlrabi",
    "Snap Peas",
    "Brown Rice",
    "Sesame seeds",
    "Sriracha",
"""


def get_meal_component_foods(component_name, mealtype) -> list:
    if component_name is None or component_name == "":
        raise AssertionError("Component name was None or blank")

    comp_food = CompositeFood(component_name)
    component_name_lower = component_name.lower()

    if "reek salad" in component_name_lower:
        if "avocado" in component_name_lower:
            comp_food.add_mediums("Avocados")
        comp_food.add_smalls(["Olives", "Cucumber", "Tomatoes"])
        comp_food.add_tinys(["Garlic", "Lemon oil", "Avocado Oil"])

    elif component_name_lower == "15 bean soup":
        if mealtype is MealType.SNACK:
            comp_food.add_tinys(["Onion", "Garlic", "Salt", "Carrot", "White Bean",
                                 "Yelloweye Bean", "Lentils", "Navy Bean", "Black Beans",
                                 "Pinto Bean", "Lima Bean", "Garbanzo", "Peas", "Kidney Bean"])
        else:
            comp_food.add_tinys(["Onion", "Garlic", "Salt", "Carrot", "White Bean",
                                 "Yelloweye Bean", "Lentils", "Navy Bean", "Black Beans"])
            comp_food.add_smalls(
                ["Pinto Bean", "Lima Bean", "Garbanzo", "Peas", "Kidney Bean"])

    elif component_name_lower == "amy's bahn mi veggie wrap":
        comp_food.add_tinys(["Onions: Cooked", "Garbanzo Beans",
                             "Vinegar", "Potato starch", "Sorghum Flour", "Sunflower Oil",
                             "Sweet rice flour", "Garlic", "Ginger", "Jalape"])
        comp_food.add_smalls(["Mushrooms", "Pinto Beans", "Brown Rice"])
        comp_food.add_mediums(["Tofu"])

    elif component_name_lower == "amy's gluten free burrito":
        comp_food.add_mediums(["Pinto Beans", "Brown Rice"])
        comp_food.add_tinys(["Garbanzo Beans", "Tomato sauce",
                             "Sorghum Flour", "Sunflower Oil", "Sweet rice flour",
                             "Tapioca", "Onions: Cooked"])

    elif component_name_lower == "amy's vegetable barley soup":
        comp_food.add_tinys(["Onions", "Barley", "Carrot",
                             "Tomatoe", "Celery", "Leek", "Zucchini", "Peas",
                             "Sea Salt", "Safflower Oil", "Sunflower oil",
                             "Garlic", "Black Pepper"])

    elif component_name_lower == "baked potato":
        comp_food.add_mediums("Potatoes")
        comp_food.add_tinys("Margarine")

    elif component_name_lower == "blt":
        comp_food.add_mediums(["Fake bacon", "Gluten free bread", "Tomatoes"])
        comp_food.add_smalls("Mayonnaise")

    elif component_name_lower == "chicken kebab":
        comp_food.add_larges("Chicken - Skinless")
        comp_food.add_mediums("White Rice")
        comp_food._add_smalls("Cooked", ["Tomatoes", "Onions", "Cucumber"])
        comp_food.add_tinys(["Lettuce - Iceberg", "Tzatziki"])

    elif component_name_lower == "chicken caesar salad":
        comp_food.add_mediums(["Chicken - Skinless", "Lettuce - Iceberg"])
        comp_food.add_smalls(["Cheese - Parmesan", "Caesar salad dressing"])

    elif "chicken with mixed vegetables" in component_name_lower:
        comp_food.add_larges("Chicken - Skinless")
        comp_food.add_smalls(["Snap peas", "Carrots", "Broccoli"])
        if "and rice" in component_name:
            comp_food.add_mediums("White Rice")

    elif component_name_lower == "chocolate shake":
        comp_food.add_mediums(["Sugar"])
        comp_food.add_smalls(["Milk - Cow"])
        comp_food.add_tinys(["Chocolate"])

    elif "gluten free waffles" in component_name_lower:
        comp_food.add_mediums(["Gluten free waffles"])
        if "syrup" in component_name_lower:
            comp_food.add_smalls(["Maple Syrup", "Margarine"])
        else:
            comp_food.add_smalls(["Margarine"])

    elif component_name_lower == "crab cake":
        comp_food.add_mediums(["Crab"])
        comp_food.add_tinys([
            "Canola oil", "Honey", "Vinegar", "Eggs - Whole", "Salt",
            "Mustard seed", "Vinegar", "Citric acid", "Tartaric acid",
            "Lemon juice", "Paprika", "Apple Cider Vinegar", "Molasses",
            "Soybeans", "Cane sugar", "Tamarind", "Ginger", "Garlic powder",
            "Onion Powder", "Xanthan gum", "Shiitake mushroom powder",
            "Allspice", "Red pepper", "Cloves", "Cayenne",
            ])

    elif component_name_lower == "eden cajun rice & beans":
        comp_food.add_mediums(["Brown Rice", "Red Beans"])
        comp_food.add_smalls(
            ["Tomato Sauce", "Garlic", "Salt", "Cayenne Pepper"])
        comp_food.add_tinys(["Onion", "Red Pepper", "Parsley",
                             "Bay Leaf", "Black Pepper", "Cumin"])

    elif component_name_lower == "egg salad sandwich":
        comp_food.add_mediums("Egg")
        comp_food.add_smalls(["Gluten free bread", "Mayonnaise", "Lettuce"])
        comp_food.add_tinys(["Mustard", "Salt", "Black Pepper"])

    elif component_name_lower == "eggs - hardboiled":
        comp_food.add_smalls(component_name)
        comp_food.add_tinys("Black Pepper")

    elif component_name_lower == "hash browns & eggs":
        comp_food._add_mediums("Cooked", ["Potatoes", "Eggs - Whole"])
        comp_food._add_tinys("Cooked", ["Bell Peppers", "Onions"])
        comp_food.add_tinys("Avocado Oil")

    elif component_name_lower == "kashi coconut almond bar":
        comp_food.add_tinys([
            "Peanuts", "Almond butter", "Coconut",
            "Almonds", "Sunflower seeds", "Tapioca",
            "Pumpkin seeds", "Honey", "Cane sugar"])

    elif component_name_lower == "chick fil-a market salad":
        comp_food.add_larges(["Chicken - Skinless", "Unsweet iced tea"])
        comp_food.add_mediums("Potato chips")
        comp_food.add_smalls([
            "Lettuce - Iceberg", "Lettuce - Romaine", "Lettuce - Butter",
            "Apples", "Strawberries"])
        comp_food.add_tinys(["Blueberries", "Almonds - sliced",
                             "Oats - Gluten Free", "Vinaigrette dressing"])

    elif component_name_lower == "mixed fruit":
        comp_food.add_smalls(["Cantaloupe", "Honeydew Melon"])
        comp_food.add_tinys(["Pineapple", "Grape"])

    elif component_name_lower == "monte pollino tuscan bean soup with kale":
        comp_food.add_mediums("Cannellini Beans")
        comp_food.add_smalls(["Cabbage", "Kale", "Carrot", "Celery"])
        comp_food.add_tinys(["Onions", "Olive Oil"])

    elif component_name_lower == "mujadara":
        comp_food.add_mediums(["Onion", "Yellow Rice"])
        comp_food.add_smalls(["Olive oil", "Cottonseed oil", "Canola oil"])
        comp_food.add_tinys("Yogurt")

    elif component_name_lower == "multivitamin":
        comp_food.add_smalls(component_name)

    elif component_name_lower == "neilly's zesty rice & red beans mix":
        comp_food.add_larges("White Rice")
        comp_food.add_mediums("Red Beans")
        comp_food.add_tinys(["Tomatoes", "Onion", "Garlic", "Green Onion",
                             "Black Pepper", "Canola Oil"])

    elif component_name_lower == "oat vanilla ice cream":
        comp_food.add_smalls(["Oat milk", "Cane sugar", "Tapioca"])
        comp_food.add_tinys("Coconut Oil")

    elif component_name_lower == "oatmeal with raisins":
        comp_food.add_mediums("Oatmeal")
        comp_food.add_tinys("Raisins")

    elif component_name_lower == "off the beaten path rice & pea crackers":
        comp_food.add_smalls(["Rice Flour", "Peas"])
        comp_food.add_tinys(["Sunflower Oil", "Black Bean", "Salt"])

    elif component_name_lower == "rice & beans":
        comp_food._add_mediums("Cooked", "White Rice")
        comp_food.add_mediums("Brown beans")
        comp_food.add_tinys(["Onions", "Honey"])

    elif component_name_lower == "rice pizza":
        comp_food.add_larges("Rice Flour")
        comp_food.add_mediums(["Tomato sauce", "Olive Oil"])
        comp_food._add_smalls(
            "Cooked", ["Mushrooms", "Onions", "Bell Peppers"])
        comp_food.add_smalls(["Parmesan Cheese", "Baking Powder", "Salt"])
        comp_food.add_tinys(["Oregano", "Garlic"])

    elif component_name_lower == "right foods dr. mcdougall's black bean soup":
        comp_food.add_smalls(["Black Beans"])
        comp_food.add_tinys(["Tomatoe", "Onions", "Celery", "Bell Pepper",
                             "Brown Rice", "Cilantro",
                             "Carrots", "Sea Salt", "Basil", "Oregano"])

    elif component_name_lower == "pacific foods creamy plant based broth":
        comp_food.add_smalls("Turmeric")
        comp_food.add_tinys([
            "Onions", "Pea protein", "Celery", "Carrot",
            "Ginger", "Sunflower oil", "Sea salt", "Garlic"])

    elif component_name_lower == "puffed rice cereal":
        comp_food.add_mediums(component_name)
        comp_food.add_smalls("Rice milk")

    elif component_name_lower == "siete chips":
        comp_food.add_mediums("Cassava Flour")
        comp_food.add_smalls(["Avocado Oil", "Salt"])
        comp_food.add_tinys(["Chia Seed", "Coconut Flour"])

    elif component_name_lower == "shakshuka":
        comp_food.add_mediums(["Eggs - Whole", "Paprika"])
        comp_food._add_mediums("Cooked", ["Tomatoe"])
        comp_food._add_smalls("Cooked", ["Onions"])
        comp_food.add_tinys(["Citric Acid", "Salt", "Bell Pepper",
            "Olive Oil", "Garlic", "Cilantro"])

    elif component_name_lower == "spaghetti":
        comp_food.add_larges("Brown rice and lentil pasta")
        comp_food.add_mediums("Tomato sauce")
        comp_food._add_smalls("Cooked", ["Mushrooms", "Onions"])

    elif component_name_lower == "spaghetti chickpea banza":
        comp_food.add_mediums(["Chickpea", "Tomato sauce"])
        comp_food.add_smalls(["Pea starch", "Tapioca"])
        comp_food._add_smalls("Cooked", ["Mushrooms", "Onions"])

    elif component_name_lower == "sweet potato" or component_name_lower == "sweet potatoes":
        comp_food.add_mediums("Sweet Potatoes")
        comp_food.add_tinys("Margarine")

    elif component_name_lower == "terra vegetable chips":
        comp_food.add_smalls(["Sweet potato chips", "Taro chips"])
        comp_food.add_tinys(
            ["Batata", "Parsnip chips", "Canola Oil", "Safflower Oil", "Sunflower Oil"])

    elif component_name_lower == "tropical smoothie - smoothie":
        comp_food.add_mediums("Smoothie - sugar, banana, strawberry, lime")
        comp_food.add_smalls("Vitamin")
        comp_food.add_tinys("Chia seed")

    elif component_name_lower == "tropical smoothie - chicken wrap":
        comp_food.add_mediums(["Chicken - Skinless", "Gluten free wrap"])
        comp_food.add_smalls(["Thai peanut sauce", "Lettuce - Iceberg"])
        comp_food.add_tinys(["Cilantro", "Carrot", "Onion"])

    elif component_name_lower == "tuna melt":
        comp_food.add_mediums(
            ["Tuna", "Cheese - Provolone", "Gluten Free Bread - Toasted"])
        comp_food.add_smalls(["Mayonnaise", "Butter"])

    elif component_name_lower == "whenever bar - oat blueberry lemon":
        comp_food.add_smalls(["Oats", "Agave", "Sugar"])
        comp_food.add_tinys(["Blueberr",
                             "Safflower", "Sunflower", "Chia Seed", "Egg",
                             "Nutmeg", "Rice Flour", "Almond", "Tapioca"])

    elif component_name_lower == "wild rice cherry onion":
        comp_food.add_mediums("Wild Rice")
        comp_food.add_smalls(["Cherry", "Margarine"])
        comp_food.add_tinys("Onion")

    elif is_small_food(component_name_lower):
        comp_food.add_smalls(component_name)

    elif is_exact_match_food(component_name_lower):
        if is_food_to_pluralize(component_name_lower):
            return [Food(component_name + "s", 2, "Raw", MatchType.EXACT)]
        elif component_name_lower == "apples":
            return [Food("Apples", 2, "Raw", MatchType.EXACT)]
        else:
            return [Food(component_name, 2, None, MatchType.EXACT)]

    elif is_raw_food(component_name_lower):
        return [Food(component_name, 2, "Raw")]

    else:
        component_name, prep = get_food_details(component_name)
        if prep is None:
            return [Food(component_name, 2)]
        else:
            return [Food(component_name, 2, prep)]

    return comp_food.foods
