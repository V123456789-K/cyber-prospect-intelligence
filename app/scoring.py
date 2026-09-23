
def score_prospect(record):
    score = 0
    signals = []

    if record.get("domains"):
        score += 20
        signals.append("Domain information available")

    if record.get("hostnames"):
        score += 15
        signals.append("Hostnames identified")

    if record.get("org"):
        score += 15
        signals.append("Organization identified")

    if record.get("asn"):
        score += 10
        signals.append("ASN identified")

    if record.get("location"):
        score += 10
        signals.append("Geographic information available")

    if record.get("os"):
        score += 10
        signals.append("Operating system identified")

    shodan = record.get("_shodan", {})

    if isinstance(shodan, dict):
        if shodan.get("module"):
            score += 10
            signals.append("Technology/module detected")

        if shodan.get("ptr"):
            score += 5
            signals.append("Reverse DNS information available")

    if record.get("transport"):
        score += 5
        signals.append("Network transport identified")

    return {
        "score": min(score, 100),
        "signals": signals
    }
