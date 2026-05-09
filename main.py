import json
from cache import ask, json_making
from prompts import researcherPromptMaking, researchSystemPrompt
from models import generalModel
from researcher import search_google


def main():
    user_input = ask()
    researcherPrompt = researcherPromptMaking(user_input)
    str_data = generalModel(researcherPrompt, researchSystemPrompt)
    raw_data = json_making(str_data)
    data = json.loads(raw_data)
    urls = search_google(data)
    print(urls)
    

if __name__ == "__main__":
    main()