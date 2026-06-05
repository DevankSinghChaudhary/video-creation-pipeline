from pydantic import BaseModel

#============
# Cleaner Agent Output Structure
#============
class CleanerAgentOutput(BaseModel):
    summary: str