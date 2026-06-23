import os
import time
from dotenv import load_dotenv

from langchain.agents import create_agent
from langchain_openai import ChatOpenAI

from core.nodes.state.research.state import FormatterState
from core.nodes.state.globalstate import GlobalInformationState
from core.prompt import get_systemprompt

load_dotenv()
model = ChatOpenAI(
    model = 'mistral-large-latest',
    base_url = 'https://api.mistral.ai/v1',
    api_key = os.getenv('MISTRALAI_API_KEY')
)

system_prompt = get_systemprompt("formatter")

def Formatter(state: GlobalInformationState):
    script = state['script']


    prompt = f"""
    You will receive a documentary narration script.

    INPUT SCRIPT:
    {script}

    TASK:
    Refine this script only for TTS delivery.

    IMPORTANT:
    - Preserve all meaning exactly.
    - Preserve all facts, names, dates, and sequence.
    - Convert all numbers into fully spoken words.
    - Fix only unnatural spoken flow if necessary.
    - Do not add or remove information.
    - Do not rewrite for creativity.

    PUNCTUATION RULES:

    Use punctuation for speech timing, not formal writing.

    - Periods create full stops and should control major breath points.
    - Commas should only separate clauses that are naturally spoken together.
    - Never stack multiple commas in one sentence unless unavoidable.
    - Avoid commas before short trailing phrases.
    - Prefer splitting long comma-heavy sentences into separate sentences.
    - Use em-dashes only for hard tonal shifts or sharp factual pivots.
    - Use ellipses only for intentional dramatic hesitation and rarely.

    TTS RHYTHM RULES:

    - Each sentence should carry one primary spoken idea.
    - Avoid more than one major pause inside a sentence.
    - If a sentence contains two unrelated facts, split them.
    - If two sentences are too short and sound choppy, merge them.
    - Prefer uneven sentence lengths for natural cadence.
    - Alternate short and medium sentence lengths when possible.
    - Avoid repetitive sentence openings.
    - Avoid back-to-back identical rhythm structures.

    BREATH RULE:

    Every sentence should be speakable in one natural breath unless the content requires emphasis.
    If it feels breath-heavy, split it.
    If it feels too fragmented, merge it.

    WORD FORMATTING RULE:

    When converting numbers into spoken words:

    - Never hyphenate compound numbers.
    - Always separate compound number words with spaces.

    Examples:
    - forty five (correct)
    - sixty two (correct)
    - one hundred twenty three (correct)
    etc

    Forbidden:
    - forty-five
    - sixty-two
    - one-hundred
    etc
    
    Also:
    - state-on-state
    - full-scale
    etc
    Tip: Don't use hyphen '-' at all.
    Reason:
    Hyphens can introduce unnatural pauses or segmentation in TTS engines.

    All number words must be space-separated for smoother pronunciation.

    PAUSE PRIORITY:

    Meaning > grammar > pacing.

    If punctuation improves grammar but hurts speech flow, prefer speech flow.
    
    IMPORTANT NOTE: TTS models do not care about grammer pauses(often times break the flow), its purely based on our formatting. 
    
    Return only the final TTS-safe narration.
    """

    agent = create_agent(
        model = model,
        system_prompt = system_prompt,
        response_format = FormatterState
    )
    
    t = time.time()
    result = agent.invoke({
        'messages':{
            'role':'user',
            'content': prompt
        }
    })
    print('Formatter: ', time.time() - t)
    result = result['structured_response']
    return {
        'script': result
    }