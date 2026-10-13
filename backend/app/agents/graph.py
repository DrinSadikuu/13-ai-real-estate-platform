
from langchain_openai import ChatOpenAI
from langchain_core.messages import ToolMessage

from langgraph.graph import END, StateGraph
from langgraph.prebuilt import ToolNode

from langgraph.types import interrupt

from app.agents.state import AgentState
from app.core.config import get_settings

from app.tools.property_matching import find_property_matches_for_client
from app.tools.client_tools import get_client
from app.tools.property_tools import get_property, get_properties
from app.tools.viewing_tools import get_viewing, get_viewings
from app.tools.viewing_actions import schedule_viewing


settings = get_settings()

read_tools = [
    find_property_matches_for_client,
    get_client,
    get_property,
    get_properties,
    get_viewing,
    get_viewings,
]

write_tools = [schedule_viewing]
tools = read_tools + write_tools

model = ChatOpenAI(
    model=settings.openai_model,
    api_key=settings.openai_api_key,
)

model_with_tools = model.bind_tools(
    tools,
    parallel_tool_calls=False,
)


async def call_model(state: AgentState):
    response = await model_with_tools.ainvoke(state["messages"])
    return {"messages": [response]}


def route_tools(state: AgentState):
    last_message = state["messages"][-1]

    if not last_message.tool_calls:
        return END

    tool_name = last_message.tool_calls[0]["name"]

    if tool_name == "schedule_viewing":
        return "approval_gate"

    return "read_tools"


def approval_gate(state: AgentState):
    last_message = state["messages"][-1]
    pending_call = last_message.tool_calls[0]

    approved = interrupt({
        "type": "approval_required",
        "pending_actions": [pending_call],
    })

    if approved:
        return {"approved": True}

    return {
        "approved": False,
        "messages": [
            ToolMessage(
                content="Viewing scheduling was rejected by the employee.",
                tool_call_id=pending_call["id"],
            )
        ],
    }



def route_approval(state: AgentState):
    if state["approved"]:
        return "write_tools"

    return "agent"


builder = StateGraph(AgentState)

builder.add_node("agent", call_model)
builder.add_node("read_tools", ToolNode(read_tools))
builder.add_node("approval_gate", approval_gate)
builder.add_node("write_tools", ToolNode(write_tools))

builder.set_entry_point("agent")

builder.add_conditional_edges(
    "agent",
    route_tools,
    {
        "read_tools": "read_tools",
        "approval_gate": "approval_gate",
        END: END,
    },
)

builder.add_edge("read_tools", "agent")

builder.add_conditional_edges(
    "approval_gate",
    route_approval,
    {
        "write_tools": "write_tools",
        "agent": "agent",
    },
)

builder.add_edge("write_tools", "agent")

def create_graph(checkpointer):
    return builder.compile(checkpointer=checkpointer)
