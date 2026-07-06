import os
import time
from dotenv import load_dotenv

from langchain.agents import create_agent
from langchain_openai import ChatOpenAI

from core.nodes.retries import with_retry
from core.nodes.script.tools.FactsSelector import FactSelectorAgent
from core.nodes.script.tools.NarrativeFlow import NarrativeFlowBuilder
from core.nodes.script.tools.ContinuityAgent import ContinuityAgent

from core.nodes.script.state.ScriptWriter import ScriptState
from core.nodes.state.globalstate import GlobalInformationState
from core.prompt import get_systemprompt

load_dotenv()

model = ChatOpenAI(
    model = 'ministral-14b-2512',
    base_url = 'https://api.mistral.ai/v1',
    api_key = os.getenv('MISTRALAI_API_KEY')
)

system_prompt = get_systemprompt("writer")


@with_retry
def Writer(state: GlobalInformationState):

    print(f'[Writer] Started Processing')
    st = time.time()

    topic = state['topic']
    information = state['information']
    
    prompt = f"""
    ROLE:
    Documentary narration writer.

    TASK:
    Convert the provided ordered factual units into one continuous short-form documentary narration.

    CORE RULE:
    Use only provided information.
    Do not invent facts.
    Do not add external knowledge.
    Do not add filler.

    SPOKEN REALISM:
    The output must sound natural when spoken.

    Rules:

    * Vary sentence length naturally
    * Avoid repetitive sentence structures
    * Allow sentence fusion when facts are tightly connected
    * Prefer natural spoken rhythm over rigid written form
    * Avoid over-explaining obvious causal relationships

    BANNED:

    * Generic documentary phrases
    * Filler phrases
    * Commentary phrases
    * Rhetorical questions
    * Artificial suspense
    * Dramatic closers
    * Symmetrical repetitive sentence rhythm

    CONTENT RULES:

    * Every sentence must add new factual information
    * No repetition
    * No paraphrasing of the same fact
    * No emotional exaggeration
    * No vague setup phrases

    OPENING RULE:
    Start with the strongest concrete event, incident, or measurable fact.

    Never start with:

    * background
    * broad context
    * vague historical framing

    LENGTH:

    * Target: 50-60 words
    * Hard max: 80 words

    STYLE:
    Neutral.
    Dense.
    Factual.
    Natural spoken documentary narration.

    OUTPUT:
    Return only the final narration text.

    TOOLS:

    FactSelectorAgent:
    Use when the available information is too large, redundant, or exceeds the time budget.
    Purpose: select only the highest-value factual units.
    Input:
    - topic
    - intent
    - information

    NarrativeFlowBuilder:
    Use after fact selection when factual units need ordering.
    Purpose: arrange selected facts into strongest documentary progression.
    Input:
    - topic
    - intent
    - selected_facts

    ContinuityAgent:
    Use after narrative flow building and script generation when the factual sequence or written narration needs structural validation.
    Purpose: inspect factual order and script continuity for chronology, causality, missing bridges, escalation flow, redundancy, and context gaps.
    It does not rewrite, repair, reorder, or add facts. It only validates structural integrity.
    Input:
    - topic
    - intent
    - ordered_facts
    - script

    TOPIC: {topic}
    INFORMATION: {information}
    """

    agent = create_agent(
        model = model,
        system_prompt = system_prompt,
        response_format = ScriptState,
        tools = [FactSelectorAgent, NarrativeFlowBuilder,ContinuityAgent]
    )
    
    result = agent.invoke({
        'messages':{
            'role':'user',
            'content': prompt
        }
    })
    result = result['structured_response']
    
    print(f'[Writer] Finished Successfully')
    print(f'[Writer] {time.time()-st}')
    
    return {
        'script': result
    }