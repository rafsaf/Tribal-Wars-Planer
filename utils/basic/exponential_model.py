import numpy as np
import sympy as sp
from scipy.optimize import differential_evolution
from sklearn.metrics import mean_squared_error, r2_score
from sympy import lambdify, symbols

# =========================================================================
# === DATA ===
# =========================================================================

X_vals = np.array(
    [
        25,
        25,
        25,
        25,
        25,
        25,
        25,
        25,
        25,
        25,
        25,
        25,
        25,
        25,
        25,
        25,
        25,
        25,
        25,
        25,
        25,
        25,
        25,
        25,
        25,
        50,
        50,
        50,
        50,
        50,
        50,
        50,
        50,
        50,
        50,
        50,
        50,
        50,
        50,
        50,
        50,
        50,
        50,
        50,
        50,
        50,
        50,
        50,
        75,
        75,
        75,
        75,
        75,
        75,
        75,
        75,
        75,
        75,
        75,
        75,
        75,
        75,
        75,
        75,
        75,
        75,
        75,
        75,
        75,
        100,
        100,
        100,
        100,
        100,
        100,
        100,
        100,
        100,
        100,
        100,
        100,
        100,
        100,
        100,
        100,
        100,
        150,
        150,
        150,
        150,
        150,
        150,
        150,
        150,
        150,
        150,
        150,
        150,
        150,
        150,
        150,
        200,
        200,
        200,
        200,
        200,
        200,
        200,
        200,
        200,
        200,
        200,
        200,
        200,
        200,
        1000,
        500,
        1100,
        750,
        750,
        500,
        350,
        281,
        282,
        282,
        281,
        280,
        279,
        278,
        277,
        276,
        275,
        274,
        273,
        272,
        271,
        270,
        269,
        268,
        267,
        37,
        37,
        20,
        15,
        5,
        5,
    ]
)

Y_vals = np.array(
    [
        30,
        29,
        28,
        27,
        26,
        25,
        24,
        23,
        22,
        21,
        20,
        19,
        18,
        17,
        16,
        15,
        14,
        13,
        12,
        11,
        10,
        9,
        8,
        7,
        6,
        30,
        29,
        28,
        27,
        26,
        25,
        24,
        23,
        22,
        21,
        20,
        19,
        18,
        17,
        16,
        15,
        14,
        13,
        12,
        11,
        10,
        9,
        30,
        29,
        28,
        27,
        26,
        25,
        24,
        23,
        22,
        21,
        20,
        19,
        18,
        17,
        16,
        15,
        14,
        13,
        12,
        11,
        30,
        29,
        28,
        27,
        26,
        25,
        24,
        23,
        22,
        21,
        20,
        19,
        18,
        17,
        16,
        15,
        14,
        13,
        30,
        29,
        28,
        27,
        26,
        25,
        24,
        23,
        22,
        21,
        20,
        19,
        18,
        17,
        16,
        15,
        30,
        29,
        28,
        27,
        26,
        25,
        24,
        23,
        22,
        21,
        20,
        19,
        18,
        17,
        30,
        30,
        30,
        30,
        27,
        27,
        27,
        27,
        27,
        26,
        26,
        26,
        26,
        26,
        26,
        26,
        26,
        26,
        26,
        26,
        26,
        26,
        26,
        26,
        26,
        20,
        15,
        10,
        8,
        5,
        4,
    ]
)

Z_known = np.array(
    [
        29,
        28,
        27,
        26,
        25,
        24,
        23,
        22,
        21,
        20,
        19,
        17,
        16,
        15,
        14,
        13,
        12,
        10,
        9,
        8,
        6,
        5,
        4,
        2,
        1,
        29,
        28,
        27,
        25,
        24,
        23,
        22,
        21,
        19,
        18,
        17,
        16,
        14,
        13,
        12,
        10,
        9,
        8,
        6,
        5,
        3,
        1,
        28,
        27,
        26,
        25,
        23,
        22,
        21,
        20,
        18,
        17,
        16,
        14,
        13,
        11,
        10,
        8,
        7,
        5,
        3,
        1,
        27,
        26,
        25,
        24,
        22,
        21,
        20,
        18,
        17,
        16,
        14,
        13,
        11,
        9,
        8,
        6,
        4,
        2,
        26,
        25,
        24,
        22,
        21,
        19,
        18,
        16,
        14,
        13,
        11,
        9,
        7,
        5,
        3,
        1,
        25,
        24,
        22,
        20,
        19,
        17,
        16,
        14,
        12,
        10,
        8,
        6,
        4,
        2,
        5,
        17,
        2,
        11,
        3,
        11,
        16,
        18,
        18,
        16,
        16,
        16,
        16,
        16,
        16,
        16,
        16,
        16,
        16,
        16,
        16,
        16,
        16,
        16,
        17,
        18,
        12,
        7,
        5,
        4,
        3,
    ]
)

rounding_tolerance = 0.5

print("=" * 70)
print("ALTERNATIVE MODEL: y * exp(-a * x^b) form")
print("=" * 70)
print(f"Data points: {len(X_vals)}")
print(f"Rounding tolerance: ±{rounding_tolerance}\n")

# =========================================================================
# === PHYSICALLY-MOTIVATED MODEL ===
# =========================================================================
# Model: z = (y - c) * exp(-a * x^b) + c
# This ensures:
# - When x=0, z = y (no catapults = no damage)
# - z decreases as x increases (more catapults = more damage)
# - z approaches c as x → ∞ (minimum damage level)
# - Works uniformly across all catapult ranges

x, y = symbols("x y", real=True)
a, b, c = symbols("a b c", real=True)

# Model expression
model_expr = (y - c) * sp.exp(-a * (x**b)) + c

print("Model form: z = (y - c) · exp(-a · x^b) + c")
print("Where x = catapults, y = current level, z = next level\n")

# Convert to numerical function
model_func = lambdify([x, y, a, b, c], model_expr, "numpy")


def objective_function(params):
    """Optimize model parameters"""
    a_val, b_val, c_val = params

    # Ensure parameters make sense
    if a_val <= 0 or b_val <= 0:
        return 1e10

    predictions = model_func(X_vals, Y_vals, a_val, b_val, c_val)

    # Strong penalty for impossible values (z > y or z < 0)
    negative_penalty = np.sum(np.maximum(0, -predictions) ** 2) * 10000
    increase_penalty = np.sum(np.maximum(0, predictions - Y_vals) ** 2) * 10000

    # Rounding-aware errors
    errors = np.abs(predictions - Z_known)
    rounding_aware_errors = np.where(
        errors <= rounding_tolerance,
        0.02 * errors,  # Even smaller penalty within tolerance
        errors - rounding_tolerance + 0.02 * rounding_tolerance,
    )

    loss = np.sum(rounding_aware_errors**2)

    return loss + negative_penalty + increase_penalty


print("Running global optimization (this may take a minute)...")

# Use differential evolution for global optimization (better for non-convex problems)
bounds = [(0.00001, 0.05), (0.3, 1.5), (-5, 5)]  # bounds for a, b, c
result = differential_evolution(
    objective_function,
    bounds,
    maxiter=2000,
    popsize=50,
    seed=42,
    atol=1e-10,
    tol=1e-10,
    workers=1,
)

a_opt, b_opt, c_opt = result.x

print("\nOptimization complete!")
print(f"Loss: {result.fun:.6f}\n")

print("=" * 70)
print("OPTIMAL PARAMETERS:")
print("=" * 70)
print(f"a = {a_opt:.6f}")
print(f"b = {b_opt:.6f}")
print(f"c = {c_opt:.6f}")
print("\nFinal function:")
print(f"f(x, y) = y · exp(-{a_opt:.6f} · x^{b_opt:.6f}) + {c_opt:.6f}")

# Evaluate
Z_pred = model_func(X_vals, Y_vals, a_opt, b_opt, c_opt)
mse = mean_squared_error(Z_known, Z_pred)
r2 = r2_score(Z_known, Z_pred)
abs_errors = np.abs(Z_pred - Z_known)
within_tolerance = np.sum(abs_errors <= rounding_tolerance)
percentage_within = (within_tolerance / len(Z_known)) * 100
mae = np.mean(abs_errors)
max_error = np.max(abs_errors)

print("\n" + "=" * 70)
print("MODEL PERFORMANCE:")
print("=" * 70)
print(f"Mean Squared Error (MSE): {mse:.4f}")
print(f"Mean Absolute Error (MAE): {mae:.4f}")
print(f"R-squared (R²): {r2:.4f}")
print(
    f"Predictions within ±{rounding_tolerance}: {within_tolerance}/{len(Z_known)} ({percentage_within:.1f}%)"
)
print(f"Max absolute error: {max_error:.4f}")

print("\n" + "=" * 70)
print("SAMPLE PREDICTIONS:")
print("=" * 70)
print(
    f"{'Catapults':>9} | {'Current Lvl':>11} | {'Observed':>8} | {'Predicted':>9} | {'Error':>7}"
)
print("-" * 70)
for i in range(min(20, len(X_vals))):
    error = Z_pred[i] - Z_known[i]
    print(
        f"{X_vals[i]:9.0f} | {Y_vals[i]:11.0f} | {Z_known[i]:8.0f} | {Z_pred[i]:9.2f} | {error:+7.2f}"
    )

# Check extreme values specifically
print("\n" + "=" * 70)
print("EXTREME VALUES (catapults >= 350):")
print("=" * 70)
print(
    f"{'Catapults':>9} | {'Current Lvl':>11} | {'Observed':>8} | {'Predicted':>9} | {'Error':>7}"
)
print("-" * 70)
extreme_indices = np.where(X_vals >= 350)[0]
for i in extreme_indices:
    error = Z_pred[i] - Z_known[i]
    print(
        f"{X_vals[i]:9.0f} | {Y_vals[i]:11.0f} | {Z_known[i]:8.0f} | {Z_pred[i]:9.2f} | {error:+7.2f}"
    )

problematic_indices = np.where(abs_errors > 0.5)[0]
if len(problematic_indices) > 0:
    print("\n" + "=" * 70)
    print(f"PREDICTIONS WITH ERROR > 0.5 ({len(problematic_indices)} cases)")
    print("=" * 70)
    print(
        f"{'Catapults':>9} | {'Current Lvl':>11} | {'Observed':>8} | {'Predicted':>9} | {'Error':>7}"
    )
    print("-" * 70)
    for i in problematic_indices:
        error = Z_pred[i] - Z_known[i]
        print(
            f"{X_vals[i]:9.0f} | {Y_vals[i]:11.0f} | {Z_known[i]:8.0f} | {Z_pred[i]:9.2f} | {error:+7.2f}"
        )
else:
    print("\n" + "=" * 70)
    print("✓ ALL PREDICTIONS ARE WITHIN ±0.5!")
    print("=" * 70)
