import pandas as pd


def generate_optimization_recommendations(file_path):
    df = pd.read_csv(file_path)

    # Calculate eCPM for each demand partner
    partner_analysis = df.groupby("demand_partner").agg(
        requests=("ad_requests", "sum"),
        impressions=("impressions", "sum"),
        revenue=("revenue", "sum"),
        fill_rate=("responses", "sum")
    ).reset_index()

    partner_analysis["ecpm"] = (
        partner_analysis["revenue"]
        / partner_analysis["impressions"]
        * 1000
    )

    # Calculate average eCPM
    average_ecpm = partner_analysis["ecpm"].mean()

    recommendations = []

    for _, row in partner_analysis.iterrows():

        if row["ecpm"] < average_ecpm * 0.80:
            recommendations.append({
                "demand_partner": row["demand_partner"],
                "issue": "Low eCPM",
                "recommendation": "Review partner performance and consider reducing priority or testing alternative demand."
            })

        elif row["ecpm"] > average_ecpm * 1.20:
            recommendations.append({
                "demand_partner": row["demand_partner"],
                "issue": "High eCPM",
                "recommendation": "Consider increasing partner priority to capture more high-value demand."
            })

    return pd.DataFrame(recommendations)
