import json

def get_systemprompt(agent_name):
    with open('src\core\promptconfig.json', 'r', encoding='utf-8') as file:
        config = json.load(file)

    system_prompt = config["node"]["research"][agent_name]["system_prompt"]
    return system_prompt