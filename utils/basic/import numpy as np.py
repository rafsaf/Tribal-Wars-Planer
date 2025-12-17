import numpy as np
from sklearn.linear_model import Lasso
from sklearn.metrics import mean_squared_error, r2_score
from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import PolynomialFeatures

# =========================================================================
# === 1. FILL IN YOUR DATA VALUES AND SETTINGS HERE ===
# =========================================================================


# Extract data from LEVEL_DICTIONARY where Z != 0
# Format: (X_catapults, Y_current_level): Z_next_level

# X_vals: catapult count (first element of tuple)
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

# Y_vals: current level (second element of tuple)
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

# Z_known: next level (values, excluding all zeros)
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

# --- SETTING ---
# The maximum degree for polynomial terms to check.
# degree=3 includes terms like: x, y, x^2, xy, y^2, x^3, x^2y, xy^2, y^3
max_degree = 2

# =========================================================================
# === 2. DATA PREPARATION ===
# =========================================================================

# Combine X and Y inputs into a single feature matrix X_input
X_input = np.array([X_vals, Y_vals]).T
Z_target = Z_known

# Separate data for training and testing (important for larger datasets)
# We use all data for training here since the dataset is small.
X_train, Z_train = X_input, Z_target

# --- Sanity Check ---
if len(X_vals) != len(Y_vals) or len(X_vals) != len(Z_known):
    raise ValueError(
        "All input arrays (X_vals, Y_vals, Z_known) must have the same length."
    )

# =========================================================================
# === 3. AUTOMATIC FEATURE GENERATION AND REGRESSION ===
# =========================================================================

print(f"--- Running Polynomial Regression (Degree {max_degree}) ---")

# 1. Create the pipeline:
#    a. PolynomialFeatures: Generates all terms up to max_degree (e.g., x, y, x^2, xy, ...)
#    b. LinearRegression: Fits the coefficients to these generated features
# model = make_pipeline(
#     PolynomialFeatures(degree=max_degree, include_bias=False), LinearRegression()
# )
model = make_pipeline(
    PolynomialFeatures(degree=max_degree, include_bias=False),
    Lasso(alpha=0.05, max_iter=10000),  # Increased max_iter for convergence
)

# 2. Train the model
model.fit(X_train, Z_train)

# Get the PolynomialFeatures object from the pipeline
poly_transformer = model.named_steps["polynomialfeatures"]
# Get the LinearRegression object from the pipeline
# linear_model = model.named_steps["linearregression"]
linear_model = model.named_steps["lasso"]

# =========================================================================
# === 4. OUTPUT THE RESULTING FUNCTION ===
# =========================================================================

# Get the names of the features generated (e.g., x0, x1, x0^2, x0 x1, ...)
feature_names_internal = poly_transformer.get_feature_names_out(["x", "y"])

# Get the coefficients found by the model
coefficients = linear_model.coef_
intercept = linear_model.intercept_

# List the features and their corresponding coefficients
print("\nFound Coefficients:")
result_terms = []
for name, coef in zip(feature_names_internal, coefficients):
    # Skip terms with near-zero coefficients (for cleaner output)
    if abs(coef) > 1e-6:
        result_terms.append(f"({coef:.6f} * {name})")
        print(f"  {name}: {coef:.6f}")

print(f"\nIntercept: {intercept:.6f}")

# Reconstruct the final function expression
function_expression = " + ".join(result_terms) + f" + {intercept:.6f}"

print("\n--- Final Best-Fit Function (Terms with significant coefficients) ---")
print(f"f(x, y) ≈ {function_expression}")

# =========================================================================
# === 5. MODEL EVALUATION (Optional but Recommended) ===
# =========================================================================

Z_pred = model.predict(X_train)
mse = mean_squared_error(Z_train, Z_pred)
r2 = r2_score(Z_train, Z_pred)

print("-" * 60)
print("Model Performance Metrics (on Training Data):")
print(f"Mean Squared Error (MSE): {mse:.4f}")
print(f"R-squared (R²): {r2:.4f} (Closer to 1 is better)")
print("-" * 60)
