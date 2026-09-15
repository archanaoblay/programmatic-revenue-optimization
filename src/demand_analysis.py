import pandas as pd


def analyze_demand_partners(file_path):
    df = pd.read_csv(file_path)

    analysis = df.groupby("demand_partner").agg(
        requests=("ad_requests", "sum"),
        responses=("responses", "sum"),
        wins=("wins", "sum"),
        impressions=("impressions", "sum"),
        revenue=("revenue", "sum"),
        avg_latency=("latency_ms", "mean")
    ).reset_index()

    analysis["fill_rate"] = (
        analysis["responses"] / analysis["requests"] * 100
    ).round(2)

    analysis["win_rate"] = (
        analysis["wins"] / analysis["responses"] * 100
    ).round(2)

    analysis["ecpm"] = (
        analysis["revenue"] / analysis["impressions"] * 1000
    ).round(2)

    return analysis.sort_values("revenue", ascending=False)
