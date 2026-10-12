from langchain_openai import ChatOpenAI
from langgraph.graph import END, StateGraph
from langgraph.prebuilt import ToolNode

from app.agents.state import AgentState
from app.core.config import get_settings
from app.tools.property_matching import find_property_matches_for_client
from app.tools.client_tools import get_client
from app.tools.property_tools import get_property,get_properties
from app.tools.viewing_tools import get_viewing, get_viewings

settings = get_settings()

tools = [
    find_property_matches_for_client,
    get_client,
    get_property,
    get_properties,
    get_viewing,
    get_viewings,
]

model = ChatOpenAI(
    model = settings.openai_model,
    api_key = settings.openai_api_key
)

model_with_tools = model.bind_tools(tools)

async def call_model(state: AgentState):
    response = await model_with_tools.ainvoke(
        state["messages"]
    )

    return {
        "messages": [response]
    }

def should_continue(state: AgentState):
    last_message = state["messages"][-1]

    if last_message.tool_calls:
        return "tools"

    return END

builder = StateGraph(AgentState)

builder.add_node(
    "agent",
    call_model
)

builder.add_node(
    "tools",
    ToolNode(tools)
)

builder.set_entry_point("agent")

builder.add_conditional_edges(
    "agent",
    should_continue,
    {
        "tools": "tools",
        END: END
    }
)

builder.add_edge(
    "tools",
    "agent",
)

graph = builder.compile()
