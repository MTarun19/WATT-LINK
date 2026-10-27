"""Parser for structured LLM decisions in WATT LINK.

The Agentic AI layer requires every model response to be a JSON object with at
least:

* ``decision``            - short label (e.g. ``"CHARGE_BATTERY"``)
* ``reason``              - human-readable explanation
* ``confidence``          - float in [0.0, 1.0]
* ``recommended_action``  - concrete next step

``DecisionParser`` extracts that object from a raw completion (tolerating
markdown fences and surrounding prose), validates it, and returns an
``AgentDecision`` dataclass.  On failure it raises ``DecisionParseError``.
"""

from __future__ import annotations

import json
import re
from dataclasses import asdict, dataclass, field
from typing import Any, Dict, Mapping, Optional

# Keys that must be present in every decision object.
_REQUIRED_KEYS = ("decision", "reason", "confidence", "recommended_action")

# Regex that finds the first {...} block, tolerant of nested braces.
_JSON_OBJECT_RE = re.compile(r"\{.*\}", re.DOTALL)
# Matches a ```json ... ``` or ``` ... ``` fenced block.
_FENCE_RE = re.compile(r"```(?:json)?\s*(.*?)```", re.DOTALL | re.IGNORECASE)


class DecisionParseError(ValueError):
    """Raised when an LLM completion cannot be parsed into a decision."""


@dataclass
class AgentDecision:
    """Canonical structured decision returned by every agent and the manager.

    Attributes
    ----------
    decision
        Short label, e.g. ``"CHARGE_BATTERY"`` or ``"HOLD"``.
    reason
        1-3 sentence explanation of the reasoning.
    confidence
        Float in [0.0, 1.0].
    recommended_action
        Concrete next step for the microgrid operator / relay controller.
    metrics
        Optional dictionary of numeric evidence (soc, price, predicted_kw, ...).
    raw
        The full parsed JSON object, kept for debugging / persistence.
    """

    decision: str
    reason: str
    confidence: float
    recommended_action: str
    metrics: Dict[str, Any] = field(default_factory=dict)
    raw: Dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        """Serialise to a plain dict suitable for JSON persistence."""
        return {
            "decision": self.decision,
            "reason": self.reason,
            "confidence": self.confidence,
            "recommended_action": self.recommended_action,
            "metrics": self.metrics,
        }

    def to_full_dict(self) -> Dict[str, Any]:
        """Like ``to_dict`` but also includes the raw payload."""
        out = self.to_dict()
        out["raw"] = self.raw
        return out


class DecisionParser:
    """Parse raw LLM text completions into ``AgentDecision`` objects."""

    def parse(self, text: str) -> AgentDecision:
        """Parse ``text`` into an ``AgentDecision``.

        Raises
        ------
        DecisionParseError
            If no JSON object can be found or required keys are missing / wrong
            type.
        """
        payload = self._extract_json(text)
        if payload is None:
            raise DecisionParseError(f"No JSON object found in completion: {text[:200]!r}")
        return self._build_decision(payload)

    # ------------------------------------------------------------------ #
    # Internal helpers
    # ------------------------------------------------------------------ #
    @staticmethod
    def _extract_json(text: str) -> Optional[Dict[str, Any]]:
        """Pull the first JSON object out of ``text``.

        Handles three common cases:
        1. Pure JSON.
        2. JSON wrapped in ```json ... ``` fences.
        3. JSON embedded in surrounding prose.
        """
        if not text or not text.strip():
            return None

        # 1. Try a direct parse first (fast path).
        try:
            loaded = json.loads(text)
            if isinstance(loaded, dict):
                return loaded
        except json.JSONDecodeError:
            pass

        # 2. Look inside fenced blocks.
        fence_match = _FENCE_RE.search(text)
        if fence_match:
            candidate = fence_match.group(1).strip()
            try:
                loaded = json.loads(candidate)
                if isinstance(loaded, dict):
                    return loaded
            except json.JSONDecodeError:
                pass

        # 3. Greedy match for the first {...} block (handles nested braces
        #    because the regex is DOTALL and ends at the *last* closing brace).
        obj_match = _JSON_OBJECT_RE.search(text)
        if obj_match:
            candidate = obj_match.group(0)
            try:
                loaded = json.loads(candidate)
                if isinstance(loaded, dict):
                    return loaded
            except json.JSONDecodeError:
                # Try a balanced-brace scan as a last resort.
                balanced = _balanced_braces(text)
                if balanced is not None:
                    try:
                        loaded = json.loads(balanced)
                        if isinstance(loaded, dict):
                            return loaded
                    except json.JSONDecodeError:
                        pass
        return None

    @staticmethod
    def _build_decision(payload: Mapping[str, Any]) -> AgentDecision:
        missing = [k for k in _REQUIRED_KEYS if k not in payload]
        if missing:
            raise DecisionParseError(
                f"Decision JSON missing required keys: {', '.join(missing)}"
            )

        decision = str(payload["decision"]).strip()
        reason = str(payload["reason"]).strip()
        recommended_action = str(payload["recommended_action"]).strip()
        if not decision or not reason or not recommended_action:
            raise DecisionParseError("Decision JSON has empty required fields.")

        confidence = _coerce_confidence(payload["confidence"])

        metrics = payload.get("metrics", {})
        if not isinstance(metrics, dict):
            metrics = {"value": metrics}

        raw = dict(payload)
        return AgentDecision(
            decision=decision,
            reason=reason,
            confidence=confidence,
            recommended_action=recommended_action,
            metrics=metrics,
            raw=raw,
        )


# ---------------------------------------------------------------------- #
# Module-level helpers
# ---------------------------------------------------------------------- #
def _coerce_confidence(value: Any) -> float:
    """Coerce ``value`` to a float clamped to [0.0, 1.0]."""
    try:
        conf = float(value)
    except (TypeError, ValueError) as exc:
        raise DecisionParseError(f"confidence is not numeric: {value!r}") from exc
    if conf < 0.0:
        return 0.0
    if conf > 1.0:
        # Accept 0-100 style and normalise.
        if conf > 1.5:
            return round(conf / 100.0, 4)
        return 1.0
    return round(conf, 4)


def _balanced_braces(text: str) -> Optional[str]:
    """Return the substring of the first balanced ``{...}`` block, or None."""
    start = text.find("{")
    if start == -1:
        return None
    depth = 0
    in_string = False
    escape = False
    for i in range(start, len(text)):
        ch = text[i]
        if escape:
            escape = False
            continue
        if ch == "\\":
            escape = True
            continue
        if ch == '"':
            in_string = not in_string
            continue
        if in_string:
            continue
        if ch == "{":
            depth += 1
        elif ch == "}":
            depth -= 1
            if depth == 0:
                return text[start : i + 1]
    return None
