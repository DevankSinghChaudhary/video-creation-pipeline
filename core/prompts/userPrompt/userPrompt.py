def researcherPromptMaking(user_input):
    if not user_input:
        raise ValueError("User input not available!")
    
    prompt = f"""
YOU ARE AN EXPERT RESEARCH QUERY GENERATOR FOR DOCUMENTARY AND EXPLAINER VIDEOS.

TOPIC:
{user_input}

YOUR TASK:
Understand the REAL meaning and category of the topic first.

Then generate highly relevant web search queries that will help gather:
- factual information
- timelines
- causes
- impacts
- mechanisms
- controversies
- visuals
- geography
- statistics
- human impact
- strategic importance
- scientific explanations
- economic implications

IMPORTANT:
DO NOT blindly combine the topic with generic keywords.

First determine:
- what the topic actually is
- what fields it belongs to
- what information matters most

EXAMPLES:

If topic is:
"Kepler-452b"

Good queries:
- Kepler-452b habitability explained
- how Kepler-452b was discovered
- Kepler transit detection method
- Kepler-452b compared to Earth
- Kepler-452b atmosphere possibilities

If topic is:
"Great Nicobar Project"

Good queries:
- Great Nicobar Project explained
- Great Nicobar Project environmental impact
- Great Nicobar Project India strategic importance
- Great Nicobar Project map and location
- Great Nicobar Project tribal concerns
- Great Nicobar Project infrastructure plan
- Great Nicobar Project relation to Indo-Pacific strategy
- Great Nicobar transshipment port explained

BAD QUERIES:
- Nicobar step by step
- Nicobar rise and fall
- Nicobar stakeholder analysis

RULES:
- Queries must sound natural and realistic
- Queries must help create informative visual explainers
- Prefer searchable human-like queries
- Avoid repetitive query patterns
- Avoid meaningless combinations
- Focus on high-information searches

OUTPUT:
RETURN ONLY VALID JSON

{{
  "search_queries": [
    "query1",
    "query2",
    "query3"
  ]
}}
"""
    return prompt