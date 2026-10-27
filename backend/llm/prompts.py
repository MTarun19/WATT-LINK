"""Prompt templates for the WATT LINK Agentic AI layer.

Two system prompts are defined:

* ``SYSTEM_PROMPT_AGENT``   - shared by every specialist agent (battery,
  forecast, load, trading, fault, security).  It locks the model into returning
  a strict JSON object so ``parser.DecisionParser`` can parse it reliably.
* ``SYSTEM_PROMPT_MANAGER`` - used by the AI Manager to fuse the per-agent
  decisions into a single, final microgrid decision.

Two builder helpers assemble the *user* message from live context:

* ``build_agent_user_prompt``   - agent name, role, live sensor data, battery
  status and recent memory.
* ``build_manager_user_prompt`` - all sub-agent decisions + grid context.

Keeping every prompt in one module makes it easy to tune wording without
touching agent logic.
"""

from __future__ import annotations

import json
from typing import Any, Dict, List, Mapping, Optional

# ---------------------------------------------------------------------- #
# Shared JSON output contract (must stay in sync with parser.py)
# ---------------------------------------------------------------------- #
DECISION_JSON_SCHEMA_HINT = (
    "Respond with ONLY a single JSON object (no markdown, no prose) using "
    "exactly these keys:\n"
    "{\n"
    '  "decision": "short label, e.g. CHARGE_BATTERY",\n'
    '  "reason": "1-3 sentence explanation of why",\n'
    '  "confidence": <float 0.0-1.0>,\n'
    '  "recommended_action": "concrete next step for the microgrid operator",\n'
    '  "metrics": { ... optional numeric evidence ... }\n'
    "}"
)

# ---------------------------------------------------------------------- #
# System prompts
# ---------------------------------------------------------------------- #
SYSTEM_PROMPT_AGENT = (
    "You are a specialist AI agent inside WATT LINK, a smart microgrid and "
    "peer-to-peer energy trading platform. You monitor live IoT sensor data "
    "from ESP32 devices and reason about one narrow domain.\n\n"
    "Rules:\n"
    "1. Base every conclusion on the data you are given; never invent sensor "
    "readings.\n"
    "2. If a required value is missing or null, say so and lower your "
    "confidence accordingly.\n"
    "3. Be concise and operational - this output drives real relay control "
    "and trading decisions.\n"
    "4. Learn from the recent decisions you are shown: avoid repeating failed "
    "actions and prefer actions that worked before in similar conditions.\n"
    f"5. {DECISION_JSON_SCHEMA_HINT}"
)

SYSTEM_PROMPT_MANAGER = (
    "You are the AI Manager of WATT LINK, the central brain coordinating all "
    "specialist agents (battery, forecast, load, trading, fault, security).\n\n"
    "Your job:\n"
    "1. Read each agent's structured decision and weigh them together.\n"
    "2. Safety first: any FAULT or SECURITY alert overrides trading gains.\n"
    "3. Balance battery health, solar forecast, demand forecast and trading "
    "opportunity into ONE coherent plan.\n"
    "4. If agents disagree, explain the trade-off and pick the safest, most "
    "efficient option.\n"
    "5. Learn from the recent manager decisions you are shown.\n"
    f"6. {DECISION_JSON_SCHEMA_HINT}"
)

# ---------------------------------------------------------------------- #
# User-prompt builders
# ---------------------------------------------------------------------- #

def _json_block(label: str, data: Any) -> str:
    """Render ``data`` as a labelled, indented JSON block (or ``null``)."""
    if data is None:
        return f"{label}: null"
    try:
        rendered = json.dumps(data, indent=2, default=str, sort_keys=True)
    except (TypeError, ValueError):
        rendered = str(data)
    return f"{label}:\n{rendered}"


def build_agent_user_prompt(
    *,
    agent_name: str,
    agent_role: str,
    sensor_data: Optional[Mapping[str, Any]] = None,
    battery_status: Optional[Mapping[str, Any]] = None,
    market_context: Optional[Mapping[str, Any]] = None,
    recent_memory: Optional[List[Mapping[str, Any]]] = None,
) -> str:
    """Build the user message for a specialist agent.

    Parameters
    ----------
    agent_name
        e.g. ``"BatteryAgent"``.
    agent_role
        One-line description of the agent's responsibility.
    sensor_data
        Latest ESP32 sensor readings (voltage, current, irradiance, ...).
    battery_status
        State of charge, temperature, health, charge/discharge rate, ...
    market_context
        Current energy price, peer offers, grid tariff (optional).
    recent_memory
        Previous decisions for this agent, newest first (used for learning).
    """
    parts: List[str] = [
        f"Agent: {agent_name}",
        f"Role: {agent_role}",
        _json_block("Live sensor data", sensor_data),
        _json_block("Battery status", battery_status),
        _json_block("Market context", market_context),
    ]
    if recent_memory:
        # Keep the context window small: cap at 5 recent decisions.
        trimmed = list(recent_memory[:5])
        parts.append(_json_block("Recent decisions (newest first)", trimmed))
    else:
        parts.append("Recent decisions: none yet")
    parts.append(
        "Analyse the data for your domain and return the JSON decision now."
    )
    return "\n\n".join(parts)


def build_manager_user_prompt(
    *,
    agent_decisions: Mapping[str, Mapping[str, Any]],
    grid_context: Optional[Mapping[str, Any]] = None,
    recent_memory: Optional[List[Mapping[str, Any]]] = None,
) -> str:
    """Build the user message for the AI Manager.

    Parameters
    ----------
    agent_decisions
        Mapping of ``agent_name -> decision dict`` produced by the specialists.
    grid_context
        Optional overall microgrid snapshot (total load, total generation,
        grid connection state, relay states, ...).
    recent_memory
        Previous manager decisions, newest first.
    """
    parts: List[str] = [
        _json_block("Specialist agent decisions", dict(agent_decisions)),
        _json_block("Grid context", grid_context),
    ]
    if recent_memory:
        trimmed = list(recent_memory[:5])
        parts.append(_json_block("Recent manager decisions (newest first)", trimmed))
    else:
        parts.append("Recent manager decisions: none yet")
    parts.append(
        "Synthesise the agent decisions into one final WATT LINK decision and "
        "return the JSON now."
    )
    return "\n\n".join(parts)
