# Rajasthan Royals Auction Intelligence — IPL 2027

A professional Streamlit scouting and auction-strategy dashboard inspired by the supplied Rajasthan Royals auction-arena reference.

## 1. Add your eight CSV files

Copy these exact files into `data/`:

- `rr_final_auction_strategy.csv`
- `rr_final_middle_order_recruitment.csv`
- `rr_squad_audit.csv`
- `rr_bowling_evidence.csv`
- `rr_gap_matrix.csv`
- `rr_opening_role_conclusion.csv`
- `rr_opening_combined_ranking.csv`
- `rr_opening_player_evidence.csv`

## 2. Install

```bash
python -m venv .venv
```

Windows PowerShell:
```powershell
.venv\Scripts\Activate.ps1
pip install -r requirements.txt
```

## 3. Run

```bash
streamlit run app.py
```

Open `http://localhost:8501`.

## Pages

- Auction Arena
- Squad Matrix
- Opening Analysis
- Middle-Order Lab
- Bowling Lab
- Strategy Board
- Methodology & Data

## Important

This is an auction-preparation and historical scouting dashboard, not a live bidding feed. It does not claim real-time purse, live bids, 2027 player availability, retention, or auction eligibility. Bowling metrics remain marked provisional as per the analysis caveats.
