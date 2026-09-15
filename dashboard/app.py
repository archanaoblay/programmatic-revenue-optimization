import streamlit as st
import pandas as pd


# --------------------------------------------------
# PAGE CONFIGURATION
# --------------------------------------------------

st.set_page_config(
    page_title="Programmatic Revenue Optimization",
    page_icon="📊",
    layout="wide"
)


# --------------------------------------------------
# LOAD DATA
# --------------------------------------------------

df = pd.read_csv("ad_delivery_data.csv")
df["date"] = pd.to_datetime(df["date"])


# --------------------------------------------------
# SIDEBAR FILTERS
# --------------------------------------------------

st.sidebar.title("🎛️ Filters")

apps = sorted(df["app"].unique())
geos = sorted(df["geo"].unique())
devices = sorted(df["device"].unique())
ad_formats = sorted(df["ad_format"].unique())
partners = sorted(df["demand_partner"].unique())

selected_app = st.sidebar.multiselect(
    "App",
    apps,
    default=apps
)

selected_geo = st.sidebar.multiselect(
    "GEO",
    geos,
    default=geos
)

selected_device = st.sidebar.multiselect(
    "Device",
    devices,
    default=devices
)

selected_format = st.sidebar.multiselect(
    "Ad Format",
    ad_formats,
    default=ad_formats
)

selected_partner = st.sidebar.multiselect(
    "Demand Partner",
    partners,
    default=partners
)


# Apply filters
filtered_df = df[
    df["app"].isin(selected_app)
    & df["geo"].isin(selected_geo)
    & df["device"].isin(selected_device)
    & df["ad_format"].isin(selected_format)
    & df["demand_partner"].isin(selected_partner)
]


# --------------------------------------------------
# HEADER
# --------------------------------------------------

st.title("🚀 Programmatic Revenue Optimization Engine")

st.write(
    "Interactive analytics dashboard for monitoring programmatic "
    "advertising performance, identifying revenue leakage, and "
    "generating optimization opportunities."
)

st.caption(
    f"Showing {len(filtered_df):,} records from {len(df):,} total records."
)


# --------------------------------------------------
# KPI CALCULATIONS
# --------------------------------------------------

total_requests = filtered_df["ad_requests"].sum()
total_responses = filtered_df["responses"].sum()
total_wins = filtered_df["wins"].sum()
total_impressions = filtered_df["impressions"].sum()
total_clicks = filtered_df["clicks"].sum()
total_revenue = filtered_df["revenue"].sum()

fill_rate = (
    total_responses / total_requests * 100
    if total_requests > 0 else 0
)

win_rate = (
    total_wins / total_responses * 100
    if total_responses > 0 else 0
)

ctr = (
    total_clicks / total_impressions * 100
    if total_impressions > 0 else 0
)

ecpm = (
    total_revenue / total_impressions * 1000
    if total_impressions > 0 else 0
)


# --------------------------------------------------
# KPI CARDS
# --------------------------------------------------

st.subheader("📈 Key Performance Indicators")

col1, col2, col3, col4, col5 = st.columns(5)

col1.metric(
    "Revenue",
    f"${total_revenue:,.2f}"
)

col2.metric(
    "eCPM",
    f"${ecpm:.2f}"
)

col3.metric(
    "Fill Rate",
    f"{fill_rate:.2f}%"
)

col4.metric(
    "Win Rate",
    f"{win_rate:.2f}%"
)

col5.metric(
    "CTR",
    f"{ctr:.2f}%"
)


st.divider()


# --------------------------------------------------
# REVENUE TREND
# --------------------------------------------------

st.subheader("📊 Revenue Trend")

daily_revenue = (
    filtered_df
    .groupby("date")["revenue"]
    .sum()
    .sort_index()
)

st.line_chart(daily_revenue)


# --------------------------------------------------
# DEMAND PARTNER ANALYSIS
# --------------------------------------------------

st.subheader("🤝 Demand Partner Performance")

partner = (
    filtered_df
    .groupby("demand_partner")
    .agg(
        requests=("ad_requests", "sum"),
        responses=("responses", "sum"),
        wins=("wins", "sum"),
        impressions=("impressions", "sum"),
        revenue=("revenue", "sum"),
        avg_latency_ms=("latency_ms", "mean")
    )
    .reset_index()
)

partner["fill_rate"] = (
    partner["responses"]
    / partner["requests"]
    * 100
).round(2)

partner["win_rate"] = (
    partner["wins"]
    / partner["responses"]
    * 100
).round(2)

partner["eCPM"] = (
    partner["revenue"]
    / partner["impressions"]
    * 1000
).round(2)

partner["avg_latency_ms"] = (
    partner["avg_latency_ms"]
    .round(2)
)

partner = partner.sort_values(
    "revenue",
    ascending=False
)

st.dataframe(
    partner,
    use_container_width=True
)


# --------------------------------------------------
# PARTNER REVENUE CHART
# --------------------------------------------------

st.subheader("💰 Revenue by Demand Partner")

partner_chart = partner.set_index(
    "demand_partner"
)["revenue"]

st.bar_chart(partner_chart)


# --------------------------------------------------
# ECPM COMPARISON
# --------------------------------------------------

st.subheader("💵 eCPM Comparison")

ecpm_chart = partner.set_index(
    "demand_partner"
)["eCPM"]

st.bar_chart(ecpm_chart)


# --------------------------------------------------
# REVENUE LEAKAGE DETECTION
# --------------------------------------------------

st.subheader("⚠️ Revenue Leakage Detection")

if len(filtered_df) > 0:

    request_threshold = filtered_df["ad_requests"].quantile(0.75)
    revenue_threshold = filtered_df["revenue"].quantile(0.25)

    leakage = filtered_df[
        (filtered_df["ad_requests"] >= request_threshold)
        & (filtered_df["revenue"] <= revenue_threshold)
    ].copy()

    if len(leakage) > 0:

        leakage["revenue_per_request"] = (
            leakage["revenue"]
            / leakage["ad_requests"]
        )

        leakage["eCPM"] = (
            leakage["revenue"]
            / leakage["impressions"]
            * 1000
        )

        leakage = leakage[
            [
                "date",
                "app",
                "placement",
                "geo",
                "demand_partner",
                "ad_requests",
                "impressions",
                "revenue",
                "eCPM"
            ]
        ]

        st.warning(
            f"{len(leakage)} inventory segments show "
            "high traffic but relatively low revenue."
        )

        st.dataframe(
            leakage.sort_values(
                "ad_requests",
                ascending=False
            ),
            use_container_width=True
        )

    else:
        st.success(
            "No significant revenue leakage detected "
            "for the selected filters."
        )


# --------------------------------------------------
# ANOMALY DETECTION
# --------------------------------------------------

st.subheader("🚨 Revenue Anomaly Detection")

daily = (
    filtered_df
    .groupby("date")["revenue"]
    .sum()
    .reset_index()
)

if len(daily) >= 2:

    mean_revenue = daily["revenue"].mean()
    std_revenue = daily["revenue"].std()

    upper_limit = mean_revenue + (2 * std_revenue)
    lower_limit = mean_revenue - (2 * std_revenue)

    anomalies = daily[
        (daily["revenue"] > upper_limit)
        | (daily["revenue"] < lower_limit)
    ].copy()

    if len(anomalies) > 0:

        anomalies["anomaly_type"] = anomalies[
            "revenue"
        ].apply(
            lambda x:
            "Unusually High Revenue"
            if x > upper_limit
            else "Unusually Low Revenue"
        )

        st.warning(
            f"{len(anomalies)} unusual revenue days detected."
        )

        st.dataframe(
            anomalies,
            use_container_width=True
        )

    else:

        st.success(
            "No significant revenue anomalies detected."
        )


# --------------------------------------------------
# OPTIMIZATION RECOMMENDATIONS
# --------------------------------------------------

st.subheader("🎯 Optimization Recommendations")

if len(partner) > 0:

    average_ecpm = partner["eCPM"].mean()

    recommendations = []

    for _, row in partner.iterrows():

        if row["eCPM"] < average_ecpm * 0.80:

            recommendations.append({
                "Demand Partner": row["demand_partner"],
                "Issue": "Low eCPM",
                "Recommendation":
                    "Review partner performance and "
                    "consider testing alternative demand."
            })

        elif row["eCPM"] > average_ecpm * 1.20:

            recommendations.append({
                "Demand Partner": row["demand_partner"],
                "Issue": "High eCPM",
                "Recommendation":
                    "Consider increasing partner priority "
                    "to capture more high-value demand."
            })

    if recommendations:

        recommendation_df = pd.DataFrame(
            recommendations
        )

        st.dataframe(
            recommendation_df,
            use_container_width=True
        )

    else:

        st.success(
            "No major partner-level optimization "
            "opportunities detected."
        )


# --------------------------------------------------
# FOOTER
# --------------------------------------------------

st.divider()

st.caption(
    "Independent portfolio project using synthetic advertising data."
)
