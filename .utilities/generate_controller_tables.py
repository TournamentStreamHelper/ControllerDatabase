import json
import textwrap
import glob
from copy import deepcopy

with open(".utilities/consoles_list.json") as json_file:
    consoles_dict = json.loads(json_file.read())

def bool_to_emoji(boolean: bool):
    if boolean:
        return("✔️")
    else:
        return("❌")

def str_to_emoji(string: str):
    if string:
        if string == "+":
            return("➕")
        if string == "-":
            return("➖")
        return(string)
    else:
        return("❌")

def process_list(source: list, level = 1):
    result = ""
    for i in range(len(source)):
        result += f"""
{'#'*level} `{i}`
"""
        if not source[i] and (type(source[i])!=bool):
            result += "None\n"
        elif type(source[i]) in (int, float, str, bool):
            result += f"{source[i]}\n"
        elif type(source[i])==dict:
            result += f"""
<details>

{process_dict(source[i], level+1)}

</details>
"""
        elif type(source[i])==list:
            result += f"""
<details>

{process_list(source[i], level+1)}

</details>

"""
    return(result)


def process_dict(source: dict, level = 1):
    result = ""
    source = {key: source[key] for key in sorted(source)}
    for key in source.keys():
        result += f"""
{'#'*level} `{key}`
"""
        if not source[key] and (type(source[key])!=bool):
            result += "None\n"
        elif type(source[key]) in (int, float, str, bool):
            result += f"{source[key]}\n"
        elif type(source[key])==dict:
            result += f"""
<details>

{process_dict(source[key], level+1)}

</details>

"""
        elif type(source[key])==list:
            result += f"""
<details>

{process_list(source[key], level+1)}

</details>

"""
    return(result)

def process_socd(list_socd):
    result = ""
    if list_socd:
        for i in range(len(list_socd)):
            if i != 0:
                if i == len(list_socd)-1:
                    result += " or "
                else:
                    result += ", "
            if list_socd[i] == "disable":
                result += "Disabled"
            if list_socd[i] == "neutral":
                result += "Neutral"
            if list_socd[i] == "last_input":
                result += "Last Direction"
            if list_socd[i] == "first_input":
                result += "First Direction"
            if list_socd[i] == "up":
                result += "Always Up"
    else:
        result += bool_to_emoji(False)
    return(result)

def process_directional_buttons(list_buttons, title="Directional Buttons", level = 1):
    result =""
    if list_buttons:
        result += f"""{'#'*level} {title}

"""
        for i in range(len(list_buttons)):
            button_set = list_buttons[i]
            result += process_list_string(button_set["set"], title=f"Set #{i+1}", level=level+1)
            result += "**SOCD Cleaning**\n\n"
            result += f"- Hardware SOCD Cleaning: {bool_to_emoji(button_set['socd_prevention']['hardware'])}\n"
            if button_set['socd_prevention']['software']:
                result += f"- Software SOCD Cleaning:\n"
                result += f"  - Left + Right: {process_socd(button_set['socd_prevention']['software']['left_right'])}\n"
                result += f"  - Up + Down: {process_socd(button_set['socd_prevention']['software']['up_down'])}\n"
            else:
                result += f"- Software SOCD Cleaning: {bool_to_emoji(False)}\n"

        result += "\n"
    return(result)


def process_stick_or_trackpad(list_stick, title="Analog Sticks", level = 1):
    result =""
    if list_stick:
        result += f"""{'#'*level} {title}

| Name | Clickable |
| :---: | :---: |
"""
        for stick in list_stick:
            clickable = stick.get("has_button") or stick.get("clickable")
            result += f"| {stick['name']} | {bool_to_emoji(clickable)} |\n"
        result += "\n"
    return(result)

def process_screen(list_screen, title="Touch Screens", level = 1):
    result = ""
    if list_screen:
        result += f"""{'#'*level} {title}

| Index | Resolution | Type |
| :---: | :---: | :---: |
"""
        for i in range(len(list_screen)):
            screen = list_screen[i]
            resolution = f"{screen['resolution'][0]}x{screen['resolution'][1]}"
            result += f"| {i+1} | {resolution} | {screen['type'].title()} |\n"
        result += "\n"
    return(result)

def process_list_string(list_str, title="Menu Buttons", level = 1):
    result = ""
    if list_str:
        result += f"""{'#'*level} {title}

"""
        for button_name in list_str:
            result += f"- {str_to_emoji(button_name)}\n"
        result += "\n"
    return(result)

def process_digital_to_analog(list_digital_analog, title="Digital-to-Analog Conversion Features", level = 1):
    result = ""
    if list_digital_analog:
        result += f"""{'#'*level} {title}

| Emulated Input | Type of conversion | Associated Modifier Buttons |
| :---: | :---: | :---: |
"""
        for conversion in list_digital_analog:
            if conversion["type"] == "8_way":
                type_conversion = "8-way Movement"
            if conversion["type"] == "button":
                type_conversion = "Full Button Press"
            if conversion["type"] == "precision":
                type_conversion = "Precise Input"
            result += f"| {conversion['emulated_analog']} | {type_conversion} | {conversion['modifier_buttons']} |\n"
        result += "\n"
    return(result)

def process_functions(functions:dict, level=1):
    result = ""

    # Sticks / Trackpads
    result += process_stick_or_trackpad(functions["analog_sticks"], title="Analog Sticks", level=level)
    result += process_stick_or_trackpad(functions["digital_sticks"], title="Digital Sticks", level=level)
    result += process_stick_or_trackpad(functions["trackpads"], title="Trackpads", level=level)

    # Directional Buttons
    result += process_directional_buttons(functions["directional_buttons"], title="Directional Buttons", level=level)

    # Action Buttons
    if functions.get("action_buttons"):
        result += f"""{'#'*level} Action Buttons

| Name | Analog |
| :---: | :---: |
"""
        for button in functions.get("action_buttons"):
            result += f"| {button['name']} | {bool_to_emoji(button['analog'])} |\n"
        result += "\n"
    
    # Other Buttons
    result += process_list_string(functions.get("menu_buttons"), title="Menu Buttons", level=level)
    result += process_list_string(functions.get("system_buttons"), title="System Buttons", level=level)
    result += process_list_string(functions.get("other_buttons"), title="Other Buttons", level=level)

    # Digital-to-Analog conversion
    result += process_digital_to_analog(functions.get("digital_to_analog_conversion"), title="Digital-to-Analog Conversion Features", level=level)

    # Touch Screens
    result += process_screen(functions.get("touch_screens"), title="Touch Screens", level=level)

    # Cable info
    if functions.get("cable"):
        result += f"""{'#'*level} Cable

- Interface: {functions['cable']['interface']}
- Removable: {bool_to_emoji(functions['cable']['removable'])}

"""

    # Other functions
    rumble = str_to_emoji(functions['rumble'])

    result += f"""{'#'*level} Other Features

| Feature | Value |
| :---: | :---: |
| Macro | {bool_to_emoji(functions['macro'])} |
| Turbo | {bool_to_emoji(functions['turbo'])} |
| Accelerometer | {bool_to_emoji(functions['accelerometer'])} |
| Gyroscope | {bool_to_emoji(functions['gyroscope'])} |
| IR Reciever | {bool_to_emoji(functions['ir_reciever'])} |
| Extension Ports | {functions['extension_ports']} |
| Headset Port | {bool_to_emoji(functions['headset_port'])} |
| Speaker | {bool_to_emoji(functions['speaker'])} |
| Microphone | {bool_to_emoji(functions['microphone'])} |
| Rumble | {rumble.title()} |
| Bluetooth | {bool_to_emoji(functions['bluetooth'])} |
| 2.4GHz Wireless | {bool_to_emoji(functions['2_4ghz'])} |
| XInput | {bool_to_emoji(functions['pc_xinput'])} |
| Steam Input Compatibility | {bool_to_emoji(functions['pc_steaminput'])} |"""

    return(result)

def process_controller(path, level = 1):
    with open(f"{path}/config.json", "rt", encoding="utf-8") as json_file:
        controller = json.loads(json_file.read())
    image_url = f"https://raw.githubusercontent.com/Wolfy76700/ControllerDatabase/main/{path}/image.png"
    result = f"{'#'*level} {controller['name']}\n"
    result += f"""
<picture>
<img src="{image_url}" alt="{controller['name']}" height="250">
</picture>

"""
    if controller.get("source"):
        result += f"*More information: {controller.get('source')}*\n\n"
    if controller["functions"].get("native_consoles"):
        result += f"{'#'*(level+1)} Native console compatibility\n\n"
        sorted_list = deepcopy(controller["functions"].get("native_consoles"))
        sorted_list.sort()
        for console in sorted_list:
            result += f"- {consoles_dict[console]}\n"
        result += "\n"
    result += f"""{'#'*(level+1)} Functions

<details>

{process_functions(controller["functions"], level=level+2)}

</details>

"""
    if controller.get("variants"):
        result += f"""{'#'*(level+1)} Variants

<details>

"""
        for variant in controller.get("variants"):
            result += f"""{'#'*(level+2)} {variant['name']}

<picture>
<img src="https://raw.githubusercontent.com/Wolfy76700/ControllerDatabase/main/{path}/{variant['image']}" alt="{variant['name']}" height="150"/>
</picture>

"""
        result += f"</details>\n\n"


    return(result)

def process_manufacturer(path, level=1):
    with open(f"{path}/config.json", "rt", encoding="utf-8") as json_file:
        manufacturer = json.loads(json_file.read())
    list_folders = glob.glob(f"{path}/*/")
    list_folders.sort()
    if not list_folders:
        return("")
    result = f"{'#'*level} {manufacturer['name']}\n\n"
    for folder in list_folders:
        result += process_controller(folder.replace("\\", "/"), level+1)
    return(result)

def process_category(path, level=1):
    with open(f"{path}/config.json", "rt", encoding="utf-8") as json_file:
        category = json.loads(json_file.read())
    list_folders = glob.glob(f"{path}/*/")
    list_folders.sort()
    if not list_folders:
        return("")
    result = f"{'#'*level} {category['name']}\n\n*{category['desc']}*\n\n"
    for folder in list_folders:
        result += process_manufacturer(folder.replace("\\", "/"), level+1)
    return(result)

def process_all():
    list_folders = glob.glob(f"*/")
    result = ""
    for folder in list_folders:
        print(folder)
        result += process_category(folder.replace("\\", "/"))
    return(result)

def create_consoles_table():
    result = "| ID | Name |\n| :---: | :--- |\n"
    for console in consoles_dict.keys():
        result += f"| `{console}` | {consoles_dict[console]} |\n"
    with open(".wiki/Console IDs.md", "wt", encoding="utf-8") as md_file:
        md_file.write(result)

result = process_all()
create_consoles_table()

with open(".wiki/List of controllers.md", "wt", encoding="utf-8") as md_file:
    md_file.write(result)
