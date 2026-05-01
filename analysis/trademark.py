from rapidfuzz import fuzz

from models import FlaggedListing, TrademarkReport

# words that scream knockoff
KNOCKOFF_WORDS = [
    "replica",
    "dupe",
    "lookalike",
    "inspired",
    "fake",
    "copy",
    "knockoff",
    "knock-off",
    "imitation",
    "bootleg",
    "kw",
    "brand new replica",
]


def knockoff_score(title):
    t = title.lower()
    reasons = []
    for word in KNOCKOFF_WORDS:
        if word in t:
            reasons.append(f'suspicious word: "{word}"')

    # each hit adds 0.3, cap at 0.6
    score = min(len(reasons) * 0.3, 0.6)
    return score, reasons


def fuzzy_score(brand, seller, title):
    reasons = []
    b = brand.lower()
    seller_sim = fuzz.partial_ratio(b, seller.lower()) / 100
    title_sim = fuzz.partial_ratio(b, title.lower()) / 100
    score = 0.0

    if 0.6 < seller_sim < 0.99:
        score += 0.4
        reasons.append(f"seller name similar to brand ({int(seller_sim * 100)}% match)")

    if title_sim > 0.85 and b not in title.lower():
        score += 0.3
        reasons.append(f"title close match to brand ({int(title_sim * 100)}%)")

    return score, reasons


def analyze(brand, items):
    flagged = []
    for item in items:
        k_score, k_reasons = knockoff_score(item.title)
        f_score, f_reasons = fuzzy_score(brand, item.seller, item.title)
        total = min(k_score + f_score, 1.0)
        reasons = k_reasons + f_reasons
        if total > 0:
            flagged.append(FlaggedListing(listing=item, score=total, reasons=reasons))

    flagged.sort(key=lambda x: x.score, reverse=True)
    return TrademarkReport(brand=brand, total_scanned=len(items), flagged=flagged)
