import os
import time
from dotenv import load_dotenv

from langchain.agents import create_agent
from langchain_openai import ChatOpenAI

from core.nodes.state.research.state import ScriptState
from core.nodes.state.globalstate import GlobalInformationState
from core.prompt import get_systemprompt

load_dotenv()
model = ChatOpenAI(
    model = 'mistral-large-latest',
    base_url = 'https://api.mistral.ai/v1',
    api_key = os.getenv('MISTRALAI_API_KEY')
)

system_prompt = get_systemprompt("writer")

def Writer(state: GlobalInformationState):
    topic = state['topic']
    information = state['information']


    prompt = f"""
    ROLE:
    Elite documentary narration engine.

    TASK:
    Convert provided structured research units into a single continuous documentary narration.

    CORE RULE:
    Use ONLY provided information. No invention. No stylistic padding. No external knowledge.

    SPOKEN REALISM RULE:
    The output must sound like natural spoken documentary narration, not written explanation.

    To achieve this:

    Vary sentence length (short, medium, slightly extended)
    Allow 1-2 sentence fusions when facts are tightly related
    Do NOT make every sentence equal in weight
    Avoid explicit “this led to that” explanation chains unless necessary
    Prefer implication over over-explanation when causality is obvious from context
    Reduce repetitive grammatical structures across consecutive sentences

    ❌ BAN LIST (STRONG ADDITION)

    Remove these patterns entirely:
    “This X marked Y”
    “It also made a decision”
    “That alliance had been built on…”
    “The question is no longer X—but Y” (overused AI documentary closure form)
    symmetrical sentence chaining (“A happened. B happened. C happened.” rhythm)
    
    HARD CONSTRAINTS:

    30-40 seconds spoken duration
    90-120 words target
    max 140 words absolute
    one unified narration (NOT per ID breakdown in output)
    no formatting, no labels, no structure markers

    CONTENT RULES:

    Every sentence must introduce new factual information
    No repetition or paraphrasing of same idea
    No filler, no setup phrases, no commentary language
    No generic documentary phrases (“this reveals”, “this highlights”, “it is important to note”)
    No emotional framing unless explicitly in data
    No rhetorical questions
    No transitions like “meanwhile”, “in turn”, “today”, unless factually required

    FIRST SENTENCE RULE (STRICT):
    Must begin with:

    a concrete event OR
    measurable consequence OR
    verified incident OR
    quantifiable outcome

    Forbidden openings:

    background explanations
    historical framing
    vague setups (“over time”, “through history”, etc.)

    STRUCTURE (MANDATORY FLOW):
    Sentence 1: Core factual event or outcome
    Sentence 2-3: Key mechanism or cause
    Sentence 4-5: Consequence or broader impact

    STYLE RULE:
    Neutral, factual, high-density informational narration.
    No “AI documentary voice”.

    OUTPUT RULE:
    Return ONLY final script text.
    No labels.
    No formatting.
    No explanations.

    
    IMPORTANT:
    This is a short-form documentary.
    You must compress the material into a maximum of one hundred twenty words and a maximum of five spoken segments.

    Do not cover all research if it exceeds the time budget.
    Select only the highest-value facts.


    TOPIC: {topic}

    INFORMATION: {information}
    """

    agent = create_agent(
        model = model,
        system_prompt = system_prompt,
        response_format = ScriptState
    )
    
    t = time.time()
    result = agent.invoke({
        'messages':{
            'role':'user',
            'content': prompt
        }
    })
    print('Writer: ', time.time() - t)
    result = result['structured_response']
    return {
        'script': result
    }