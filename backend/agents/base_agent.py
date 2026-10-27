"""Shared base class for all WATT LINK specialist agents.

Every agent (battery, forecast, load, trading, fault, security) inherits from
``BaseAgent``.  The base class handles the common pipeline:

1. Pull recent decisions from the shared ``MemoryStore`` (learning context).
2. Build the user prompt with ``build_agent_user_prompt``.
3. Call the LLM via the shared ``LLMClient``.
4. Parse the completion into an ``AgentDecision`` with ``DecisionParser``.
5. Persist the decision to memory.
6. On any LLM / parsing failure, fall back to ``safe_fallback()`` so the
microgrid never stalls because a model endpoint is down.

Subclasses only need to set ``name`` and ``role`` and override
``analyze(context)`` (domain logic) and ``safe_fallback(context)``.
"""

from __future__ import annotations

import logging
from abc import ABC, abstractmethod
from typing import Any, Dict, Mapping, Optional

from ..llm import (
    AgentDecision,
    DecisionParser,
    DecisionParseError,
    LLMClient,
    MemoryStore,
    SYSTEM_PROMPT_AGENT,
    build_agent_user_prompt,
)

logger = logging.getLogger(__name__)


class BaseAgent(ABC):
    """Abstract base for every specialist agent.

    Parameters
    ----------
    llm_client
        Shared, provider-agnostic LLM client.
    memory
        Shared decision-history store.
    """

    #: Short agent name, e.g. ``"BatteryAgent"``.
    name: str = "BaseAgent"
    #: One-line responsibility description shown to the model.
    role: str = "Specialist agent."

    def __init__(
        self,
        *,
        llm_client: LLMClient,
        memory: MemoryStore,
    ) -> None:
        self.llm_client = llm_client
        self.memory = memory
        self.parser = DecisionParser()

    # ------------------------------------------------------------------ #
    # Public entry point
    # ------------------------------------------------------------------ #
    def run(self, context: Mapping[str, Any]) -> AgentDecision:
        """Execute the agent pipeline for one microgrid snapshot.

        Parameters
        ----------
        context
            A mapping that may contain:
            ``sensor_data``, ``battery_status``, ``market_context``,
            ``grid_context``.  Agents pick the keys they care about.

        Returns
        -------
        AgentDecision
            The structured decision (decision / reason / confidence /
            recommended_action).
        """
        # 1. Domain-specific pre-analysis (may enrich context).
        enriched = self.analyze(dict(context))

        # 2. Learning context: recent decisions for this agent.
        recent = self.memory.recent_as_context(self.name, limit=5)

        # 3. Build prompt.
        user_prompt = build_agent_user_prompt(
            agent_name=self.name,
            agent_role=self.role,
            sensor_data=enriched.get("sensor_data"),
            battery_status=enriched.get("battery_status"),
            market_context=enriched.get("market_context"),
            recent_memory=recent,
        )

        # 4. Call LLM and parse.
        try:
            raw = self.llm_client.complete(SYSTEM_PROMPT_AGENT, user_prompt)
            decision = self.parser.parse(raw)
        except (DecisionParseError, Exception) as exc:  # noqa: BLE001
            logger.warning("%s LLM/parse failed (%s) - using fallback", self.name, exc)
            decision = self.safe_fallback(enriched)

        # 5. Persist to memory for future learning.
        self.memory.add(
            agent_name=self.name,
            decision=decision.to_dict(),
            context={
                k: enriched.get(k)
                for k in ("sensor_data", "battery_status", "market_context")
                if k in enriched
            },
        )
        return decision

    # ------------------------------------------------------------------ #
    # Hooks for subclasses
    # ------------------------------------------------------------------ #
    @abstractmethod
    def analyze(self, context: Dict[str, Any]) -> Dict[str, Any]:
        """Domain-specific pre-processing.

        Override to compute derived metrics, validate ranges, or filter the
        context.  Must return the (possibly enriched) context mapping with the
        standard keys (``sensor_data``, ``battery_status``, ``market_context``).
        """

    def safe_fallback(self, context: Mapping[str, Any]) -> AgentDecision:
        """Return a conservative hold decision when the LLM is unavailable.

        Subclasses should override to provide a domain-specific safe state
        (e.g. stop charging, disconnect trading).
        """
        return AgentDecision(
            decision="HOLD",
            reason=f"{self.name} could not reach the LLM; defaulting to a safe hold.",
            confidence=0.0,
            recommended_action="No action taken; await next cycle.",
            raw={},
        )
