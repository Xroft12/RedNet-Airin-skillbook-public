from __future__ import annotations

from typing import Iterable, List, Sequence, Set
import cmath
import hashlib
import math
import re

from .models import Branch

_TOKEN_RE = re.compile(r"[A-Za-zА-Яа-яЁё0-9_]+", re.UNICODE)


def tokenize(text: str) -> Set[str]:
    return {t.lower() for t in _TOKEN_RE.findall(text or "") if len(t) > 1}


def stable_hash_float(text: str, modulo: int = 10_000) -> float:
    digest = hashlib.sha256(text.encode("utf-8", errors="ignore")).hexdigest()
    return (int(digest[:12], 16) % modulo) / float(modulo)


def phase_from_text(text: str) -> float:
    return stable_hash_float(text, modulo=100_000) * 2.0 * math.pi


def jaccard_kernel(a: str | Iterable[str], b: str | Iterable[str]) -> float:
    ta = tokenize(a) if isinstance(a, str) else set(a)
    tb = tokenize(b) if isinstance(b, str) else set(b)
    if not ta and not tb:
        return 1.0
    if not ta or not tb:
        return 0.0
    return len(ta & tb) / len(ta | tb)


def interference_matrix(branches: Sequence[Branch]) -> List[List[float]]:
    matrix: List[List[float]] = []
    for bi in branches:
        row = []
        left = bi.signature or bi.content
        for bj in branches:
            right = bj.signature or bj.content
            row.append(jaccard_kernel(left, right))
        matrix.append(row)
    return matrix


def normalize_amplitudes(branches: Sequence[Branch]) -> None:
    norm_sq = sum(abs(b.amplitude) ** 2 for b in branches)
    if norm_sq <= 0:
        if not branches:
            return
        value = 1.0 / math.sqrt(len(branches))
        for b in branches:
            b.amplitude = complex(value, 0.0)
        return
    norm = math.sqrt(norm_sq)
    for b in branches:
        b.amplitude = b.amplitude / norm


def born_probabilities(branches: Sequence[Branch]) -> List[float]:
    total = sum(abs(b.amplitude) ** 2 for b in branches)
    if total <= 0:
        if not branches:
            return []
        return [1.0 / len(branches)] * len(branches)
    return [(abs(b.amplitude) ** 2) / total for b in branches]


def softmax(values: Sequence[float], beta: float = 1.0) -> List[float]:
    if not values:
        return []
    scaled = [max(min(beta * v, 60.0), -60.0) for v in values]
    m = max(scaled)
    exps = [math.exp(v - m) for v in scaled]
    s = sum(exps) or 1.0
    return [e / s for e in exps]


def update_signatures(branches: Sequence[Branch]) -> None:
    for b in branches:
        tokens = sorted(tokenize(" ".join([b.role, b.content, " ".join(b.evidence)])))
        b.signature = " ".join(tokens[:128])


def apply_interference(
    branches: Sequence[Branch],
    gamma: float = 0.18,
    eta: float = 0.30,
    beta: float = 2.0,
) -> List[List[float]]:
    """Recalculate amplitudes using a classical interference-inspired rule.

    u_i = score_i - loss_i + gamma * sum_j G_ij score_j - eta * contradiction_i
    alpha_i' = sqrt(softmax(beta * u_i)) * exp(i phase_i)
    """
    update_signatures(branches)
    matrix = interference_matrix(branches)
    utilities: List[float] = []
    for i, b in enumerate(branches):
        support = 0.0
        for j, other in enumerate(branches):
            if i == j:
                continue
            support += matrix[i][j] * other.score
        u = b.score - b.loss + gamma * support - eta * b.contradiction
        utilities.append(u)
        b.add_trace("interference.utility", "utility recalculated", utility=u, support=support)
    probs = softmax(utilities, beta=beta)
    for b, p in zip(branches, probs):
        phase = b.phase if b.phase else phase_from_text(b.branch_id + b.content)
        b.phase = phase
        b.amplitude = math.sqrt(max(p, 0.0)) * cmath.exp(1j * phase)
        b.add_trace("interference.amplitude", "amplitude updated", probability=p, phase=phase)
    normalize_amplitudes(branches)
    return matrix


def entropy(probabilities: Sequence[float]) -> float:
    total = 0.0
    for p in probabilities:
        if p > 0:
            total -= p * math.log(p)
    return total
