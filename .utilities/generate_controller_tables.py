import json
import textwrap
import glob

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
    result += f"""{'#'*(level+1)} Functions

<details>

{process_dict(controller["functions"], level=level+2)}

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

result = process_all()

with open(".wiki/List of controllers.md", "wt", encoding="utf-8") as md_file:
    md_file.write(result)
