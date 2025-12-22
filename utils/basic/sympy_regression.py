import numpy as np
from scipy.optimize import NonlinearConstraint, linprog, minimize
from sklearn.metrics import mean_squared_error, r2_score
from sympy import lambdify, symbols

try:
    # When imported as part of the utils.basic package
    from .ruin_regression_data import X_vals, Y_vals, Z_known
except ImportError:
    # When executed directly from this folder
    from ruin_regression_data import X_vals, Y_vals, Z_known

# =========================================================================
# === 1. FILL IN YOUR DATA VALUES AND SETTINGS HERE ===
# =========================================================================

# Extract data from LEVEL_DICTIONARY where Z != 0
# Format: (X_catapults, Y_current_level): Z_next_level


# --- SETTINGS ---
max_degree = 8  # Degree 8 polynomial (needed to get near the 0.5 boundary)
rounding_tolerance = (
    0.5  # Account for rounding: true value is within ±0.5 of rounded value
)
round_coefficients = False  # Don't round - keep full precision
coefficient_penalty = 0.1  # Very small L1 regularization

# Optimization controls (keep degree; improve methodology)
use_constraints = True  # Try to enforce |pred - Z| <= rounding_tolerance for all points
constraint_solver = "lp"  # "lp" (fast, robust) or "trust-constr" (can be slow/freeze)
constraint_margin = 1e-6  # Small margin to avoid boundary numerical issues
random_restarts = 40  # Additional restarts for constrained solver
seed_base = 1337
lp_coeff_bound = 1e6  # Helps HiGHS stability for higher-degree fits
lp_strict_margin = 1e-6  # Try to get strictly below tolerance (0.5 - margin)
lp_highs_method = "highs"  # try "highs" / "highs-ds" / "highs-ipm"

# Allow a small number of outliers while enforcing <=0.5 on the rest (Option B).
allow_outliers = 1
inlier_tolerance = rounding_tolerance  # enforce <= 0.5 for inliers
strict_eval_tolerance = rounding_tolerance - 1e-6  # for reporting strict < 0.5
candidate_exclusions = 25  # try excluding only the worst 25 points (faster than all n)

# Feature transform (still a degree-3 polynomial, just in a better-conditioned feature space)
# Options: "linear" (use X as-is) or "log1p" (use log(1+X)).
x_transform = "linear"  # try: "linear", "log1p", "sqrt", "inv", "inv_sqrt"
run_stage1_powell = (
    False  # LP directly minimizes max abs error; Powell is optional/slow
)

# =========================================================================
# === 2. DATA PREPARATION ===
# =========================================================================

if len(X_vals) != len(Y_vals) or len(X_vals) != len(Z_known):
    raise ValueError("All input arrays must have the same length.")

X_input = np.array([X_vals, Y_vals]).T
Z_target = Z_known

print(f"--- Sympy Polynomial Regression (Degree {max_degree}) ---")
print(f"Data points: {len(X_vals)}")
print(
    f"Accounting for rounding: true values within ±{rounding_tolerance} of observed\n"
)

# =========================================================================
# === 2.5. INPUT SCALING (NUMERICAL STABILITY) ===
# =========================================================================


def _transform_x(x_vals: np.ndarray) -> np.ndarray:
    x_vals = np.asarray(x_vals, dtype=float)
    if x_transform == "linear":
        return x_vals
    if x_transform == "log1p":
        return np.log1p(x_vals)
    if x_transform == "sqrt":
        return np.sqrt(x_vals)
    if x_transform == "inv":
        return 1.0 / x_vals
    if x_transform == "inv_sqrt":
        return 1.0 / np.sqrt(x_vals)
    raise ValueError(f"Unknown x_transform: {x_transform}")


X_feat = _transform_x(X_vals)
Y_feat = Y_vals.astype(float)

# Scale transformed X and Y to roughly [-1, 1] to make x^3 terms numerically sane.
X_min, X_max = float(np.min(X_feat)), float(np.max(X_feat))
Y_min, Y_max = float(np.min(Y_feat)), float(np.max(Y_feat))

X_mid = 0.5 * (X_min + X_max)
Y_mid = 0.5 * (Y_min + Y_max)
X_half = 0.5 * (X_max - X_min)
Y_half = 0.5 * (Y_max - Y_min)

# Avoid division by zero if a feature is constant
if X_half == 0:
    X_half = 1.0
if Y_half == 0:
    Y_half = 1.0

X_scaled = (X_feat - X_mid) / X_half
Y_scaled = (Y_feat - Y_mid) / Y_half

print(
    "Scaling inputs for stability: "
    f"X({x_transform}) in [{X_min:.4f},{X_max:.4f}] -> ~[-1,1], "
    f"Y in [{Y_min:.0f},{Y_max:.0f}] -> ~[-1,1]"
)

# Sanity: strict <0.5 is impossible if the same (X,Y) appears with different Z.
_xy_to_zs: dict[tuple[int, int], set[int]] = {}
for _x, _y, _z in zip(X_vals.astype(int), Y_vals.astype(int), Z_known.astype(int)):
    _xy_to_zs.setdefault((int(_x), int(_y)), set()).add(int(_z))
_conflicts = {k: v for k, v in _xy_to_zs.items() if len(v) > 1}
if _conflicts:
    # If any conflict has Z values that differ by 1, their open intervals
    # (z-0.5, z+0.5) do not overlap -> strict <0.5 cannot be satisfied for both.
    min_required_outliers_strict = 0
    for _k, _zs in _conflicts.items():
        min_required_outliers_strict += len(_zs) - 1
    print(
        "WARNING: Conflicting labels for the same (X,Y) detected. "
        "Strict <0.5 for all points is impossible without outliers. "
        f"Conflicting keys={len(_conflicts)}, minimum strict outliers needed >= {min_required_outliers_strict}."
    )
    for _k, _zs in list(_conflicts.items())[:5]:
        print(f"  conflict {_k}: Z values={sorted(_zs)}")

# =========================================================================
# === 3. SYMBOLIC SETUP WITH SYMPY ===
# =========================================================================

# Define symbolic variables
x, y = symbols("x y", real=True)

# Generate all polynomial terms up to max_degree
terms = []
coeffs_symbols = []
term_exponents = []  # list of (i, j) for x^i * y^j

term_idx = 0
for deg in range(1, max_degree + 1):
    for i in range(deg + 1):
        j = deg - i
        # Create term x^i * y^j
        term = (x**i) * (y**j)
        terms.append(term)
        term_exponents.append((i, j))
        # Create a symbolic coefficient for this term
        coeff_symbol = symbols(f"c{term_idx}", real=True)
        coeffs_symbols.append(coeff_symbol)
        term_idx += 1

# Add intercept term
intercept = symbols("c_intercept", real=True)

# Build the polynomial expression
polynomial_expr = intercept + sum(
    coeff * term for coeff, term in zip(coeffs_symbols, terms)
)

print(f"Polynomial structure with {len(coeffs_symbols) + 1} coefficients:")
print(f"f(x, y) = {polynomial_expr}\n")

# =========================================================================
# === 4. OPTIMIZATION WITH ROUNDING CONSTRAINTS ===
# =========================================================================

# Convert symbolic expression to numerical function
all_coeffs = [intercept] + coeffs_symbols
poly_func = lambdify([x, y] + all_coeffs, polynomial_expr, "numpy")


def _predict_from_coeffs(coeff_values):
    # Evaluate the polynomial on scaled inputs.
    return poly_func(X_scaled, Y_scaled, *coeff_values)


def objective_function(coeff_values):
    """
    Minimize the error accounting for rounding.
    For each data point, the predicted value should be close to the rounded observed value.
    We use a penalty function that accounts for the rounding.
    """
    predictions = _predict_from_coeffs(coeff_values)

    # Calculate error with rounding awareness - NO clamping, raw prediction vs observed
    errors = np.abs(predictions - Z_known)

    # Heavy penalty for errors outside tolerance - we must stay within ±0.5
    rounding_aware_errors = np.where(
        errors <= rounding_tolerance,
        0.001 * errors,  # Tiny penalty within tolerance
        5 * (errors) ** 2,  # ABSOLUTELY MASSIVE penalty outside
    )

    # Total loss: sum of rounding-aware errors
    loss = np.sum(rounding_aware_errors)

    # L1 regularization to encourage simpler (smaller) coefficients
    regularization = coefficient_penalty * np.sum(np.abs(coeff_values[1:]))

    return loss + regularization


# Initial guess: least squares on scaled design matrix (much better than zeros)


def _build_design_matrix(x_arr, y_arr):
    # Columns: intercept, then each term x^i y^j in the exact same order as term_exponents.
    cols = [np.ones_like(x_arr, dtype=float)]
    for i, j in term_exponents:
        cols.append((x_arr**i) * (y_arr**j))
    return np.vstack(cols).T


A = _build_design_matrix(X_scaled, Y_scaled)


# From here on, use the explicit design matrix for predictions.
# This matches the LP formulation exactly and avoids tiny discrepancies from lambdify.
def _predict_from_coeffs(coeff_values):
    coeff_values = np.asarray(coeff_values, dtype=float)
    return A @ coeff_values


lsq_coeffs, *_ = np.linalg.lstsq(A, Z_known.astype(float), rcond=None)
initial_guess = lsq_coeffs

print("Running optimization to find coefficients...")
print("This accounts for the fact that Z_known values are rounded.\n")

# Try multiple optimization methods to find the best fit
print("Trying multiple optimization algorithms...")

best_loss = float("inf")
best_coeffs = None

# Constrained formulation: enforce |pred - Z| <= rounding_tolerance
if use_constraints:
    lower = (-rounding_tolerance + constraint_margin) * np.ones_like(
        Z_known, dtype=float
    )
    upper = (rounding_tolerance - constraint_margin) * np.ones_like(
        Z_known, dtype=float
    )

    def constraint_fun(coeff_values):
        return _predict_from_coeffs(coeff_values) - Z_known

    nl_con = NonlinearConstraint(constraint_fun, lower, upper)

    def regularized_objective(coeff_values):
        # If constraints are satisfied, just prefer smaller coefficients.
        # Add a tiny L2 term to keep trust-constr well-behaved.
        l1 = coefficient_penalty * np.sum(np.abs(coeff_values[1:]))
        l2 = 1e-8 * float(np.sum(coeff_values * coeff_values))
        return l1 + l2


def _max_abs_err(coeff_values):
    preds = _predict_from_coeffs(coeff_values)
    return float(np.max(np.abs(preds - Z_known)))


if run_stage1_powell:
    # Stage 1: keep your original rounding-aware objective, but start from LSQ and add more restarts.
    for trial in range(30):
        if trial == 0:
            guess = initial_guess
        else:
            rng = np.random.default_rng(seed_base + trial)
            # Small noise around LSQ start; scale increases a bit with trial.
            scale = 0.01 * (1.0 + (trial // 10))
            guess = initial_guess + rng.standard_normal(len(all_coeffs)) * scale

        result_powell = minimize(
            objective_function,
            guess,
            method="Powell",
            options={"maxiter": 20000, "ftol": 1e-12},
        )

        if result_powell.fun < best_loss:
            best_loss = result_powell.fun
            best_coeffs = result_powell.x
            print(
                f"  Stage1 Trial {trial}: New best loss = {best_loss:.6f} "
                f"(max_abs_err={_max_abs_err(best_coeffs):.6f})"
            )

# Stage 2: attempt a feasibility solve via constraints, starting from best Stage 1 solution.
if use_constraints:
    print("\nAttempting constrained solve: enforce |pred - Z| <= tolerance...")

    constrained_best = None
    constrained_best_maxerr = float("inf")

    if constraint_solver == "lp":
        # Key observation: the model is linear in coefficients.
        # For design matrix A and coefficients c: preds = A @ c.
        # Option B strategy:
        #   1) Solve minimax LP to minimize max_i |A c - z|.
        #   2) If max error <= 0.5: done.
        #   3) Else exclude up to one worst point and solve feasibility on the rest:
        #        |A_sub c - z_sub| <= 0.5.

        A_mat = A.astype(float)
        z = Z_known.astype(float)
        n, p = A_mat.shape

        def solve_feasibility(A_sub: np.ndarray, z_sub: np.ndarray, tol: float):
            # Find any c such that |A_sub c - z_sub| <= tol.
            A_ub = np.vstack([A_sub, -A_sub])
            b_ub = np.concatenate([z_sub + tol, tol - z_sub])
            res = linprog(
                c=np.zeros(A_sub.shape[1], dtype=float),
                A_ub=A_ub,
                b_ub=b_ub,
                bounds=[(-lp_coeff_bound, lp_coeff_bound)] * A_sub.shape[1],
                method=lp_highs_method,
                options={"presolve": True},
            )
            if res.success and res.x is not None:
                return res.x
            return None

        def solve_minimax(A_all: np.ndarray, z_all: np.ndarray):
            # Minimize t s.t. |A c - z| <= t.
            n_all, p_all = A_all.shape
            c_obj = np.zeros(p_all + 1, dtype=float)
            c_obj[-1] = 1.0
            ones = np.ones((n_all, 1), dtype=float)
            A_ub = np.vstack(
                [
                    np.hstack([A_all, -ones]),
                    np.hstack([-A_all, -ones]),
                ]
            )
            b_ub = np.concatenate([z_all, -z_all])
            bounds = [(-lp_coeff_bound, lp_coeff_bound)] * p_all + [(0.0, None)]
            res = linprog(
                c=c_obj,
                A_ub=A_ub,
                b_ub=b_ub,
                bounds=bounds,
                method=lp_highs_method,
                options={"presolve": True},
            )
            if res.success and res.x is not None:
                return res.x[:-1], float(res.x[-1])
            return None, None

        # 1) Minimax
        coeff_mm, t_mm = solve_minimax(A_mat, z)
        if coeff_mm is None:
            print("  LP minimax failed.")
        else:
            errs_mm = np.abs(A_mat @ coeff_mm - z)
            maxerr_mm = float(np.max(errs_mm))
            viol_mm = int(np.sum(errs_mm > inlier_tolerance))
            print(
                f"  LP minimax solved: t={t_mm:.6f}, max_abs_err={maxerr_mm:.6f}, violations>{inlier_tolerance:.3f}: {viol_mm}/{n}"
            )

            # If already within tolerance (or within allowed outliers), accept.
            if viol_mm <= allow_outliers:
                constrained_best = coeff_mm
                constrained_best_maxerr = maxerr_mm
            else:
                # 2) Exclude one candidate and enforce feasibility on the rest.
                order = np.argsort(-errs_mm)
                tried = 0
                best_feas = None
                best_feas_excl = None
                best_feas_maxerr = float("inf")
                for excl in order[: max(1, candidate_exclusions)]:
                    mask = np.ones(n, dtype=bool)
                    mask[int(excl)] = False
                    coeff = solve_feasibility(A_mat[mask], z[mask], inlier_tolerance)
                    tried += 1
                    if coeff is None:
                        continue
                    errs = np.abs(A_mat @ coeff - z)
                    maxerr = float(np.max(errs))
                    viol = int(np.sum(errs > inlier_tolerance))
                    if viol <= allow_outliers and maxerr < best_feas_maxerr:
                        best_feas = coeff
                        best_feas_excl = int(excl)
                        best_feas_maxerr = maxerr
                        # early exit if very good
                        if best_feas_maxerr <= inlier_tolerance + 1e-9:
                            break

                if best_feas is not None:
                    constrained_best = best_feas
                    constrained_best_maxerr = best_feas_maxerr
                    print(
                        f"  LP feasibility success excluding idx={best_feas_excl} (tried {tried} candidates): "
                        f"global_maxerr={constrained_best_maxerr:.6f}"
                    )
                else:
                    print(
                        f"  LP feasibility failed for all attempted exclusions (tried {tried})."
                    )

    else:
        # Fallback: trust-constr (can be slow on this problem)
        starts = [best_coeffs if best_coeffs is not None else initial_guess]
        rng = np.random.default_rng(seed_base)
        for k in range(random_restarts):
            scale = 0.02 * (1.0 + (k // 10))
            starts.append(starts[0] + rng.standard_normal(len(all_coeffs)) * scale)

        for si, start in enumerate(starts[: (1 + random_restarts)]):
            res_tc = minimize(
                regularized_objective,
                start,
                method="trust-constr",
                constraints=[nl_con],
                options={
                    "maxiter": 500,
                    "gtol": 1e-10,
                    "xtol": 1e-12,
                    "barrier_tol": 1e-12,
                    "verbose": 0,
                },
            )

            cand = res_tc.x
            cand_maxerr = _max_abs_err(cand)
            if cand_maxerr < constrained_best_maxerr:
                constrained_best_maxerr = cand_maxerr
                constrained_best = cand
                print(
                    f"  Constrained start {si}: max_abs_err={cand_maxerr:.6f} "
                    f"(success={res_tc.success}, status={res_tc.status})"
                )

            if cand_maxerr <= rounding_tolerance:
                break

    # Adopt LP result as the best coefficients (it is the global optimum for max error).
    if constrained_best is not None:
        best_coeffs = constrained_best
        best_loss = objective_function(best_coeffs)
        if constrained_best_maxerr <= rounding_tolerance:
            print("✓ Found coefficients satisfying tolerance constraint.")
        else:
            print(
                "✗ Constrained solve did not fully satisfy tolerance; "
                f"best max_abs_err={constrained_best_maxerr:.6f}"
            )

print(f"\nBest loss achieved: {best_loss:.10f}\n")

if best_coeffs is None:
    # Shouldn't happen normally, but keeps the script robust if an optimizer fails.
    print(
        "WARNING: No optimizer produced coefficients; falling back to least-squares guess."
    )
    best_coeffs = initial_guess
    best_loss = objective_function(best_coeffs)

optimal_coeffs = best_coeffs

# Optional: Round coefficients for simplicity if flag is set
if round_coefficients:
    rounded_coeffs = np.round(optimal_coeffs, 6)
    # Test if rounded coefficients still meet tolerance
    test_predictions = _predict_from_coeffs(rounded_coeffs)
    max_test_error = float(np.max(np.abs(test_predictions - Z_known)))

    if max_test_error <= rounding_tolerance:
        print(
            f"✓ Rounded coefficients (6 decimals) work! Max error: {max_test_error:.4f}"
        )
        optimal_coeffs = rounded_coeffs
    else:
        print(
            f"✗ Rounded coefficients don't work (max error: {max_test_error:.4f}), keeping full precision"
        )


# =========================================================================
# === 5. OUTPUT THE RESULTING FUNCTION ===
# =========================================================================

print("\n" + "=" * 70)
print("OPTIMAL COEFFICIENTS FOUND:")
print("=" * 70)

# Display intercept
print(f"\nIntercept (c_intercept): {optimal_coeffs[0]}")

# Display other coefficients with their terms
print("\nPolynomial terms:")
print("ALL COEFFICIENTS (including small ones):")
for idx, (coeff_val, term) in enumerate(zip(optimal_coeffs[1:], terms)):
    term_str = str(term).replace("**", "^").replace("*", "·")
    print(f"  c{idx} ({term_str}): {coeff_val}")

result_terms = [f"{optimal_coeffs[0]}"]
for idx, (coeff_val, term) in enumerate(zip(optimal_coeffs[1:], terms)):
    if abs(coeff_val) > 1e-6:  # Only show significant coefficients in expression
        term_str = str(term).replace("**", "^").replace("*", "·")
        result_terms.append(f"{coeff_val}·{term_str}")

# Construct final expression
function_expression = " + ".join(result_terms)
print("\n" + "=" * 70)
print("FINAL BEST-FIT FUNCTION:")
print("=" * 70)
print(f"f(x, y) = {function_expression}")


# Create numerical function with optimal coefficients
def final_func(x_val, y_val):
    # Apply the same scaling used during training
    x_feat = _transform_x(np.asarray(x_val, dtype=float))
    x_s = (x_feat - X_mid) / X_half
    y_s = (np.asarray(y_val, dtype=float) - Y_mid) / Y_half
    A_eval = _build_design_matrix(x_s, y_s)
    out = A_eval @ np.asarray(optimal_coeffs, dtype=float)
    out = np.asarray(out)
    if out.shape == ():
        return float(out)
    if out.size == 1:
        return float(out.reshape(-1)[0])
    return out


# =========================================================================
# === 6. MODEL EVALUATION ===
# =========================================================================

# Get predictions - use raw predictions, no clamping
Z_pred = final_func(X_vals, Y_vals)

# DEBUG: Check if predictions are actually raw
print("\nDEBUG POLYNOMIAL OUTPUT:")
print(f"  X=1166, Y=30: raw prediction = {final_func(1166, 30):.4f}")
print(f"  X=1000, Y=30: raw prediction = {final_func(1000, 30):.4f}")
print(f"  X=1155, Y=30: raw prediction = {final_func(1155, 30):.4f}")

# Standard metrics
mse = mean_squared_error(Z_known, Z_pred)
r2 = r2_score(Z_known, Z_pred)

# Rounding-aware metrics
within_tolerance = np.sum(np.abs(Z_pred - Z_known) <= rounding_tolerance)
percentage_within_tolerance = (within_tolerance / len(Z_known)) * 100

# Strict inlier metrics (for reporting)
strict_within = np.sum(np.abs(Z_pred - Z_known) < strict_eval_tolerance)
strict_percentage = (strict_within / len(Z_known)) * 100
strict_outliers = len(Z_known) - strict_within

# Average absolute error
mae = np.mean(np.abs(Z_pred - Z_known))

# DEBUG: Find and check extreme catapult cases
extreme_indices = []
for i in range(len(X_vals)):
    if X_vals[i] >= 900:
        extreme_indices.append(i)

print(f"\nDEBUG: Found {len(extreme_indices)} cases with X >= 900")
print("First 10 extreme cases:")
for idx in extreme_indices[:10]:
    error = Z_pred[idx] - Z_known[idx]
    print(
        f"  idx={idx}: X={X_vals[idx]:4d}, Y={Y_vals[idx]:2d}, Expected={Z_known[idx]:2d}, Predicted={Z_pred[idx]:7.2f}, Error={error:+7.2f}"
    )

print("\n" + "=" * 70)
print("MODEL PERFORMANCE METRICS:")
print("=" * 70)
print(f"Mean Squared Error (MSE): {mse:.4f}")
print(f"Mean Absolute Error (MAE): {mae:.4f}")
print(f"R-squared (R²): {r2:.4f}")
print("\nRounding-aware metrics:")
print(
    f"  Predictions within ±{rounding_tolerance}: {within_tolerance}/{len(Z_known)} ({percentage_within_tolerance:.1f}%)"
)
print(
    f"  Strict inliers (<{strict_eval_tolerance:.6f}): {strict_within}/{len(Z_known)} ({strict_percentage:.1f}%), outliers={strict_outliers} (allowed={allow_outliers})"
)
print(f"  Max absolute error: {np.max(np.abs(Z_pred - Z_known)):.4f}")
print("=" * 70)

# =========================================================================
# === 7. SHOW SOME EXAMPLE PREDICTIONS ===
# =========================================================================

print("\n" + "=" * 70)
print("SAMPLE PREDICTIONS (first 200 data points):")
print("=" * 70)
print("Catapults | Current Lvl | Observed | Predicted | Error")
print("-" * 70)
for i in range(min(200, len(X_vals))):
    error = Z_pred[i] - Z_known[i]
    print(
        f"{X_vals[i]:9.0f} | {Y_vals[i]:11.0f} | {Z_known[i]:8.0f} | {Z_pred[i]:9.2f} | {error:+6.2f}"
    )
print("=" * 70)
