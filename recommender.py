from __future__ import annotations
from typing import List, Tuple, Iterable

from user import User
from property import Property


def _normalize_to_list(x) -> list[str]:
    """
    Accepts list/tuple/set/None/str and returns a clean list[str].
    - If it's a CSV string: split by ','.
    - Trims whitespace and lowercases for matching.
    """
    if x is None:
        return []
    if isinstance(x, str):
        parts = [p.strip() for p in x.split(",") if p.strip()]
    elif isinstance(x, Iterable):
        parts = [str(p).strip() for p in x if str(p).strip()]
    else:
        parts = [str(x).strip()]
    return [p.lower() for p in parts]


def _env_score(user: User, prop: Property) -> float:
    """
    1.0 if user's preferred_env appears in property's tags (case-insensitive), else 0.0.
    """
    user_env = (user.preferred_env or "").strip().lower()
    if not user_env:
        return 0.0
    tags = _normalize_to_list(getattr(prop, "tags", []))
    return 1.0 if user_env in tags else 0.0


def _price_score(user: User, price: float) -> float:
    """
    Return a [0,1] affordability score:
    - 1.0 inside the budget range
    - smoothly decays if above max (heavier penalty)
    - mild penalty if below min (you might expect higher quality)
    """
    bmin = float(user.budget_min)
    bmax = float(user.budget_max)

    if bmin > bmax:
        bmin, bmax = bmax, bmin  # safety

    if price < bmin:
        # below desired range: close to 1 if just a bit below; lower if far below
        # distance as fraction of bmin (avoid div-by-zero)
        frac = (bmin - price) / max(1.0, bmin)
        return max(0.6, 1.0 - 0.4 * min(frac, 1.0))  # clamp to [0.6, 1.0]
    elif price <= bmax:
        return 1.0
    else:
        # above budget: stronger penalty, linear decay toward 0
        over_frac = (price - bmax) / max(1.0, bmax)
        return max(0.0, 1.0 - min(1.0, over_frac))


def _feature_overlap(required_features: list[str] | None, prop_features) -> float:
    """
    Fraction of required features present in the property (0..1).
    If user didn't specify any required features, return neutral 0.5.
    """
    if not required_features:
        return 0.5
    want = set(_normalize_to_list(required_features))
    have = set(_normalize_to_list(prop_features))
    if not want:
        return 0.5
    return len(want & have) / len(want)


def score_property(user: User, prop: Property, required_features: list[str] | None = None) -> float:
    """
    Weighted, human-explainable score.
    """
    env = _env_score(user, prop)                   # 0 or 1
    price = _price_score(user, float(prop.nightly_price))
    feat = _feature_overlap(required_features, getattr(prop, "features", []))

    # weights chosen to prioritize vibe and affordability
    total = 2.0 * price + 1.5 * env + 1.0 * feat
    return float(total)


def recommend(user: User, props: List[Property], top_n: int = 3,
              required_features: list[str] | None = None) -> List[Tuple[Property, float]]:
    """
    Score all properties and return the top-N as (property, score).
    If 'props' is empty, returns [].
    """
    if not props:
        return []
    scored = [(p, score_property(user, p, required_features)) for p in props]
    scored.sort(key=lambda x: x[1], reverse=True)
    return scored[:top_n]
