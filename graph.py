from typing import TypedDict

from langgraph.graph import StateGraph, END

from agents import (
    researcher_agent,
    writer_agent,
    critic_agent
)


class ResearchState(TypedDict):
    topic: str
    research_notes: str
    report: str
    feedback: str
    score: int
    approved: bool
    revision_count: int



def research_node(state: ResearchState):
    notes = researcher_agent(state["topic"])

    return {
        "research_notes": notes
    }



def writer_node(state: ResearchState):
    report = writer_agent(
        topic=state["topic"],
        research_notes=state["research_notes"],
        feedback=state.get("feedback", "")
    )

    return {
        "report": report
    }



def critic_node(state: ResearchState):
    result = critic_agent(state["report"])

    return {
        "feedback": result["feedback"],
        "score": result["score"],
        "approved": result["approved"],
        "revision_count": state["revision_count"] + 1
    }



def supervisor(state: ResearchState):
    if state["approved"]:
        return END

    if state["revision_count"] >= 3:
        return END

    return "writer"


builder = StateGraph(ResearchState)

builder.add_node("research", research_node)
builder.add_node("writer", writer_node)
builder.add_node("critic", critic_node)

builder.set_entry_point("research")

builder.add_edge("research", "writer")
builder.add_edge("writer", "critic")

builder.add_conditional_edges(
    "critic",
    supervisor
)

graph = builder.compile()