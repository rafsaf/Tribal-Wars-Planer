from __future__ import annotations

from dataclasses import dataclass
from functools import lru_cache

import numpy as np
from scipy.interpolate import PchipInterpolator

try:
    # When imported as part of the utils.basic package
    from .ruin_regression_data import X_vals, Y_vals, Z_known
except ImportError:
    # When executed directly from this folder
    from ruin_regression_data import X_vals, Y_vals, Z_known


@dataclass(frozen=True)
class _LevelModel:
    y_level: int
    x_min: float
    x_max: float
    pchip: PchipInterpolator


def _aggregate_duplicates(
    x: np.ndarray, z: np.ndarray
) -> tuple[np.ndarray, np.ndarray]:
    # If the same X appears multiple times for a given Y, average Z.
    # This is the best deterministic choice when labels conflict.
    x = np.asarray(x, dtype=float)
    z = np.asarray(z, dtype=float)

    order = np.argsort(x)
    x = x[order]
    z = z[order]

    uniq_x, idx_start = np.unique(x, return_index=True)
    z_out = np.empty_like(uniq_x, dtype=float)

    for i, start in enumerate(idx_start):
        end = idx_start[i + 1] if i + 1 < len(idx_start) else len(x)
        z_out[i] = float(np.mean(z[start:end]))

    return uniq_x, z_out


@lru_cache(maxsize=1)
def _build_models() -> dict[int, _LevelModel]:
    x_all = np.asarray(X_vals, dtype=float)
    y_all = np.asarray(Y_vals, dtype=int)
    z_all = np.asarray(Z_known, dtype=float)

    models: dict[int, _LevelModel] = {}
    for y_level in sorted(set(int(v) for v in y_all.tolist())):
        mask = y_all == y_level
        x = x_all[mask]
        z = z_all[mask]
        x_u, z_u = _aggregate_duplicates(x, z)
        # Need at least 2 unique points for PCHIP; if not, fall back to a constant.
        if len(x_u) < 2:
            const = float(z_u[0]) if len(z_u) else float(np.mean(z_all))
            x_u = np.array([0.0, 1.0], dtype=float)
            z_u = np.array([const, const], dtype=float)

        pchip = PchipInterpolator(x_u, z_u, extrapolate=True)
        models[y_level] = _LevelModel(
            y_level=y_level,
            x_min=float(np.min(x_u)),
            x_max=float(np.max(x_u)),
            pchip=pchip,
        )

    return models


def predict_next_level(
    catapults: float | np.ndarray, current_level: int | np.ndarray
) -> np.ndarray:
    """Piecewise monotone interpolator: predicts next level from (catapults, current_level).

    - Fits a monotone PCHIP per integer current_level (Y).
    - If current_level is not present in the training data, uses the nearest known Y.
    - Clips catapults into the per-level observed X-range for stability.

    Returns a NumPy array (even for scalars).
    """

    models = _build_models()
    known_levels = np.array(sorted(models.keys()), dtype=int)

    x = np.asarray(catapults, dtype=float)
    y = np.asarray(current_level, dtype=int)

    # Broadcast
    x_b, y_b = np.broadcast_arrays(x, y)
    out = np.empty_like(x_b, dtype=float)

    # Vectorized per unique level
    for y_level in np.unique(y_b):
        # Clamp to nearest known level if unseen
        if y_level not in models:
            nearest = int(known_levels[np.argmin(np.abs(known_levels - int(y_level)))])
            model = models[nearest]
        else:
            model = models[int(y_level)]

        mask = y_b == y_level
        x_m = np.clip(x_b[mask], model.x_min, model.x_max)
        out[mask] = model.pchip(x_m)

    return out


def predict_next_level_int(
    catapults: float | np.ndarray, current_level: int | np.ndarray
) -> np.ndarray:
    """Same as predict_next_level, but rounds to nearest integer."""
    return np.rint(predict_next_level(catapults, current_level)).astype(int)
