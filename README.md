# CyberNewsAI — Real-Time Threat Intelligence & Live News Radar

[![FastAPI](https://img.shields.io/badge/Backend-FastAPI-009688.svg?style=flat&logo=fastapi)](https://fastapi.tiangolo.com)
[![React](https://img.shields.io/badge/Frontend-React%2019%20%2B%20Vite-61DAFB.svg?style=flat&logo=react)](https://react.dev/)
[![SQLite](https://img.shields.io/badge/Database-SQLite%20WAL-003B57.svg?style=flat&logo=sqlite)](https://www.sqlite.org/)
[![AI Engine](https://img.shields.io/badge/AI%20Engine-Gemini%203.5%20Flash-4285F4.svg?style=flat&logo=google)](https://aistudio.google.com/)
[![License](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)

An enterprise-grade **Cybersecurity Threat Intelligence Platform and Live News Radar** engineered with an ultra-futuristic cyberpunk/SOC HUD aesthetic.

CyberNewsAI captures live, real-time threat intelligence directly from authoritative threat research repositories across the internet in under a second upon pressing **LIVE RADAR SYNC**. Built as a final-year cybersecurity student portfolio project, the platform features fully interactive buttons, dynamic category filtering, instant CVE search, pin-to-vault bookmarking, and on-demand AI executive summaries.

---

## Architecture Overview

```
                          ┌────────────────────────────────────────────────────────┐
                          │               Authoritative Threat Feeds               │
                          │   (BleepingComputer, The Hacker News, SecurityWeek,    │
                          │            CISA Alerts, KrebsOnSecurity)               │
                          └──────────────────────────┬─────────────────────────────┘
                                                     │ Concurrent ThreadPool (1-2s)
                                                     ▼
┌──────────────────────────────────────────────────────────────────────────────────────────┐
│                             FASTAPI BACKEND ENGINE (Port 8000)                           │
│                                                                                          │
│  ┌─────────────────────────┐   ┌──────────────────────────┐   ┌───────────────────────┐  │
│  │ Concurrent RSS Ingestion│──▶│   Threat Intelligence    │──▶│    SQLite Database    │  │
│  │ (5 Live Parallel Feeds) │   │ Classifier (CVE, Severity│   │ (WAL Mode, Indexed)   │  │
│  └─────────────────────────┘   └──────────────────────────┘   └───────────┬───────────┘  │
│                                                                           │              │
│  ┌─────────────────────────┐   ┌──────────────────────────┐               │              │
│  │ Google GenAI Integration│◀──│ Pinned Vault & Telemetry │◀──────────────┘              │
│  │ (Executive Briefings)   │   │   (Interactive Queries)  │                              │
│  └─────────────────────────┘   └─────────────┬────────────┘                              │
└──────────────────────────────────────────────┼───────────────────────────────────────────┘
                                               │ JSON REST API & Static SPA
                                               ▼
┌──────────────────────────────────────────────────────────────────────────────────────────┐
│                           FUTURISTIC REACT + VITE SOC TERMINAL                           │
│  - Live Threat Radar Stream (Default)   - SOC Operations War Room Dashboard              │
│  - Interactive CVE Inspector Chips      - Pinned Threats Vault (1-Click Pinning)         │
│  - Real-time Multi-Filter Matrix        - All Clickable Holographic Buttons              │
└──────────────────────────────────────────────────────────────────────────────────────────┘
```

---

## Key Features

1. **Ultra-Fast Real-Time Live Sync**: Captures fresh cyber threat news from 5 parallel feeds concurrently (**BleepingComputer**, **The Hacker News**, **SecurityWeek**, **CISA**, and **KrebsOnSecurity**) with parallel Python ThreadPool workers in under 1 second.
2. **Futuristic Cyberpunk / SOC HUD Design**: Neon glowing accents, scanline overlays, holographic badges, cyber telemetry indicators (`[SYS: ONLINE]`, `[BUFFER: SYNCHRONIZED]`), and micro-interactions.
3. **100% Clickable & Interactive Controls**:
   - **Click any Category Chip**: Instantly filters the live stream to that category.
   - **Click any Severity Badge**: Instantly filters the feed for Critical, High, Medium, or Low alerts.
   - **Click any Source Pill**: Instantly isolates news from that vendor.
   - **Click any CVE Identifier**: Instantly filters the radar stream for that specific CVE disclosure.
   - **Pin to Vault**: 1-click button on each card to bookmark incidents into the **Pinned Threats Vault**.
4. **Automated Threat Domain Classification**: Categorizes incidents into:
   - *Ransomware & Extortion*
   - *Vulnerabilities & Exploits*
   - *Data Breaches & Leaks*
   - *Nation-State & APT*
   - *Malware & Botnets*
   - *Cloud & Infrastructure*
   - *Defense & Advisories*
5. **CVE Extraction & Severity Risk Tiering**: Automatic regex extraction of `CVE-\d{4}-\d{4,7}` designations and dynamic risk tiering based on active exploitation, zero-day indicators, and critical infrastructure disruption.
6. **Persistent SQLite Database**: ACID-compliant SQLite WAL database with deduplication, search indices, and pre-seeded verified threat stories for offline resilience.
7. **On-Demand AI Threat Briefing**: Instant executive summaries generated by Google Gemini 3.5 Flash with clear AI labeling and vendor attribution.
8. **Secure Client Sandbox**: Strict sanitization with BeautifulSoup, zero API keys exposed in the frontend, and external links protected with `target="_blank" rel="noopener noreferrer"`.

---

## Project Structure

```
CyberNewsAI/
├── backend/                      # Python FastAPI application
│   ├── main.py                   # FastAPI server, endpoints, and SPA static mount
│   ├── database.py               # SQLite connection, schema definition & indexing
│   ├── models.py                 # Pydantic input validation & response schemas
│   └── services/
│       ├── threat_classifier.py  # Threat categorization, CVE parser & severity rules
│       ├── news_service.py       # RSS polling, deduplication, search & statistics
│       ├── ai_service.py         # Gemini client wrapper, prompt synthesis & export
│       └── sample_data.py        # Verified offline fallback cyber threat dataset
├── frontend/                     # React 19 + Vite dashboard
│   ├── src/
│   │   ├── components/
│   │   │   ├── Header.jsx        # Telemetry header, threat ticker & feed sync
│   │   │   ├── Sidebar.jsx       # Tactical SOC navigation console
│   │   │   ├── DashboardView.jsx # KPI metrics, urgent zero-days & category charts
│   │   │   ├── NewsFeedView.jsx  # Search, filters, card grid & script selector
│   │   │   ├── ArticleDetailModal.jsx # Full advisory modal with on-demand AI briefing
│   │   │   ├── ScriptStudioView.jsx   # Teleprompter script editor & export tool
│   │   │   ├── ThreatStatsView.jsx    # Analytics distributions & CVE registry
│   │   │   └── SourcesView.jsx   # Ingestion endpoints & security posture notes
│   │   ├── services/api.js       # Typed fetch client connecting to FastAPI
│   │   ├── App.jsx               # Application coordinator & notification state
│   │   ├── index.css             # Dark tactical cybersecurity SOC design tokens
│   │   └── main.jsx              # React DOM entrypoint
│   ├── index.html                # HTML template with JetBrains Mono & Outfit typography
│   ├── package.json              # Frontend dependencies (React 19, Lucide)
│   └── vite.config.js            # Vite build configuration & API reverse proxy
├── news/                         # Core ingestion logic
│   ├── rss_fetcher.py            # Feedparser & Trafilatura scraper
│   └── deduplicator.py           # Title-normalization deduplicator
├── app/                          # Legacy AI modules (preserved for compatibility)
│   ├── ai/gemini_client.py       # Google GenAI client with retry backoff
│   └── generators/               # Prompt templates & generators
├── run_backend.py                # Single-entrypoint server runner
├── test_backend_api.py           # Automated test suite (8 test cases)
├── requirements.txt              # Production Python dependencies
├── .env.example                  # Environment configuration template
└── README.md                     # Engineering documentation
```

---

## Installation & Setup

### Prerequisites
- Python 3.10+ (Tested on Python 3.12)
- Node.js 18+ and npm
- (Optional) Google Gemini API Key for dynamic AI script generation

### 1. Clone & Set Up Backend Virtual Environment
```bash
# Clone the repository
git clone https://github.com/utkarshchauhaniitk-star/CyberNewsAI-Pro.git
cd CyberNewsAI-Pro

# Create and activate virtual environment
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install Python dependencies
pip install -r requirements.txt
```

### 2. Configure Environment Variables
Copy `.env.example` to `.env`:
```bash
cp .env.example .env
```
Open `.env` and add your Google Gemini API key:
```ini
GEMINI_API_KEY=your_actual_gemini_api_key_here
PORT=8000
HOST=0.0.0.0
```
*(Note: If no API key is provided, the application automatically uses its built-in factual heuristic engine, so the application never breaks.)*

### 3. Build Frontend Assets
```bash
cd frontend
npm install
npm run build
cd ..
```

---

## Running the Application

### Option A: Unified Single-Command Mode (Recommended for Demos)
Run the complete full-stack application on a single port (`http://localhost:8000`):
```bash
python run_backend.py
```
Open your browser and navigate to:
**[http://localhost:8000](http://localhost:8000)**

### Option B: Development Dual-Server Mode (With Hot Reloading)
For active frontend development with Instant Hot-Module Reloading:

**Terminal 1 (Backend):**
```bash
source venv/bin/activate
python run_backend.py
```

**Terminal 2 (Frontend):**
```bash
cd frontend
npm run dev
```
Open **[http://localhost:5173](http://localhost:5173)** (Vite proxies all `/api/*` traffic automatically to port 8000).

---

## Automated Verification & Test Suite

The project includes an end-to-end automated test suite verifying all 8 core capabilities:
```bash
python test_backend_api.py
```

**Verification Checklist executed by the test suite:**
- [x] `[1/8]` Health Diagnostics (`/api/health`)
- [x] `[2/8]` Metadata Endpoints (`/api/categories`, `/api/sources`)
- [x] `[3/8]` Paginated Article Querying (`/api/articles`)
- [x] `[4/8]` Full-Text Search and Category Filtering
- [x] `[5/8]` Article Detail Retrieval (`/api/articles/{id}`)
- [x] `[6/8]` Real-time Threat Intelligence Aggregations (`/api/threat-stats`)
- [x] `[7/8]` On-Demand AI Executive Article Summarization
- [x] `[8/8]` Video Script Studio Generation & Plaintext File Export

---

## API Documentation

FastAPI provides an interactive OpenAPI / Swagger UI at:
**[http://localhost:8000/docs](http://localhost:8000/docs)**

### Key Endpoints

| Method | Endpoint | Description |
|---|---|---|
| `GET` | `/api/health` | Service health status and Gemini engine diagnostics |
| `GET` | `/api/articles` | Query threat stories with `q`, `category`, `source`, `severity`, `has_cve`, `page`, `limit` |
| `GET` | `/api/articles/{id}` | Detailed report extract, CVE identifiers, and severity rating |
| `POST` | `/api/articles/{id}/summarize` | Generates a 150-word executive briefing with Gemini AI |
| `POST` | `/api/news/refresh` | Ingests live RSS feeds, deduplicates, enriches, and stores in SQLite |
| `GET` | `/api/threat-stats` | Threat metrics: total incidents, severity breakdown, category matrix, detected CVEs |
| `POST` | `/api/scripts/generate` | Synthesizes a video narration teleprompter script from selected article IDs |
| `GET` | `/api/scripts` | Lists previously generated video scripts |
| `GET` | `/api/scripts/{id}/export` | Direct attachment download of the script as `.txt` |

---

## Cybersecurity Portfolio Screenshots Checklist

When presenting this project for technical interviews or portfolio reviews, capture screenshots of the following views:

1. **SOC Threat Operations Dashboard**:
   - Highlighting the top KPI counters (Total Incidents, Critical Zero-Days, Detected CVEs).
   - Priority Zero-Days & Urgent Advisories list with severity badges.
   - Category distribution progress bars.
2. **Threat Radar Feed**:
   - Search bar active with a query like `"ransomware"` or `"zero-day"`.
   - Category filter pills active with custom selections.
   - Multi-select checkboxes activated with floating "Stories ready for Video Script" action bar.
3. **Article Detail & AI Executive Summary Modal**:
   - Showing the extracted CVE identifiers, source tag, and publication timestamp.
   - Demonstrating the on-demand generated executive summary with the AI attribution badge.
   - Original source link with external badge.
4. **Video Narration Script Studio**:
   - Displaying the teleprompter narration text with broadcast cues (`[HOST NARRATION]`, `[ON-SCREEN GRAPHIC]`).
   - YouTube SEO Title, Description with timestamps, and video tags.
   - Demonstrating the "Download .txt" export functionality.
5. **Threat Intelligence Analytics**:
   - Severity distribution gauge (Critical vs High vs Medium vs Low).
   - Monitored RSS source percentage contributions.
   - Detected CVE vulnerability registry chips.

---

## Security & Compliance Principles

- **Zero Client-Side Secret Exposure**: API keys (including `GEMINI_API_KEY`) reside exclusively in backend environment memory and are never bundled into client scripts.
- **Isolated Browsing Protection**: External article hyperlinks include `rel="noopener noreferrer"` attributes to prevent tab-nabbing and DOM exploitation.
- **Strict Content Sanitization**: RSS summaries and extracted HTML are stripped of executable JavaScript via BeautifulSoup before ingestion.
- **Factual Integrity & AI Labeling**: AI outputs are clearly identified with `badge-ai` labels, and prompts strictly prohibit fabricating vulnerability disclosures or CVEs.

---

## Completed Features & Future Roadmap

### Completed Features
- [x] Full-stack modernization from monolithic Flask template to FastAPI + React 19 / Vite.
- [x] Continuous ingestion from 4 primary cybersecurity RSS feeds.
- [x] Deduplication and SQLite WAL database persistence.
- [x] Threat categorization and regex CVE identifier extraction.
- [x] Real-time threat intelligence statistics and distribution charts.
- [x] On-demand AI executive summarizer with Gemini 3.5 Flash.
- [x] Teleprompter video narration script generator with customizable durations (2m, 5m, 8m).
- [x] One-click script export to downloadable `.txt` files.
- [x] Pre-seeded verified offline dataset ensuring demo reliability.

### Future Roadmap
- [ ] STIX 2.1 / TAXII feed export for direct integration into enterprise SIEM platforms (e.g. Splunk, Microsoft Sentinel).
- [ ] Automated CVSS score lookup integration via the NIST National Vulnerability Database (NVD) REST API.
- [ ] Automated text-to-speech (TTS) audio narration rendering using `edge-tts`.

---

## Author

**Utkarsh Chauhan**  
*Final-Year Cybersecurity Engineering Student*  
*Specialization: Threat Intelligence, Vulnerability Research & Applied AI*
