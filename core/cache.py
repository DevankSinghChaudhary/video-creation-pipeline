def ask():
    while True:
        idea = input("Enter Idea: ").strip()
        if idea:
            break
        print("Cannot be Empty!")

    while True:
        duration = int(input("Enter Max Duration of Video (s): "))
        if duration:
            break
        print("Cannot be Empty!")

    return {
        "topic":idea,
        "duration of video (seconds)":duration
        }

def json_making(str_data):
    start = str_data.find("{")
    end = str_data.rfind("}")
    return str_data[start:end+1]