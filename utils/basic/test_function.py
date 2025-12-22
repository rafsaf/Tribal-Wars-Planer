import numpy as np

# =========================================================================
# === INPUT YOUR FUNCTION HERE ===
# =========================================================================


def f(x, y):
    """
    The prediction function for building ruin levels.

    Args:
        x: Number of catapults
        y: Current building level

    Returns:
        Predicted next level after catapult attack
    """
    # IMPORTANT: The SymPy regression fits on *scaled* inputs.
    # Training scaling (x_transform="linear") from ruin_regression_data.py:
    #   X in [5, 1166]  -> x_s = (x - 585.5) / 580.5
    #   Y in [4, 30]    -> y_s = (y - 17.0) / 13.0
    result = (
        1409.9491426110294
        + (-10961.896479089077) * ((np.asarray(y, dtype=float) - 17.0) / 13.0)
        + (8887.395596257455) * ((np.asarray(x, dtype=float) - 585.5) / 580.5)
        + (35254.54190648331) * ((np.asarray(y, dtype=float) - 17.0) / 13.0) ** 2
        + (-62268.48398620238)
        * ((np.asarray(x, dtype=float) - 585.5) / 580.5)
        * ((np.asarray(y, dtype=float) - 17.0) / 13.0)
        + (22352.256592323385) * ((np.asarray(x, dtype=float) - 585.5) / 580.5) ** 2
        + (-61057.565380909655) * ((np.asarray(y, dtype=float) - 17.0) / 13.0) ** 3
        + (177524.86242860352)
        * ((np.asarray(x, dtype=float) - 585.5) / 580.5)
        * ((np.asarray(y, dtype=float) - 17.0) / 13.0) ** 2
        + (-139070.97895220888)
        * ((np.asarray(x, dtype=float) - 585.5) / 580.5) ** 2
        * ((np.asarray(y, dtype=float) - 17.0) / 13.0)
        + (28375.874640425092) * ((np.asarray(x, dtype=float) - 585.5) / 580.5) ** 3
        + (61625.30194932671) * ((np.asarray(y, dtype=float) - 17.0) / 13.0) ** 4
        + (-265867.1299801906)
        * ((np.asarray(x, dtype=float) - 585.5) / 580.5)
        * ((np.asarray(y, dtype=float) - 17.0) / 13.0) ** 3
        + (345173.69674651365)
        * ((np.asarray(x, dtype=float) - 585.5) / 580.5) ** 2
        * ((np.asarray(y, dtype=float) - 17.0) / 13.0) ** 2
        + (-153273.5996871876)
        * ((np.asarray(x, dtype=float) - 585.5) / 580.5) ** 3
        * ((np.asarray(y, dtype=float) - 17.0) / 13.0)
        + (18349.989600916462) * ((np.asarray(x, dtype=float) - 585.5) / 580.5) ** 4
        + (-36062.75026385834) * ((np.asarray(y, dtype=float) - 17.0) / 13.0) ** 5
        + (222926.3702704385)
        * ((np.asarray(x, dtype=float) - 585.5) / 580.5)
        * ((np.asarray(y, dtype=float) - 17.0) / 13.0) ** 4
        + (-434434.4295119708)
        * ((np.asarray(x, dtype=float) - 585.5) / 580.5) ** 2
        * ((np.asarray(y, dtype=float) - 17.0) / 13.0) ** 3
        + (321097.98706742044)
        * ((np.asarray(x, dtype=float) - 585.5) / 580.5) ** 3
        * ((np.asarray(y, dtype=float) - 17.0) / 13.0) ** 2
        + (-83302.54838315665)
        * ((np.asarray(x, dtype=float) - 585.5) / 580.5) ** 4
        * ((np.asarray(y, dtype=float) - 17.0) / 13.0)
        + (4424.937301804264) * ((np.asarray(x, dtype=float) - 585.5) / 580.5) ** 5
        + (11196.501510033615) * ((np.asarray(y, dtype=float) - 17.0) / 13.0) ** 6
        + (-101858.68230917005)
        * ((np.asarray(x, dtype=float) - 585.5) / 580.5)
        * ((np.asarray(y, dtype=float) - 17.0) / 13.0) ** 5
        + (288413.9472004476)
        * ((np.asarray(x, dtype=float) - 585.5) / 580.5) ** 2
        * ((np.asarray(y, dtype=float) - 17.0) / 13.0) ** 4
        + (-323828.0932324542)
        * ((np.asarray(x, dtype=float) - 585.5) / 580.5) ** 3
        * ((np.asarray(y, dtype=float) - 17.0) / 13.0) ** 3
        + (140386.33649128128)
        * ((np.asarray(x, dtype=float) - 585.5) / 580.5) ** 4
        * ((np.asarray(y, dtype=float) - 17.0) / 13.0) ** 2
        + (-17040.529436206863)
        * ((np.asarray(x, dtype=float) - 585.5) / 580.5) ** 5
        * ((np.asarray(y, dtype=float) - 17.0) / 13.0)
        + (-1007.6841511188231) * ((np.asarray(x, dtype=float) - 585.5) / 580.5) ** 6
        + (-1414.4577683559548) * ((np.asarray(y, dtype=float) - 17.0) / 13.0) ** 7
        + (22074.05377715245)
        * ((np.asarray(x, dtype=float) - 585.5) / 580.5)
        * ((np.asarray(y, dtype=float) - 17.0) / 13.0) ** 6
        + (-93225.45771185527)
        * ((np.asarray(x, dtype=float) - 585.5) / 580.5) ** 2
        * ((np.asarray(y, dtype=float) - 17.0) / 13.0) ** 5
        + (155039.7516699507)
        * ((np.asarray(x, dtype=float) - 585.5) / 580.5) ** 3
        * ((np.asarray(y, dtype=float) - 17.0) / 13.0) ** 4
        + (-103516.57059959385)
        * ((np.asarray(x, dtype=float) - 585.5) / 580.5) ** 4
        * ((np.asarray(y, dtype=float) - 17.0) / 13.0) ** 3
        + (21920.074042580014)
        * ((np.asarray(x, dtype=float) - 585.5) / 580.5) ** 5
        * ((np.asarray(y, dtype=float) - 17.0) / 13.0) ** 2
        + (1439.4874043602956)
        * ((np.asarray(x, dtype=float) - 585.5) / 580.5) ** 6
        * ((np.asarray(y, dtype=float) - 17.0) / 13.0)
        + (-665.1391479956127) * ((np.asarray(x, dtype=float) - 585.5) / 580.5) ** 7
        + (24.485136493831828) * ((np.asarray(y, dtype=float) - 17.0) / 13.0) ** 8
        + (-1438.1078434211263)
        * ((np.asarray(x, dtype=float) - 585.5) / 580.5)
        * ((np.asarray(y, dtype=float) - 17.0) / 13.0) ** 7
        + (10817.97397568)
        * ((np.asarray(x, dtype=float) - 585.5) / 580.5) ** 2
        * ((np.asarray(y, dtype=float) - 17.0) / 13.0) ** 6
        + (-27389.69479876416)
        * ((np.asarray(x, dtype=float) - 585.5) / 580.5) ** 3
        * ((np.asarray(y, dtype=float) - 17.0) / 13.0) ** 5
        + (27973.814940012307)
        * ((np.asarray(x, dtype=float) - 585.5) / 580.5) ** 4
        * ((np.asarray(y, dtype=float) - 17.0) / 13.0) ** 4
        + (-9331.534099392717)
        * ((np.asarray(x, dtype=float) - 585.5) / 580.5) ** 5
        * ((np.asarray(y, dtype=float) - 17.0) / 13.0) ** 3
        + (-284.4212720456431)
        * ((np.asarray(x, dtype=float) - 585.5) / 580.5) ** 6
        * ((np.asarray(y, dtype=float) - 17.0) / 13.0) ** 2
        + (674.9673064239886)
        * ((np.asarray(x, dtype=float) - 585.5) / 580.5) ** 7
        * ((np.asarray(y, dtype=float) - 17.0) / 13.0)
        + (-64.28320644175832) * ((np.asarray(x, dtype=float) - 585.5) / 580.5) ** 8
    )

    return result


# =========================================================================
# === DATA VALUES (Same as in other scripts) ===
# =========================================================================

# X_vals: catapult count
X_vals = np.array([188, 255])

# Y_vals: current level
Y_vals = np.array([25, 19])

# Z_known: observed next level (ROUNDED values)
Z_known = np.array([18, 0])

# =========================================================================
# === CALCULATION AND OUTPUT ===
# =========================================================================

# Calculate predictions for all data points
predictions = f(X_vals, Y_vals)
errors = predictions - Z_known
abs_errors = np.abs(errors)

# Summary statistics
total_points = len(X_vals)
within_tolerance = np.sum(abs_errors <= 0.5)
percentage_within = (within_tolerance / total_points) * 100
max_error = np.max(abs_errors)
mean_abs_error = np.mean(abs_errors)

print("=" * 80)
print("FUNCTION EVALUATION RESULTS")
print("=" * 80)
print(f"\nTotal data points: {total_points}")
print(
    f"Points within ±0.5: {within_tolerance}/{total_points} ({percentage_within:.1f}%)"
)
print(f"Mean Absolute Error: {mean_abs_error:.4f}")
print(f"Max Absolute Error: {max_error:.4f}")
print("\n" + "=" * 80)
print("ALL PREDICTIONS")
print("=" * 80)
print(
    f"{'Catapults':>9} | {'Current Lvl':>11} | {'Observed':>8} | {'Predicted':>9} | {'Error':>7}"
)
print("-" * 80)

for i in range(len(X_vals)):
    print(
        f"{X_vals[i]:9.0f} | {Y_vals[i]:11.0f} | {Z_known[i]:8.0f} | "
        f"{predictions[i]:9.2f} | {errors[i]:+7.2f}"
    )

# Now print only the problematic predictions (error > 0.5)
problematic_indices = np.where(abs_errors > 0.5)[0]

if len(problematic_indices) > 0:
    print("\n" + "=" * 80)
    print(f"PREDICTIONS WITH ERROR > 0.5 ({len(problematic_indices)} cases)")
    print("=" * 80)
    print(
        f"{'Catapults':>9} | {'Current Lvl':>11} | {'Observed':>8} | {'Predicted':>9} | {'Error':>7}"
    )
    print("-" * 80)

    for i in problematic_indices:
        print(
            f"{X_vals[i]:9.0f} | {Y_vals[i]:11.0f} | {Z_known[i]:8.0f} | "
            f"{predictions[i]:9.2f} | {errors[i]:+7.2f}"
        )
else:
    print("\n" + "=" * 80)
    print("✓ ALL PREDICTIONS ARE WITHIN ±0.5 OF OBSERVED VALUES!")
    print("=" * 80)

print("\n")
