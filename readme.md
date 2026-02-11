# NovaMind – Retail Risk Decision Agent

## Overview
NovaMind is an agentic AI system that evaluates retail transaction risk by
extracting linguistic signals, observing scam tactics, and reasoning over
uncertainty to recommend actions.

## Architecture


## How It Works
1. Transaction text is analyzed for linguistic risk signals.
2. A passive honeypot observes scam-like tactics.
3. Signals are aggregated into a risk score.
4. Amazon Nova (or fallback logic) explains the decision.
5. The system recommends an action.

## Why Agentic AI
The system observes, reasons, and adapts using feedback loops rather than
single-pass inference.

## Safety & Ethics
- No real users are interacted with.
- Honeypot is passive and non-deceptive.
- No automated enforcement actions are executed.

## Tech Stack
- Python
- Streamlit
- NLP (rule-based)
- Risk Scoring
- Amazon Nova (reasoning layer)
