# Prism NVO — Interactive Stock Pitch Dashboard

> **Built for the Perplexity Stock Pitch Competition**
> A comprehensive, AI-powered investment research platform for **Novo Nordisk (NVO)**, featuring live market data, multi-dimensional analysis, and an embedded AI analyst named Prism.

---

## Overview

Prism NVO is a single-page investment research dashboard that presents a long thesis on Novo Nordisk (NVO: NYSE / NOVO B: CPH). It combines live stock data, proprietary scoring, financial modeling, and an AI chatbot into one polished interface — making institutional-grade analysis accessible to both professional investors and general audiences.

The dashboard was built entirely with vanilla React (no build step required) and served by a lightweight Python backend that proxies external API calls to avoid CORS restrictions.

---

## Investment Thesis

The core pitch centers on three converging catalysts:

1. **Compounding Crackdown** — A regulatory crackdown on unauthorized GLP-1 compounders is expected to recover $3–4B in lost revenue that is currently unmodeled by the Street.
2. **Oral Wegovy Launch** — 170,000 patients enrolled in the oral semaglutide program in month one alone, signaling massive commercial momentum.
3. **Extreme Valuation Discount** — NVO trades at ~7.6x EV/EBITDA vs. a peer median of ~13.5x — a ~45% discount despite 48% EBITDA margins and $46.8B in revenue — with pipeline rNPV of $23.38/share priced at effectively zero by the market.

**Prism Score: 6.1 / 10 — BUY**

| Dimension | Weight | Score |
|---|---|---|
| Fundamental | 40% | 7.5 |
| Technical | 20% | 4.0 |
| Intelligence | 25% | 4.5 |
| Governance | 15% | 6.5 |

---

## Features

### Live Market Data
- Real-time NVO price feed via Yahoo Finance (proxied server-side)
- Live USD/DKK currency conversion via ExchangeRate API
- Price history charting across 1W, 1M, 3M, 6M, 1Y, and 3Y ranges
- Animated SVG price charts with crosshair interaction

### Prism Composite Score Gauge
- Animated multi-arc SVG gauge showing weighted scores across four dimensions
- Scores update on load with smooth cubic-bezier transitions
- Legend with per-dimension breakdown and color-coded performance indicators

### Financial Analysis
- Income statement, balance sheet, and cash flow data tables
- Revenue and EBITDA trend charts
- Segment revenue breakdown (Diabetes & Obesity vs. Rare Disease)
- Peer comparison table with EV/EBITDA and P/E benchmarking

### DCF Scenario Modeler
- Interactive sliders for revenue growth, EBITDA margin, exit multiple, and discount rate
- Bull / Base / Bear scenario presets
- Real-time implied price and upside calculation

### Technical Analysis
- SVG price chart with 52-week high/low range indicator
- RSI, MACD, and volume indicators displayed as metric cards
- Analyst consensus summary (Hold, Avg. Target: $66)
- Support/resistance levels with explanation tooltips

### News Intelligence
- News feed sourced from Finnhub, filtered to NVO
- Headlines displayed with source, date, and summary
- Sentiment-tagged news items (bullish / bearish / neutral)

### Governance & Leadership
- Board composition breakdown with gender and independence metrics
- Animated board diversity dot chart
- Executive leadership profiles with tenure and compensation context

### Bear / Bull Rebuttal Cards
- Pre-built objection/rebuttal pairs addressing the most common bear cases (CagriSema miss, compounding risk, pipeline concerns)
- Color-coded cards with expandable detail

### Catalyst Timeline
- Upcoming catalysts ranked by impact, with date and category labels

---

## Getting Started

### Prerequisites

- Python 3.8+
- An Anthropic API key (for the Prism AI assistant)
- No Node.js or build step required

### Installation

```bash
# Clone or download the repository
git clone <repo-url>
cd prism-nvo

# Install the Anthropic Python SDK
pip install anthropic

# Set your API key
export ANTHROPIC_API_KEY=your_api_key_here
```

### Running the App

```bash
python server.py
```

Then open your browser and navigate to:

```
http://localhost:5000
```

The server will log API requests to the terminal. The dashboard is fully functional without the Anthropic API key — the Prism chat assistant will display an unavailability message instead.

---

## API Integrations

| Endpoint | External Service | Purpose |
|---|---|---|
| `GET /api/yahoo/{params}` | Yahoo Finance v8 | Live price, OHLCV history |
| `GET /api/fx` | ExchangeRate API | USD/DKK rate for Copenhagen listing parity |
| `GET /api/news` | Finnhub | Recent NVO news headlines |
| `POST /api/chat` | Anthropic Claude | Prism AI analyst responses |

All third-party calls are made server-side with SSL verification handled gracefully for restrictive environments. Fallback static data is baked into the frontend so the dashboard renders correctly even if live data is unavailable.

---

## AI Assistant: Ask Prism

**Prism** is an embedded AI analyst powered by the Anthropic Claude API (`claude-sonnet-4-6`). It is accessible via the floating chat button in the bottom-right corner of the screen.

Prism is context-aware of the NVO investment thesis and responds in two modes:

- **Expert Mode** — Responds with financial terminology, precise metrics, and data-driven reasoning suitable for investment professionals.
- **Plain English Mode** — Translates the same analysis into simple, jargon-free language for general audiences.

### Example Prompts

- "What is the bear case on NVO?"
- "Explain the compounding crackdown in simple terms"
- "How does the DCF model hold up if margins compress?"
- "What catalysts should I watch for next quarter?"

---

## Dashboard Sections

| Section | ID | Description |
|---|---|---|
| Overview | `section-1` | Hero thesis, Prism Gauge, price chart, bear/bull rebuttals, catalysts |
| Financial Analysis | `section-2` | P&L, balance sheet, cash flow, peer comp, DCF modeler |
| Technical Analysis | `section-3` | Price chart, RSI/MACD, analyst consensus, support/resistance |
| News Intelligence | `section-4` | Finnhub-sourced headlines, sentiment tagging |
| Governance & Leadership | `section-5` | Board composition, executive profiles |

Navigation is handled by a sticky tab bar. Sections support smooth scroll with a "Back to Top" button fixed to the lower-left corner.

---

## Accessibility Modes

The dashboard supports two content modes, toggled via a switch in the top navigation bar:

| Mode | Label | Audience |
|---|---|---|
| Expert | "Expert" | Finance professionals, analysts |
| Plain English | "Plain English" | General public, non-finance users |

In Plain English mode, all financial terminology is replaced with simple explanations. For example, "EV/EBITDA" becomes a description of how cheap the stock is relative to its earnings power, and section labels shift from "Fundamental" to "Business".

---

## Project Structure

```
prism-nvo/
├── index.html      # Full React application (single-file, no build step)
└── server.py       # Python HTTP server + API proxy + Claude integration
```

The entire frontend is self-contained in `index.html` using Babel standalone for JSX transpilation in-browser. This means zero build tooling is required — the app runs directly from the file system via the Python server.

---

## Built With

- **Perplexity Computer** — Claude Sonnet and Opus

---

## Disclaimer

This dashboard is built for the **Perplexity Stock Pitch Competition** and is intended for educational and demonstration purposes only. It does not constitute financial advice. All data, scores, and analysis are provided without warranty. Past performance is not indicative of future results.

---

*Prism NVO — Built with Perplexity Computer*
