import pandas as pd
import numpy as np

np.random.seed(42)

ROWS = 50000

dates = pd.date_range(
    start="2026-01-01",
    end="2026-03-31",
    periods=ROWS
)

apps = [
    "App_Alpha",
    "App_Beta",
    "App_Gamma",
    "App_Delta",
    "App_Epsilon"
]

placements = [
    "Banner_01",
    "Banner_02",
    "Interstitial_01",
    "Interstitial_02",
    "Rewarded_01",
    "Video_01"
]

geos = ["US", "UK", "IN", "DE", "BR", "CA"]

devices = ["Android", "iOS"]

formats = [
    "Banner",
    "Interstitial",
    "Rewarded",
    "Video"
]

partners = [
    "Partner_A",
    "Partner_B",
    "Partner_C",
    "Partner_D",
    "Partner_E"
]

df = pd.DataFrame({
    "date": dates,
    "app": np.random.choice(apps, ROWS),
    "placement": np.random.choice(placements, ROWS),
    "geo": np.random.choice(geos, ROWS),
    "device": np.random.choice(devices, ROWS),
    "ad_format": np.random.choice(formats, ROWS),
    "demand_partner": np.random.choice(partners, ROWS),
})

df["ad_requests"] = np.random.randint(500, 10000, ROWS)

df["responses"] = (
    df["ad_requests"] *
    np.random.uniform(0.65, 0.98, ROWS)
).astype(int)

df["wins"] = (
    df["responses"] *
    np.random.uniform(0.15, 0.65, ROWS)
).astype(int)

df["impressions"] = (
    df["wins"] *
    np.random.uniform(0.80, 0.99, ROWS)
).astype(int)

df["clicks"] = (
    df["impressions"] *
    np.random.uniform(0.005, 0.08, ROWS)
).astype(int)

df["conversions"] = (
    df["clicks"] *
    np.random.uniform(0.01, 0.15, ROWS)
).astype(int)

ecpm = np.random.uniform(0.4, 5.0, ROWS)

df["revenue"] = (
    df["impressions"] / 1000 * ecpm
).round(2)

df["latency_ms"] = np.random.uniform(
    80,
    800,
    ROWS
).round(0)

# Simulated monetization issue: Partner C
partner_c = df["demand_partner"] == "Partner_C"
df.loc[partner_c, "revenue"] *= 0.65

# Simulated low eCPM: India + Banner
india_banner = (
    (df["geo"] == "IN") &
    (df["ad_format"] == "Banner")
)

df.loc[india_banner, "revenue"] *= 0.55

# Simulated performance incident
march_drop = (
    (df["date"] >= "2026-03-15") &
    (df["date"] <= "2026-03-20")
)

df.loc[march_drop, "revenue"] *= 0.60
df.loc[march_drop, "latency_ms"] *= 1.8

df["revenue"] = df["revenue"].round(2)
df["latency_ms"] = df["latency_ms"].round(0)

output_path = "data/ad_delivery_data.csv"

df.to_csv(output_path, index=False)

print(f"Dataset created successfully: {output_path}")
print(f"Rows: {len(df)}")
print(f"Columns: {len(df.columns)}")
