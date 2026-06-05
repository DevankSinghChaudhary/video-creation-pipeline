# from langchain_openai import ChatOpenAI
# from dotenv import load_dotenv

# load_dotenv()

# model = ChatOpenAI(
#     model="nvidia/nemotron-3-ultra-550b-a55b",
#     base_url="https://integrate.api.nvidia.com/v1",
#     api_key="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",
#     timeout=200,
#     max_retries=0
# )

# prompt = """
# Topic: World War II consequences.

# TASK:
# Generate a Research Plan for a documentary.

# FORMAT:
# - strict schema only
# - no explanation
# - structured JSON style output

# STYLE: documentary explainer
# DOMAIN: auto-infer
# """

# result = model.invoke(prompt)

# print(result.content)



import requests

url = "https://integrate.api.nvidia.com/v1/models"

r = requests.get(url, timeout=10)
print(r.status_code)