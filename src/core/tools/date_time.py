"""Tool for getting the current date, time and year."""

from datetime import datetime
from langchain.tools import tool

@tool('get_date_time', description='Get the current date, time and year. USE IT TO RETRIEVE CURRENT DATE AND TIME.', return_direct=False)
def get_date_time() -> str:
    """Get the current date, time and year."""

    print(f'[get_date_time] Tool Called')
    data = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    print(f'[get_date_time] Call Finished')
    return data