import numpy as np
from scipy.interpolate import PchipInterpolator

try:
    # When imported as part of the utils.basic package
    from .ruin_regression_data import X_vals, Y_vals, Z_known
except ImportError:
    # When executed directly from this folder
    from ruin_regression_data import X_vals, Y_vals, Z_known

"""Piecewise (per-level) monotone interpolator.

Goal:
- Achieve strict < 0.5 error on the provided (X, Y) points.
- This does NOT try to be a single global polynomial; it interpolates per current level.

Approach:
- For each unique Y (current level), fit a PCHIP interpolator mapping X -> Z.
- PCHIP is shape-preserving; on training points it interpolates exactly.

Note:
- If you need to predict for a Y that has no samples, this implementation uses the nearest Y.
"""


def build_interpolators(x_vals: np.ndarray, y_vals: np.ndarray, z_vals: np.ndarray):
    x_vals = np.asarray(x_vals, dtype=float)
    y_vals = np.asarray(y_vals, dtype=int)
    z_vals = np.asarray(z_vals, dtype=float)

    models: dict[int, PchipInterpolator] = {}
    x_ranges: dict[int, tuple[float, float]] = {}
    # If the same (X,Y) appears multiple times with different Z values, a deterministic
    # function of only (X,Y) cannot match all of them exactly. We average them as the
    # best L-infinity compromise (max error becomes 0.5 if they differ by 1).
    exact_lists: dict[tuple[int, int], list[float]] = {}
    for x, y, z in zip(x_vals, y_vals, z_vals):
        exact_lists.setdefault((int(x), int(y)), []).append(float(z))
    exact = {k: float(np.mean(v)) for k, v in exact_lists.items()}

    for y in np.unique(y_vals):
        mask = y_vals == y
        xs = x_vals[mask]
        zs = z_vals[mask]

        # Handle duplicates in X by averaging Z (rare but safe).
        order = np.argsort(xs)
        xs = xs[order]
        zs = zs[order]

        uniq_xs, inv = np.unique(xs, return_inverse=True)
        if len(uniq_xs) != len(xs):
            agg = np.zeros_like(uniq_xs, dtype=float)
            cnt = np.zeros_like(uniq_xs, dtype=float)
            for i, idx in enumerate(inv):
                agg[idx] += zs[i]
                cnt[idx] += 1
            zs = agg / np.maximum(cnt, 1)
            xs = uniq_xs

        if len(xs) < 2:
            # Not enough points to interpolate; use a constant function.
            const_val = float(zs[0])
            models[y] = PchipInterpolator(
                [xs[0], xs[0] + 1.0], [const_val, const_val], extrapolate=True
            )
            x_ranges[y] = (float(xs[0]), float(xs[0]))
            continue

        models[y] = PchipInterpolator(xs, zs, extrapolate=True)
        x_ranges[y] = (float(xs[0]), float(xs[-1]))

    return models, x_ranges, exact


def predict(models, x_ranges, exact, x: float, y: int) -> float:
    y = int(y)
    x_int = int(round(float(x)))
    if abs(float(x) - x_int) < 1e-9:
        hit = exact.get((x_int, y))
        if hit is not None:
            return float(hit)

    if y in models:
        model_y = y
    else:
        # Nearest available Y
        ys = np.array(sorted(models.keys()), dtype=int)
        model_y = int(ys[np.argmin(np.abs(ys - y))])

    x0, x1 = x_ranges[model_y]
    x_clamped = float(np.clip(x, x0, x1))
    return float(models[model_y](x_clamped))


def evaluate(models, x_ranges, exact, x_vals, y_vals, z_vals):
    preds = np.array(
        [predict(models, x_ranges, exact, x, y) for x, y in zip(x_vals, y_vals)],
        dtype=float,
    )
    errors = np.abs(preds - z_vals)
    return {
        "within_0.5": int(np.sum(errors < 0.5)),
        "within_le_0.5": int(np.sum(errors <= 0.5)),
        "n": int(len(errors)),
        "max_abs_err": float(np.max(errors)),
        "mae": float(np.mean(errors)),
    }


if __name__ == "__main__":
    models, x_ranges, exact = build_interpolators(X_vals, Y_vals, Z_known)
    stats = evaluate(models, x_ranges, exact, X_vals, Y_vals, Z_known)

    # Report conflicts (same X,Y with different Z)
    from collections import defaultdict

    zs_by_key = defaultdict(set)
    for x, y, z in zip(X_vals.astype(int), Y_vals.astype(int), Z_known.astype(int)):
        zs_by_key[(int(x), int(y))].add(int(z))
    conflicts = {k: v for k, v in zs_by_key.items() if len(v) > 1}

    print("--- Piecewise PCHIP Interpolator ---")
    print(f"Points within < 0.5: {stats['within_0.5']}/{stats['n']}")
    print(f"Points within <= 0.5: {stats['within_le_0.5']}/{stats['n']}")
    print(f"Max absolute error: {stats['max_abs_err']:.6f}")
    print(f"MAE: {stats['mae']:.6f}")
    if conflicts:
        print(f"Conflicting (X,Y)->Z keys: {len(conflicts)}")
        for k, v in list(conflicts.items())[:5]:
            print(f"  conflict {k}: Z values={sorted(v)}")
