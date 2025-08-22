# Columbus Wedding Budget Planner (Streamlit)

This Streamlit app helps plan a **Winter 2026 Catholic ceremony + mid-range reception** wedding in Columbus, OH for **150–180 guests**. It provides:
- A **preset** comparison (Low / Mid / High)
- A **custom planner** with per-guest and fixed inputs
- **Stacked bar** and **pie chart** visualizations
- One-click **CSV/JSON** export of your breakdown

## Run Locally (Python)
```bash
pip install -r requirements.txt
streamlit run app.py
```
The app listens on **http://localhost:8501** by default.

## Docker
```bash
docker build -t wedding-budget-app .
docker run -d -p 8501:8501 --name wedding-budget-app wedding-budget-app
```
Or with docker-compose:
```bash
docker compose up -d
```

## Reverse Proxy (NGINX Proxy Manager)
- Map a subdomain (e.g. `wedding.mqhomeserver`) to the container at `http://<host-ip>:8501`.
- Enable WebSocket (Streamlit uses it).
- Optionally put it behind Cloudflare Tunnel and your Zero Trust rules.

> **Note on Netlify**: Streamlit is a **Python web app** and isn’t a static site. Netlify’s static hosting won’t run the Streamlit server. Prefer your **on‑prem VM + Docker**, or use a PaaS (Render, Fly.io, Railway) or **Streamlit Community Cloud**.

## Customization
- Edit `app.py` to adjust cost ranges or defaults.
- Replace preset values with live quotes from your vendors.
- Extend the app with additional tabs (timeline, vendor shortlist, task checklist).

