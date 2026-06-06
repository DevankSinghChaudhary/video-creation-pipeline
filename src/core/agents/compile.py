from core.schemas.state import state
import time

def compiler(state: state):
    t = time.time()
    final_report = (
        f"Topic: {state['topic']}\n\n"
    )

    for summary in state["summaries"]:
        final_report += f"- {summary}\n\n"

    print('Compiler: ', time.time() - t)
    return {
        "final_report": final_report
    }