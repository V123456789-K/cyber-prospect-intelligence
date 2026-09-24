import json
import os
import sys
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/"app"))
from scoring import score_prospect

DATASET=ROOT/"evals"/"datasets"/"llm_evals.json"

def build_record(data):
    return {"org":data.get("organization"),"domains":data.get("domains"),"hostnames":data.get("hostnames"),"asn":data.get("asn"),"os":data.get("os"),"transport":data.get("transport"),"location":None,"_shodan":{"module":data.get("module")}}

def validate_case(case):
    data=case["input"]; expected=case["expected"]
    result=score_prospect(build_record(data))
    assert 0 <= result["score"] <= 100
    assert len(expected["required_sections"]) == 4
    assert isinstance(expected["evidence_keys"],list)
    assert expected["forbidden_claims"]

def main():
    cases=json.loads(DATASET.read_text(encoding="utf-8"))
    for case in cases: validate_case(case)
    print(f"Dataset contract: {len(cases)}/{len(cases)} LLM eval cases valid.")
    if not os.getenv("OPENAI_API_KEY"):
        print("LLM calls not run: OPENAI_API_KEY is not configured.")
        return
    from llm import summarize_prospect
    passed=0
    for case in cases:
        data=case["input"]; record=build_record(data); scored=score_prospect(record)
        result=summarize_prospect({**data,"module":data.get("module")},scored["score"],scored["signals"])
        text=result.get("text","").lower()
        assert result["status"] == "success", case["id"]
        for section in case["expected"]["required_sections"]: assert section.lower() in text, case["id"]
        for claim in case["expected"]["forbidden_claims"]: assert claim.lower() not in text, case["id"]
        passed += 1
    print(f"LLM contract checks: {passed}/{len(cases)} passed.")

if __name__ == "__main__": main()
