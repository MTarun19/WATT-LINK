"""Decision memory for the WATT LINK Agentic AI layer.

``MemoryStore`` keeps a bounded, in-memory history of every decision made by
each specialist agent and by the AI Manager.  It also optionally mirrors each
record to the existing WATT LINK PostgreSQL database via a pluggable
``db_sink`` callback, so persistence is decoupled from the specific SQLAlchemy
models already in the project.

The store powers the "learn from previous decisions" requirement in two ways:

1. ``recent()`` returns the newest decisions for an agent so they can be
   injected into the next prompt (in-context learning).
2. ``record_outcome()`` closes the feedback loop by tagging a past decision as
   successful or not, which future prompts can use to avoid repeating failed
   actions.
"""

from __future__ import annotations

import logging
import threading
import time
import uuid
from dataclasses import dataclass, field
from typing import Any, Callable, Dict, List, Optional

logger = logging.getLogger(__name__)

# Default cap on how many records we keep per agent in memory.
DEFAULT_MAX_PER_AGENT = 200


@dataclass
class MemoryRecord:
    """A single stored AI decision.

    Attributes
    ----------
    id
        Unique identifier (used to attach outcomes later).
    agent_name
        ``"BatteryAgent"``, ``"AIManager"``, ...
    decision
        The structured ``AgentDecision`` payload (as a plain dict).
    context
        Snapshot of the sensor / grid data the decision was based on.
    timestamp
        Unix epoch seconds.
    outcome
        Optional feedback: ``True`` = success, ``False`` = failure, ``None`` =
        not yet evaluated.
    outcome_notes
        Optional human- or system-supplied notes about the outcome.
    """

    id: str
    agent_name: str
    decision: Dict[str, Any]
    context: Dict[str, Any] = field(default_factory=dict)
    timestamp: float = field(default_factory=time.time)
    outcome: Optional[bool] = None
    outcome_notes: Optional[str] = None

    def to_dict(self) -> Dict[str, Any]:
        return {
            "id": self.id,
            "agent_name": self.agent_name,
            "decision": self.decision,
            "context": self.context,
            "timestamp": self.timestamp,
            "outcome": self.outcome,
            "outcome_notes": self.outcome_notes,
        }


# Type of the optional database persistence callback.
DbSink = Callable[[MemoryRecord], None]


class MemoryStore:
    """Thread-safe, bounded decision-history store.

    Parameters
    ----------
    db_sink
        Optional callback invoked with every ``MemoryRecord`` right after it
        is stored in memory.  Use this to persist into your existing
        SQLAlchemy session, e.g.::

            MemoryStore(db_sink=lambda r: db_session.add(AIDecision(**r.to_dict())))
    max_per_agent
        How many records to keep in memory per agent (ring buffer).
    """

    def __init__(
        self,
        *,
        db_sink: Optional[DbSink] = None,
        max_per_agent: int = DEFAULT_MAX_PER_AGENT,
    ) -> None:
        self._db_sink = db_sink
        self._max = max_per_agent
        self._records: Dict[str, List[MemoryRecord]] = {}
        self._lock = threading.Lock()

    # ------------------------------------------------------------------ #
    # Writing
    # ------------------------------------------------------------------ #
    def add(
        self,
        agent_name: str,
        decision: Dict[str, Any],
        context: Optional[Dict[str, Any]] = None,
    ) -> MemoryRecord:
        """Store a new decision and return the created ``MemoryRecord``."""
        record = MemoryRecord(
            id=uuid.uuid4().hex,
            agent_name=agent_name,
            decision=dict(decision),
            context=dict(context or {}),
        )
        with self._lock:
            bucket = self._records.setdefault(agent_name, [])
            bucket.append(record)
            if len(bucket) > self._max:
                # Drop oldest in-place.
                del bucket[: len(bucket) - self._max]
        self._persist(record)
        return record

    def record_outcome(
        self,
        record_id: str,
        success: bool,
        notes: Optional[str] = None,
    ) -> bool:
        """Tag a previously stored decision as successful or not.

        Returns ``True`` if the record was found and updated.
        """
        with self._lock:
            for bucket in self._records.values():
                for rec in bucket:
                    if rec.id == record_id:
                        rec.outcome = success
                        rec.outcome_notes = notes
                        self._persist(rec)
                        return True
        logger.warning("record_outcome: record %s not found", record_id)
        return False

    # ------------------------------------------------------------------ #
    # Reading
    # ------------------------------------------------------------------ #
    def recent(
        self,
        agent_name: str,
        limit: int = 5,
        only_successful: Optional[bool] = None,
    ) -> List[MemoryRecord]:
        """Return the newest records for ``agent_name`` (newest first).

        Parameters
        ----------
        only_successful
            If ``True`` only return records tagged ``outcome=True``; if
            ``False`` only failed ones; ``None`` returns all.
        """
        with self._lock:
            bucket = list(self._records.get(agent_name, []))
        bucket.reverse()  # newest first
        if only_successful is True:
            bucket = [r for r in bucket if r.outcome is True]
        elif only_successful is False:
            bucket = [r for r in bucket if r.outcome is False]
        return bucket[:limit]

    def recent_as_context(
        self,
        agent_name: str,
        limit: int = 5,
    ) -> List[Dict[str, Any]]:
        """Return recent decisions as plain dicts ready for prompt injection."""
        records = self.recent(agent_name, limit=limit)
        return [self._record_to_prompt_dict(r) for r in records]

    def all_agents(self) -> List[str]:
        """Return the list of agent names that have at least one record."""
        with self._lock:
            return list(self._records.keys())

    def clear(self, agent_name: Optional[str] = None) -> None:
        """Clear memory for one agent, or all agents if ``None``."""
        with self._lock:
            if agent_name is None:
                self._records.clear()
            else:
                self._records.pop(agent_name, None)

    # ------------------------------------------------------------------ #
    # Internal
    # ------------------------------------------------------------------ #
    @staticmethod
    def _record_to_prompt_dict(rec: MemoryRecord) -> Dict[str, Any]:
        """Compact a record for prompt injection (no huge context blobs)."""
        return {
            "decision": rec.decision.get("decision"),
            "reason": rec.decision.get("reason"),
            "confidence": rec.decision.get("confidence"),
            "recommended_action": rec.decision.get("recommended_action"),
            "outcome": rec.outcome,
            "age_seconds": round(time.time() - rec.timestamp, 1),
        }

    def _persist(self, record: MemoryRecord) -> None:
        if self._db_sink is None:
            return
        try:
            self._db_sink(record)
        except Exception:  # noqa: BLE001 - persistence must never break AI
            logger.exception("db_sink failed for record %s", record.id)
