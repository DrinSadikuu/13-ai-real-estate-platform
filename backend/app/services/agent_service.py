
from uuid import uuid4

from langchain_core.messages import HumanMessage
from langgraph.types import Command




class AgentService:
    def __init__(self,graph):
        self.graph = graph
    @staticmethod
    def get_pending_actions(state) -> list[dict]:
        for task in state.tasks:
            for interruption in task.interrupts:
                data = interruption.value

                if data.get("type") == "approval_required":
                    return data["pending_actions"]

        return []

    async def run(
        self,
        message: str,
        thread_id: str | None = None,
    ) -> dict:

        thread_id = thread_id or str(uuid4())

        config = {
            "configurable": {
                "thread_id": thread_id,
            }
        }

        state = await self.graph.aget_state(config)

        if self.get_pending_actions(state):
            raise ValueError(
                "This conversation has a pending action. "
                "Approve or reject it before sending another message."
            )

        result = await self.graph.ainvoke(
            {"messages": [HumanMessage(content=message)]},
            config=config,
        )

        state = await self.graph.aget_state(config)
        pending_actions = self.get_pending_actions(state)

        if pending_actions:
            return {
                "thread_id": thread_id,
                "status": "approval_required",
                "pending_actions": pending_actions,
                "response": "Approval is required before scheduling the viewing.",
            }

        return {
            "thread_id": thread_id,
            "status": "completed",
            "pending_actions": [],
            "response": result["messages"][-1].content,
        }

    async def decide(
        self,
        thread_id: str,
        approved: bool,
    ) -> dict:

        config = {
            "configurable": {
                "thread_id": thread_id,
            }
        }

        state = await self.graph.aget_state(config)

        if not self.get_pending_actions(state):
            raise ValueError("No pending approval found.")

        result = await self.graph.ainvoke(
            Command(resume=approved),
            config=config,
        )

        state = await self.graph.aget_state(config)
        pending_actions = self.get_pending_actions(state)

        if pending_actions:
            return {
                "thread_id": thread_id,
                "status": "approval_required",
                "pending_actions": pending_actions,
                "response": "Another action requires approval.",
            }

        return {
            "thread_id": thread_id,
            "status": "completed",
            "pending_actions": [],
            "response": result["messages"][-1].content,
        }

    async def approve(self, thread_id: str) -> dict:
        return await self.decide(thread_id, approved=True)

    async def reject(self, thread_id: str) -> dict:
        return await self.decide(thread_id, approved=False)
