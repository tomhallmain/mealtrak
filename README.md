# mealtrak

Simple app to automate the process of meal data entry and analysis. Only supports entry into the Nutri-Q platform at this time.

## Setup

Clone this repository and ensure python3, chromedriver, and selenium are installed. Add your Nutri-Q credentials to a JSON file called creds.json and place in the nutriq directory.

### Setting up stored meals

For now, the only way to add stored meals to the pre-selection list is to modify the enums and update method `get_meal_component_foods` as needed in the `meal_components.py` file.

## Usage

Once complete, run from the runner file:

```bash
$ python3 ~/mealtrak/nutriq/nutriq_add_meals_runner.py
```
