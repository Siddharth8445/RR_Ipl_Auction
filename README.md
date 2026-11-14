# Rajasthan Royals | IPL 2027 Auction Intelligence

A data-driven scouting and recruitment strategy dashboard for **Rajasthan Royals ahead of the IPL 2027 auction**. The project analyses historical IPL performance from **2022–2026** and presents role gaps, pressure-performance evidence, candidate comparisons, and recruitment priorities through an interactive Streamlit application.

<p align="center">
  <a href="https://rr-ipl-auction-intelligence.streamlit.app/">
    <img src="https://img.shields.io/badge/Live%20Dashboard-Open%20App-EC3F8B?style=for-the-badge&logo=streamlit&logoColor=white" alt="Open live dashboard">
  </a>
  <img src="https://img.shields.io/badge/Analysis%20Window-2022--2026-102344?style=for-the-badge" alt="Analysis window 2022 to 2026">
  <img src="https://img.shields.io/badge/Focus-IPL%202027-0B1B38?style=for-the-badge" alt="IPL 2027">
</p>

> **Important:** This is a historical-data scouting and decision-support project, not a live auction feed. Player retention, auction eligibility, and availability for IPL 2027 have not been independently confirmed. Historical squad records must not be interpreted as a confirmed 2027 roster.

---

## Table of Contents

- [Project Overview](#project-overview)
- [Live Application](#live-application)
- [Key Features](#key-features)
- [Dashboard Modules](#dashboard-modules)
- [Data and Analysis](#data-and-analysis)
- [Repository Structure](#repository-structure)
- [Technology Stack](#technology-stack)
- [Run Locally](#run-locally)
- [Deployment](#deployment)
- [Analytical Notes and Limitations](#analytical-notes-and-limitations)
- [Future Improvements](#future-improvements)

---

## Project Overview

Auction planning is not simply about selecting the players with the highest aggregate statistics. Teams need to identify **role-specific requirements**, assess performance under pressure, understand squad composition, and distinguish a statistical signal from a practical recruitment recommendation.

This project builds an evidence-led scouting workspace for Rajasthan Royals. It uses historical IPL data from 2022 to 2026 to examine:

- Batting performance in pressure situations.
- Opening and middle-order candidate pools.
- Bowling performance across match phases.
- Historical squad composition and role coverage.
- Recruitment gaps and role-level priorities.

The dashboard is designed to support scouting discussions and structured decision-making. It does not predict auction prices, guarantee future performance, or confirm player availability.

## Live Application

**[Open RR Auction Intelligence](https://rr-ipl-auction-intelligence.streamlit.app/)**

The public dashboard is deployed using Streamlit Community Cloud.

## Key Features

- **Role-gap assessment:** Reviews recruitment needs across opening batting, top order, middle order/finishing, powerplay bowling, middle-over bowling, and death bowling.
- **Pressure-performance analysis:** Compares batting evidence in defined pressure situations.
- **Opening analysis:** Displays the opening-role conclusion, combined candidate ranking, and player-level evidence.
- **Middle-order recruitment analysis:** Compares qualified candidates using a weighted, relative scoring framework.
- **Bowling evidence:** Organises historical bowling evidence by match phase.
- **Historical squad audit:** Reviews the 2026 Rajasthan Royals squad baseline and maps players to historical role categories.
- **Methodology and caveats:** Makes key definitions, assumptions, and data limitations visible within the application.
- **CSV exports:** Provides downloadable analysis tables from relevant dashboard sections.

## Dashboard Modules

| Module | Purpose |
|---|---|
| **Auction Command Centre** | Executive recruitment recommendation, role-priority overview, key indicators, and middle-order targets. |
| **Squad Matrix** | Historical Rajasthan Royals squad audit, role distribution, and 2027 verification status. |
| **Opening Analysis** | Opening-role conclusion, combined candidate ranking, and player-level batting evidence. |
| **Middle-Order Lab** | Candidate comparison, relative scoring, filters, and middle-order evidence. |
| **Bowling Lab** | Phase-based bowling evidence and performance comparisons. |
| **Strategy Board** | Recruitment strategy, role-gap matrix, and supporting evidence. |
| **Methodology & Data** | Metric definitions, analytical assumptions, and limitations. |

## Data and Analysis

The application reads eight prepared CSV files from the `data/` directory:

| File | Description |
|---|---|
| `rr_final_auction_strategy.csv` | Role-level auction strategy and recruitment priorities. |
| `rr_final_middle_order_recruitment.csv` | Qualified middle-order candidate comparison and recruitment labels. |
| `rr_squad_audit.csv` | Historical Rajasthan Royals squad audit. |
| `rr_bowling_evidence.csv` | Bowling evidence organised for phase-based analysis. |
| `rr_gap_matrix.csv` | Role-gap assessment and supporting recruitment recommendations. |
| `rr_opening_role_conclusion.csv` | Opening-role conclusion and existing-player context. |
| `rr_opening_combined_ranking.csv` | Combined opening candidate ranking. |
| `rr_opening_player_evidence.csv` | Player-level opening batting evidence. |

### Analysis framework

The analysis uses historical IPL performance from **2022–2026**. The prepared datasets support role-specific comparisons rather than treating every player as interchangeable.

The middle-order analysis defines middle-order batting positions as **positions 4–7**. Its candidate score is a weighted, percentile-style comparative score across the qualified candidate pool. It is a relative ranking aid, **not a probability of future success**.

Pressure metrics are calculated using the project's defined pressure filter. In particular, the displayed pressure batting average is based on pressure runs divided by batter dismissals in the filtered pressure deliveries; it should not automatically be interpreted as a conventional season batting average.

### Current strategic signal

The current analysis identifies **death bowling as the highest role-level recruitment priority**. The dashboard reports a historical decline in Rajasthan Royals' death-phase wicket rate from **7.91 per 100 balls in 2022** to **6.39 per 100 balls in 2026**.

These bowling phase figures are provisional. Extras classification and legal-ball assumptions require validation before the figures are treated as official bowling statistics.

---

## Repository Structure

```text
RR_Ipl_Auction/
│
├── app.py
├── requirements.txt
├── README.md
│
├── .streamlit/
│   └── config.toml
│
└── data/
    ├── rr_final_auction_strategy.csv
    ├── rr_final_middle_order_recruitment.csv
    ├── rr_squad_audit.csv
    ├── rr_bowling_evidence.csv
    ├── rr_gap_matrix.csv
    ├── rr_opening_role_conclusion.csv
    ├── rr_opening_combined_ranking.csv
    └── rr_opening_player_evidence.csv
```

The application expects the CSV filenames above to remain inside the `data/` directory.

## Technology Stack

- **Python** — application and data-processing language.
- **Streamlit** — interactive dashboard framework.
- **Pandas** — CSV loading and tabular data operations.
- **NumPy** — numerical operations.
- **Plotly Express / Plotly Graph Objects** — interactive charts and visualisations.
- **CSS** — custom Rajasthan Royals-inspired navy and pink interface styling.
- **GitHub** — source control and project hosting.
- **Streamlit Community Cloud** — public application deployment.

## Run Locally

### 1. Clone the repository

```bash
git clone https://github.com/Siddharth8445/RR_Ipl_Auction.git
cd RR_Ipl_Auction
```

### 2. Create and activate a virtual environment

**Windows PowerShell**

```powershell
python -m venv .venv
.venv\Scripts\Activate.ps1
```

**macOS / Linux**

```bash
python3 -m venv .venv
source .venv/bin/activate
```

### 3. Install dependencies

```bash
python -m pip install --upgrade pip
pip install -r requirements.txt
```

### 4. Confirm the data files

Make sure all eight CSV files listed in [Data and Analysis](#data-and-analysis) are present in the `data/` directory.

### 5. Start the Streamlit application

```bash
python -m streamlit run app.py
```

Streamlit will print a local URL in the terminal, usually:

```text
http://localhost:8501
```

Open that address in your browser.

## Deployment

The application is hosted on **Streamlit Community Cloud** and connected to this GitHub repository.

Live URL: https://rr-ipl-auction-intelligence.streamlit.app/

To publish a code update:

```bash
git add .
git commit -m "Describe your update"
git push origin main
```

Streamlit Community Cloud can then deploy the latest version from the connected repository.

## Analytical Notes and Limitations

Please interpret the dashboard as a scouting aid, not as a definitive player-selection model.

1. **Historical window:** The analysis covers IPL data from 2022–2026. Historical performance does not guarantee future performance.
2. **Pressure definition:** Pressure statistics depend on the project's selected pressure filter and should be read with that definition in mind.
3. **Relative candidate scores:** The middle-order score compares candidates within the qualified analysis pool. It is not a success probability or a forecast.
4. **Metric interpretation:** Pressure batting average and consistency measures use project-specific definitions; they may differ from conventional scorecard statistics.
5. **Bowling calculations:** Bowling phase metrics are provisional pending validation of extras and legal-ball assumptions. Do not treat them as official economy or overs figures without that validation.
6. **Squad status:** The squad audit is a historical 2026 baseline, not confirmation of the Rajasthan Royals' IPL 2027 retained squad.
7. **Player availability:** Retention, auction eligibility, overseas-player limits, injuries, purse constraints, and final availability must be checked against authoritative updates before recruitment decisions are made.
8. **Scouting judgement:** A high historical score is only one input. Role fit, squad balance, tactical requirements, price, and availability also matter.

## Future Improvements

- Validate bowling legal-ball and extras calculations against official scorecards.
- Add verified auction-pool, retention, and player-availability information when officially released.
- Incorporate auction purse and overseas-player constraints into scenario planning.
- Add role-specific scenario comparisons and sensitivity analysis.
- Extend the analysis with additional seasons as reliable data becomes available.

---

## Author

**Siddharth Kumar**

B.Tech, Computer Science and Engineering

- GitHub: [@Siddharth8445](https://github.com/Siddharth8445)
- Project Repository: [RR_Ipl_Auction](https://github.com/Siddharth8445/RR_Ipl_Auction)
- Live Dashboard: [RR Auction Intelligence](https://rr-ipl-auction-intelligence.streamlit.app/)

---

<p align="center">
  <strong>Rajasthan Royals | IPL 2027 Auction Intelligence</strong><br>
  <sub>Evidence-led scouting. Role-first recruitment. Data-informed decisions.</sub>
</p>
