import math
import json
import pandas as pd
import streamlit as st
import plotly.graph_objects as go
import plotly.express as px

st.set_page_config(
    page_title="Columbus Wedding Budget Planner", 
    page_icon="💒",
    layout="centered"
)


st.title("💒 Columbus Wedding Budget Planner — Winter 2026")
st.caption("Catholic church ceremony + mid-range reception venue, 150–180 guests. Compare low/mid/high presets or build a custom plan.")

# -------------------- Data --------------------
preset_df = pd.DataFrame({
    "Category": [
        "Church Fees",
        "Reception Venue",
        "Catering + Bar",
        "Photography",
        "DJ / Entertainment",
        "Flowers & Decor",
        "Cake & Desserts",
        "Misc. & Extras",
    ],
    "Low":   [650, 2500, 11000, 1750, 850, 2000, 500, 4000],
    "Mid":   [1000, 5000, 19000, 3500, 1350, 5000, 900, 7000],
    "High":  [1250, 9000, 28500, 5500, 3000, 8500, 1350, 9000],
    "Links": [
        "https://sfacolumbus.org/weddings",
        "https://www.reddit.com/r/Columbus/comments/5jx57g/wedding_costs/",
        "https://www.theknot.com/content/average-wedding-cost",
        "https://www.weddingsbytara.com/blog/columbus-wedding-photographer-prices",
        "https://www.night-music.com/pricing/",
        "https://www.theknot.com/content/average-wedding-cost",
        "https://threebitesbakery.com/",
        "https://www.theknot.com/content/average-wedding-cost",
    ]
})



def total(series: pd.Series) -> int:
    return int(series.sum())

def stacked_three_scenarios(df: pd.DataFrame) -> go.Figure:
    """Stacked bars for Low/Mid/High with each category as a trace."""
    # Create data for plotly express
    melted_df = df.melt(
        id_vars=["Category"], 
        value_vars=["Low", "Mid", "High"],
        var_name="Scenario", 
        value_name="Amount"
    )
    
    # Use plotly express for automatic color assignment
    fig = px.bar(
        melted_df, 
        x="Scenario", 
        y="Amount", 
        color="Category",
        title="Wedding Budget Comparison: Low vs Mid vs High Scenarios",
        labels={"Amount": "Cost (USD)", "Scenario": "Budget Scenario"},
        text="Amount"
    )
    
    # Format the text on bars
    fig.update_traces(
        texttemplate='$%{text:,.0f}',
        textposition="inside",
        textfont_size=10
    )
    
    fig.update_layout(
        height=600,
        showlegend=True,
        legend=dict(orientation="v", yanchor="top", y=1, xanchor="left", x=1.02),
        margin=dict(l=50, r=150, t=80, b=50)
    )
    
    return fig

def stacked_single(title: str, breakdown: dict) -> go.Figure:
    """Single stacked bar for a custom breakdown."""
    # Create DataFrame for plotly express
    categories = list(breakdown.keys())
    amounts = list(breakdown.values())
    
    fig = px.bar(
        x=[title] * len(categories),
        y=amounts,
        color=categories,
        title=f"{title} Budget Breakdown",
        labels={"x": "", "y": "Cost (USD)", "color": "Category"}
    )
    
    fig.update_layout(
        height=500,
        showlegend=True,
        xaxis_title="",
        yaxis_title="Cost (USD)"
    )
    
    return fig

with st.expander("📎 Assumptions & Notes"):
    st.markdown("""
- Winter 2026 Columbus market; church + separate reception venue.
- Guest count: **150–180**. Catering/bar scale with headcount.
- BYO alcohol allowed in some venues; check policies (bartender & liability still required).
- Catering estimates often add **~28%** (service + tax) to base food price.
- Flowers scale modestly with table count; venue decor may include basics.
- Use the **Custom Planner** tab to reflect your exact guest count and per-guest costs.
    """)

tab1, tab2 = st.tabs(["📊 Compare Presets", "🛠️ Custom Planner"])

with tab1:
    st.subheader("Preset Low / Mid / High")
    # Interactive table without index, with clickable links
    st.dataframe(
        preset_df,
        use_container_width=True,
        hide_index=True,
        column_config={
            "Links": st.column_config.LinkColumn(display_text="Source")
        }
    )

    # Add spacing column and metric cards with colored styling
    col_spacer, colA, colB, colC = st.columns([1, 1, 1, 1])
    with colA:
        st.metric("Low Total", f"${total(preset_df['Low']):,}")
    with colB:
        st.metric("Mid Total", f"${total(preset_df['Mid']):,}")
    with colC:
        st.metric("High Total", f"${total(preset_df['High']):,}")

    st.plotly_chart(stacked_three_scenarios(preset_df), use_container_width=True, theme=None)

with tab2:
    st.subheader("Custom Planner")
    with st.form("planner"):
        c1, c2, c3 = st.columns(3)
        guests = c1.slider("Guest count", 150, 200, 170, step=5)
        include_service_tax = c2.checkbox("Include 28% service & tax on catering", True)
        byo_overhead = c3.number_input("BYO bar overhead (bartenders, ice, insurance)", min_value=0, value=800, step=50)

        # Fixed-ish sliders
        venue = st.slider("Reception Venue ($)", 2000, 10000, 5000, step=250)
        church = st.slider("Church Fees ($)", 500, 1500, 1000, step=50)
        photography = st.slider("Photography ($)", 1500, 6000, 3500, step=100)
        dj = st.slider("DJ / Entertainment ($)", 700, 4000, 1300, step=50)
        florals = st.slider("Flowers & Decor ($ total)", 1500, 12000, 5000, step=100)

        # Per-guest costs
        c4, c5, c6 = st.columns(3)
        catering_per_guest = c4.slider("Catering per guest (base)", 40, 140, 80, step=5)
        bar_per_guest = c5.slider("Bar per guest", 15, 80, 35, step=5)
        cake_per_guest = c6.slider("Cake/dessert per guest", 3, 12, 6, step=1)
        
        misc = st.slider("Misc. & Extras ($)", 2000, 12000, 7000, step=100)
        add_video = st.checkbox("Add Videography")
        video_cost = st.number_input("Videography ($)", min_value=500, value=2500, step=100) if add_video else 0

        submitted = st.form_submit_button("Calculate")
    
    if submitted:
        # Compute catering
        catering_base = guests * catering_per_guest
        catering_total = int(round(catering_base * 1.28)) if include_service_tax else int(round(catering_base))
        # Compute bar
        bar_total = int(round(guests * bar_per_guest + byo_overhead))
        # Compute cake
        cake_total = int(round(guests * cake_per_guest))

        breakdown = {
            "Church Fees": int(church),
            "Reception Venue": int(venue),
            "Catering": catering_total,
            "Bar (BYO)": bar_total,
            "Photography": int(photography),
            "DJ / Entertainment": int(dj),
            "Flowers & Decor": int(florals),
            "Cake & Desserts": cake_total,
            "Misc. & Extras": int(misc),
        }
        if add_video and video_cost:
            breakdown["Videography"] = int(video_cost)

        total_cost = int(sum(breakdown.values()))

        st.success(f"Estimated Total: **${total_cost:,}** for **{guests}** guests")
        bdf = pd.DataFrame({"Category": list(breakdown.keys()), "Amount": list(breakdown.values())})
        st.dataframe(bdf, use_container_width=True, hide_index=True)

        # Plotly stacked single bar
        st.plotly_chart(stacked_single("Custom", breakdown), use_container_width=False, theme=None)

        # Downloads
        st.download_button(
            "Download breakdown CSV",
            bdf.to_csv(index=False).encode("utf-8"),
            file_name="wedding_budget_breakdown.csv",
            mime="text/csv",
        )

st.markdown("---")
st.markdown("**Resources**: St. Francis of Assisi (Columbus) wedding info, The Knot cost report, local vendor pricing. Adjust all inputs to match current quotes and venue policies.")
