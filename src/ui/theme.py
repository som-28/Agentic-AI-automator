"""AURA visual theme for the Streamlit application."""
from __future__ import annotations

import streamlit as st


AURA_CSS = """
<style>
:root {
    --aura-paper: #f4efe6;
    --aura-paper-deep: #ebe3d6;
    --aura-surface: #fffdf8;
    --aura-ink: #17283f;
    --aura-ink-soft: #31435a;
    --aura-muted: #728093;
    --aura-line: #ded6c9;
    --aura-coral: #e66d51;
    --aura-coral-dark: #c9533d;
    --aura-teal: #16877e;
    --aura-gold: #c9943d;
    --aura-error: #b94e4e;
}

html, body, [class*="css"] {
    font-family: 'DM Sans', sans-serif;
}

.stApp {
    background-color: var(--aura-paper);
    background-image: linear-gradient(rgba(23, 40, 63, 0.035) 1px, transparent 1px), linear-gradient(90deg, rgba(23, 40, 63, 0.035) 1px, transparent 1px);
    background-size: 32px 32px;
    color: var(--aura-ink);
}

[data-testid="stHeader"] {
    background: transparent;
}

[data-testid="stSidebar"],
[data-testid="collapsedControl"],
[data-testid="stSidebarCollapsedControl"] {
    display: none !important;
}

.block-container {
    max-width: 1320px;
    padding: 2.25rem 3.5rem 4.5rem;
}

h1, h2, h3, [data-testid="stTab"],
.stButton > button, [data-testid="stFileUploaderDropzone"] button {
    font-family: 'Chakra Petch', sans-serif !important;
}

.aura-kicker {
    color: var(--aura-coral-dark);
    font-family: 'IBM Plex Mono', monospace;
    font-size: 0.7rem;
    font-weight: 500;
    letter-spacing: 0.14em;
    text-transform: uppercase;
}

.aura-title {
    color: var(--aura-ink);
    font-family: 'Chakra Petch', sans-serif;
    font-size: 3.5rem;
    font-weight: 700;
    letter-spacing: -0.045em;
    line-height: 1.05;
    margin: 0.35rem 0 0.55rem;
    max-width: 100%;
    overflow-wrap: anywhere;
}

.aura-subtitle {
    color: var(--aura-ink-soft);
    font-size: 1rem;
    line-height: 1.55;
    max-width: 720px;
    overflow-wrap: anywhere;
    margin-bottom: 2.25rem;
}

.aura-panel {
    background: var(--aura-surface);
    border: 1px solid var(--aura-line);
    border-radius: 14px;
    box-shadow: 0 12px 30px rgba(23, 40, 63, 0.06);
    padding: 1.2rem;
}

.aura-empty-state {
    background: var(--aura-surface);
    border: 1px solid var(--aura-line);
    border-radius: 14px;
    color: var(--aura-ink-soft);
    display: flex;
    flex-direction: column;
    gap: 0.35rem;
    height: 82px;
    margin-top: 28px;
    min-height: 82px;
    padding: 0.9rem 1.25rem;
}

.aura-empty-state strong {
    color: var(--aura-ink);
    font-family: 'Chakra Petch', sans-serif;
    font-size: 1rem;
}

.aura-empty-state span {
    color: var(--aura-muted);
    font-size: 0.86rem;
    overflow: hidden;
    text-overflow: ellipsis;
    white-space: nowrap;
}

.aura-metric {
    background: var(--aura-surface);
    border: 1px solid var(--aura-line);
    border-radius: 14px;
    box-shadow: 0 8px 20px rgba(23, 40, 63, 0.05);
    min-height: 100px;
    padding: 1.15rem 1.25rem;
    position: relative;
    overflow: hidden;
}

.aura-metric::before {
    background: var(--aura-coral);
    content: '';
    height: 4px;
    left: 0;
    position: absolute;
    right: 0;
    top: 0;
}

.aura-metric-label {
    color: var(--aura-muted);
    font-family: 'IBM Plex Mono', monospace;
    font-size: 0.67rem;
    letter-spacing: 0.08em;
    text-transform: uppercase;
}

.aura-metric-value {
    color: var(--aura-ink);
    font-family: 'Chakra Petch', sans-serif;
    font-size: 1.8rem;
    font-weight: 700;
    margin-top: 0.45rem;
}

.aura-event {
    align-items: baseline;
    border-bottom: 1px solid var(--aura-line);
    display: flex;
    gap: 0.8rem;
    padding: 0.75rem 0;
}

.aura-event:last-child { border-bottom: 0; }

.aura-event-type {
    color: var(--aura-teal);
    font-family: 'IBM Plex Mono', monospace;
    font-size: 0.68rem;
    min-width: 148px;
    text-transform: uppercase;
}

.aura-event-message {
    color: var(--aura-ink-soft);
    font-size: 0.88rem;
}

[data-testid="stTabs"] [role="tablist"] {
    border-bottom: 1px solid var(--aura-line);
    gap: 1.6rem;
}

[data-testid="stTab"] {
    color: var(--aura-ink-soft) !important;
    font-weight: 600;
    opacity: 1 !important;
    padding: 0.85rem 0 0.9rem;
}

[data-testid="stTab"] p {
    color: var(--aura-ink-soft) !important;
}

[data-testid="stTab"] * {
    color: var(--aura-ink-soft) !important;
    opacity: 1 !important;
}

[data-testid="stTab"][aria-selected="true"] {
    color: var(--aura-coral-dark) !important;
}

[data-testid="stTab"][aria-selected="true"] p {
    color: var(--aura-coral-dark) !important;
}

[data-testid="stTab"][aria-selected="true"] * {
    color: var(--aura-coral-dark) !important;
}

[data-testid="stTab"]:not([aria-selected="true"]),
[data-testid="stTab"]:not([aria-selected="true"]) * {
    color: var(--aura-ink-soft) !important;
    opacity: 1 !important;
    -webkit-text-fill-color: var(--aura-ink-soft) !important;
}

[data-testid="stTabs"] button[role="tab"]:after {
    background: var(--aura-coral);
    height: 3px;
}

[data-testid="stTextArea"] textarea,
[data-testid="stTextInput"] input {
    background: var(--aura-surface);
    border: 1px solid var(--aura-line);
    border-radius: 10px;
    color: var(--aura-ink);
    font-size: 0.95rem;
}

[data-testid="stTextArea"] textarea::placeholder,
[data-testid="stTextInput"] input::placeholder {
    color: var(--aura-muted) !important;
    opacity: 1 !important;
}

[data-testid="stWidgetLabel"] p,
[data-testid="stTextArea"] label,
[data-testid="stTextInput"] label {
    color: var(--aura-ink-soft) !important;
    font-weight: 600;
}

[data-testid="stTextArea"] textarea:focus,
[data-testid="stTextInput"] input:focus {
    border-color: var(--aura-coral);
    box-shadow: 0 0 0 1px var(--aura-coral);
}

[data-testid="stFileUploaderDropzone"] {
    background: var(--aura-surface);
    border: 1px dashed var(--aura-line);
    border-radius: 14px;
    padding: 1.25rem;
}

[data-testid="stFileUploaderDropzone"] * {
    color: var(--aura-ink-soft) !important;
}

[data-testid="stFileUploaderDropzone"] button {
    background: var(--aura-paper-deep);
    border: 1px solid var(--aura-line);
    color: var(--aura-ink);
}

[data-testid="stAlert"] {
    background: var(--aura-surface);
    border: 1px solid var(--aura-line);
    color: var(--aura-ink-soft);
}

[data-testid="stAlert"] p {
    color: var(--aura-ink-soft) !important;
}

.stButton > button {
    border: 1px solid var(--aura-line);
    border-radius: 9px;
    color: var(--aura-ink);
    font-weight: 600;
    height: 2.75rem;
    min-height: 2.75rem;
    padding: 0.55rem 1rem;
}

.stButton > button[kind="primary"] {
    background: var(--aura-coral);
    border-color: var(--aura-coral);
    color: #fffdf8;
    font-weight: 700;
}

.stButton > button[kind="primary"]:hover {
    background: var(--aura-coral-dark);
    border-color: var(--aura-coral-dark);
    color: #fffdf8;
}

[data-testid="stAlert"] {
    border-radius: 10px;
}

@media (max-width: 900px) {
    .block-container { padding: 1.75rem 1.25rem 4rem; }
    .aura-title { font-size: 2.35rem; }
    .aura-event { display: block; }
    .aura-event-type { display: block; margin-bottom: 0.3rem; }
}
</style>
"""


def apply_theme() -> None:
    st.markdown(
        """
        <style>
        @import url('https://fonts.googleapis.com/css2?family=Chakra+Petch:wght@500;600;700&family=DM+Sans:wght@400;500;600;700&family=IBM+Plex+Mono:wght@400;500&display=swap');
        </style>
        """,
        unsafe_allow_html=True,
    )
    st.markdown(AURA_CSS, unsafe_allow_html=True)
