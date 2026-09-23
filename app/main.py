import streamlit as st

from data import build_dataframe
from scoring import score_prospect


st.set_page_config(
    page_title="Cyber Prospect Intelligence",
    layout="wide"
)

st.title("Cyber Prospect Intelligence")
st.caption(
    "Infrastructure-based prospecting and targeting prototype"
)

df = build_dataframe()

if df.empty:
    st.error("No records found.")
    st.stop()

# Calculate scores
scores = []

for _, row in df.iterrows():
    result = score_prospect(row["raw"])
    scores.append(result)

df["score"] = [x["score"] for x in scores]
df["signals"] = [x["signals"] for x in scores]

# Sidebar filters
st.sidebar.header("Filters")

countries = sorted(
    [x for x in df["country"].dropna().unique()]
)

selected_country = st.sidebar.selectbox(
    "Country",
    ["All"] + countries
)

min_score = st.sidebar.slider(
    "Minimum prospect score",
    0,
    100,
    0
)

filtered = df.copy()

if selected_country != "All":
    filtered = filtered[
        filtered["country"] == selected_country
    ]

filtered = filtered[
    filtered["score"] >= min_score
]

filtered = filtered.sort_values(
    "score",
    ascending=False
)

# Metrics
c1, c2, c3 = st.columns(3)

c1.metric("Prospects", len(filtered))
c2.metric(
    "High-signal prospects",
    len(filtered[filtered["score"] >= 60])
)
c3.metric(
    "Organizations identified",
    filtered["organization"].notna().sum()
)

st.divider()

st.subheader("Prospect List")

display_columns = [
    "score",
    "ip",
    "organization",
    "country",
    "city",
    "asn",
    "module",
    "domains"
]

st.dataframe(
    filtered[display_columns],
    use_container_width=True,
    hide_index=True
)

st.divider()

st.subheader("Prospect Investigation")

if len(filtered) > 0:

    selected_ip = st.selectbox(
        "Select prospect",
        filtered["ip"].tolist()
    )

    prospect = filtered[
        filtered["ip"] == selected_ip
    ].iloc[0]

    left, right = st.columns(2)

    with left:
        st.metric(
            "Prospect Score",
            prospect["score"]
        )

        st.write("**Organization:**", prospect["organization"])
        st.write("**ASN:**", prospect["asn"])
        st.write("**Location:**",
                 f"{prospect['city']}, {prospect['country']}")
        st.write("**Domains:**", prospect["domains"])
        st.write("**Hostnames:**", prospect["hostnames"])

    with right:
        st.write("### Why this prospect?")

        for signal in prospect["signals"]:
            st.write(f"✓ {signal}")

else:
    st.info("No prospects match the selected filters.")