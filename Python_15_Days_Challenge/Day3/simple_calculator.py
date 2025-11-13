import streamlit as st

st.set_page_config(
    page_title="Modern Calculator",
    page_icon="🧮",
    layout="centered"
)

# ---------- Styling ----------
st.markdown(
    """
    <style>
        body {
            background: linear-gradient(135deg, #eef2ff 0%, #f9fafb 100%);
        }
        div[data-testid="stVerticalBlock"] > div.element-container:has(> div.calculator-card-anchor) {
            background-color: #ffffffdd;
            backdrop-filter: blur(8px);
            border-radius: 18px;
            padding: 2.5rem 2rem 2.2rem;
            box-shadow: 0 18px 40px rgba(15, 23, 42, 0.12);
        }
        div.calculator-card-anchor {
            height: 0;
            margin: 0;
            padding: 0;
        }
        .stNumberInput input, .stSelectbox select {
            font-size: 1.05rem;
            font-weight: 500;
            border-radius: 10px !important;
            border: 1px solid #cbd5f5 !important;
        }
        .stylish-title {
            font-size: 2.8rem;
            font-weight: 800;
            background: linear-gradient(135deg, #1d4ed8 0%, #7c3aed 50%, #ec4899 100%);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            background-clip: text;
            margin-bottom: 0.5rem;
            letter-spacing: -0.02em;
        }
        .stylish-subtitle {
            color: #64748b;
            font-size: 1.05rem;
            margin-top: 0;
            line-height: 1.6;
        }
        .result-display {
            font-size: 2.5rem;
            font-weight: 700;
            color: #1d4ed8;
        }
        .result-display.negative {
            color: #dc2626;
        }
        .result-display.positive {
            color: #059669;
        }
        .result-display.zero {
            color: #6b7280;
        }
        .status-badge {
            display: inline-flex;
            align-items: center;
            gap: 0.4rem;
            font-weight: 600;
            padding: 0.4rem 0.8rem;
            border-radius: 999px;
            background-color: #e0f2fe;
            color: #0c4a6e;
        }
    </style>
    """,
    unsafe_allow_html=True,
)

card = st.container()
with card:
    st.markdown('<div class="calculator-card-anchor"></div>', unsafe_allow_html=True)
    st.markdown(
        """
        <div class="stylish-title">🧮 Simple Calculator</div>
        <p class="stylish-subtitle">
            Bring quick math to every catch-up: add, subtract, multiply, or divide in seconds.
        </p>
        """,
        unsafe_allow_html=True
    )
    st.divider()

# ---------- Inputs ----------
    col1, col2 = st.columns(2)

    with col1:
        num_a = st.number_input(
            "First number",
            value=0.0,
            step=1.0,
            help="Supports decimals and negatives."
        )

    with col2:
        num_b = st.number_input(
            "Second number",
            value=0.0,
            step=1.0,
            help="Supports decimals and negatives."
        )

    operation = st.selectbox(
        "Choose operation",
        ("Addition ( + )", "Subtraction ( − )", "Multiplication ( × )", "Division ( ÷ )"),
        help="Select the mathematical operation to apply."
    )

    # ---------- Computation ----------
    def calculate(a: float, b: float, op: str) -> tuple[float | None, str]:
        """Return (result, message) pair."""
        try:
            if op.startswith("Addition"):
                return a + b, "Sum of the numbers."
            if op.startswith("Subtraction"):
                return a - b, "Difference between the numbers."
            if op.startswith("Multiplication"):
                return a * b, "Product of the numbers."
            if op.startswith("Division"):
                if b == 0:
                    return None, "Division by zero is undefined. Pick a different second number."
                return a / b, "Quotient of the numbers."
        except Exception as exc:  # Catch any unexpected math errors
            return None, f"Calculation failed: {exc}"
        return None, "Unsupported operation."

    result, status_msg = calculate(num_a, num_b, operation)

    # ---------- Output ----------
    status_col, _ = st.columns([2, 1])
    with status_col:
        badge_icon = "✅" if result is not None else "⚠️"
        st.markdown(
            f'<span class="status-badge">{badge_icon} {status_msg}</span>',
            unsafe_allow_html=True
        )

    st.markdown("### Result")

    if result is None:
        st.error("No valid result to show yet.")
    else:
        # Format result with proper handling of negatives
        pretty = f"{result:,.4f}".rstrip("0").rstrip(".")
        
        # Determine CSS class based on sign for color coding
        if result < 0:
            css_class = "result-display negative"
        elif result > 0:
            css_class = "result-display positive"
        else:
            css_class = "result-display zero"
        
        # Display with appropriate styling (negative numbers already include minus sign)
        st.markdown(
            f'<div class="{css_class}">{pretty}</div>',
            unsafe_allow_html=True
        )
        
        # Show additional info for negative results
        if result < 0:
            st.info(f"💡 **Negative Result**: The calculation resulted in a negative value ({pretty}). This is valid for operations like subtraction when the second number is larger.")

    st.divider()

    with st.expander("How we guard against failures"):
        st.write(
            "- **Division by zero**: Raises a friendly warning instead of crashing the app.\n"
            "- **Negative numbers**: Fully supported! Results are color-coded (red for negative, green for positive, gray for zero).\n"
            "- **Decimal support**: All operations work seamlessly with decimal values.\n"
            "- **Error handling**: Any unexpected error displays as a helpful message so you can adjust inputs.\n"
            "- **Negative result display**: When results are negative, they're clearly highlighted in red with an informative message."
        )

st.caption("Tip: Need to reset? Just punch in new numbers and pick another operation — the result updates instantly.")

