"""Reusable presentation components for the AURA Streamlit UI."""
from __future__ import annotations

from typing import Iterable

import streamlit as st

from src.agent.models import TaskEvent


def render_page_header(kicker: str, title: str, subtitle: str) -> None:
    st.markdown(f'<div class="aura-kicker">{kicker}</div>', unsafe_allow_html=True)
    st.markdown(f'<div class="aura-title">{title}</div>', unsafe_allow_html=True)
    st.markdown(f'<div class="aura-subtitle">{subtitle}</div>', unsafe_allow_html=True)


def render_metric(label: str, value: str) -> None:
    st.markdown(
        f"""
        <div class="aura-metric">
            <div class="aura-metric-label">{label}</div>
            <div class="aura-metric-value">{value}</div>
        </div>
        """,
        unsafe_allow_html=True,
    )


def render_empty_state(title: str, message: str) -> None:
    st.markdown(
        f"""
        <div class="aura-empty-state">
            <strong>{title}</strong>
            <span>{message}</span>
        </div>
        """,
        unsafe_allow_html=True,
    )


def render_event_stream(events: Iterable[TaskEvent]) -> None:
    event_list = list(events)
    if not event_list:
        st.info("No execution events yet.")
        return

    rows = []
    for event in event_list:
        if isinstance(event, dict):
            raw_timestamp = event.get("timestamp", "")
            timestamp = raw_timestamp[11:19] if isinstance(raw_timestamp, str) else ""
            event_type = event.get("event_type", "event")
            message = event.get("message", "")
        else:
            timestamp = event.timestamp.strftime("%H:%M:%S")
            event_type = event.event_type
            message = event.message
        rows.append(
            f'<div class="aura-event"><span class="aura-event-type">{timestamp} {event_type}</span>'
            f'<span class="aura-event-message">{message}</span></div>'
        )
    st.markdown(f'<div class="aura-panel">{"".join(rows)}</div>', unsafe_allow_html=True)
