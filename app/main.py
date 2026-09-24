import os
import streamlit as st

from data import build_dataframe
from scoring import score_prospect
from llm import summarize_prospect

st.set_page_config(page_title="Cyber Prospect Intelligence", layout="wide")
st.title("Cyber Prospect Intelligence")
st.caption("Infrastructure-based prospecting and evidence-grounded research prototype")

DATASET_PATH = os.getenv("DATASET_PATH", "data/sample.jsonl")
df = build_dataframe(DATASET_PATH)

if df.empty:
    st.error(f"No records found in {DATASET_PATH}.")
    st.stop()

scores = [score_prospect(row["raw"]) for _, row in df.iterrows()]
df["score"] = [x["score"] for x in scores]
df["signals"] = [x["signals"] for x in scores]

st.sidebar.header("Filters")
countries = sorted([x for x in df["country"].dropna().unique()])
selected_country = st.sidebar.selectbox("Country", ["All"] + countries)
min_score = st.sidebar.slider("Minimum research-priority score", 0, 100, 0)
filtered = df.copy()
if selected_country != "All": filtered = filtered[filtered["country"] == selected_country]
filtered = filtered[filtered["score"] >= min_score].sort_values("score", ascending=False)

c1,c2,c3=st.columns(3)
c1.metric("Prospects",len(filtered)); c2.metric("High-signal prospects",len(filtered[filtered["score"]>=60])); c3.metric("Organizations identified",filtered["organization"].notna().sum())
st.divider()
st.subheader("Prospect List")
st.dataframe(filtered[["score","ip","organization","country","city","asn","module","domains"]],use_container_width=True,hide_index=True)
st.divider()
st.subheader("Prospect Investigation")

if len(filtered):
    selected_ip=st.selectbox("Select prospect",filtered["ip"].tolist())
    prospect=filtered[filtered["ip"]==selected_ip].iloc[0]
    left,right=st.columns(2)
    with left:
        st.metric("Research-priority score",prospect["score"])
        st.write("**Organization:**",prospect["organization"])
        st.write("**ASN:**",prospect["asn"])
        st.write("**Location:**",f"{prospect['city']}, {prospect['country']}")
        st.write("**Domains:**",prospect["domains"])
        st.write("**Hostnames:**",prospect["hostnames"])
    with right:
        st.write("### Why this prospect?")
        for signal in prospect["signals"]: st.write(f"✓ {signal}")
        st.write("### AI Research Assistant")
        st.caption("The LLM summarizes only the observable evidence shown here; it does not calculate the score or establish security need.")
        if st.button("Generate evidence-grounded research summary", type="primary"):
            with st.spinner("Generating research summary..."):
                result=summarize_prospect(prospect["raw"],int(prospect["score"]),prospect["signals"])
            if result["status"] == "success":
                st.markdown(result["text"])
                usage=result.get("usage",{})
                if usage: st.caption(f"Model: {usage.get('model')} · {usage.get('input_tokens',0)} input + {usage.get('output_tokens',0)} output tokens · {usage.get('latency_ms',0)} ms")
            else:
                st.info(result["text"])
else:
    st.info("No prospects match the selected filters.")
