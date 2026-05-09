from openai import OpenAI
from dotenv import load_dotenv
import os


load_dotenv()
client = OpenAI(
  base_url = "https://integrate.api.nvidia.com/v1",
  api_key = os.getenv("NVIDIA_AI")
)

def generalModel(researchPrompt, researchSystemPrompt):
    completion = client.chat.completions.create(
        model="openai/gpt-oss-120b",
        messages=[{"role":"user","content":researchPrompt},{"role":"system","content":researchSystemPrompt}],
        temperature=1,
        top_p=1,
        max_tokens=5000,
        stream=False
    )
    return completion.choices[0].message.content