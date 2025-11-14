# Python Streamlit - 15 Days Challenge

A collection of bite-sized Streamlit projects, one per day, to sharpen UI skills and data handling with Python.

## Repository Layout

```
python_15_days_challenge/
├── Day1/
│   └── greeting_form.py
├── Day2/
│   └── expense_splitter.py
├── Day3/
│   └── simple_calculator.py
├── Day4/
│   └── bmi_calculator.py
├── README.md
└── requirements.txt
```

Install the shared dependencies once:

```bash
pip install -r requirements.txt
```

## Progress Tracker

| Day | Challenge | Status | Date Completed | Description |
|-----|-----------|--------|----------------|-------------|
| 1 | Greeting Form | ✅ Completed | Nov 11, 2025 | Built a friendly form with name + age capture, dynamic greetings, and playful metrics |
| 2 | Expense Splitter | ✅ Completed | Nov 13, 2025 | Split INR expenses with custom names, contributions, balances, and helpful charts |
| 3 | Modern Calculator | ✅ Completed | Nov 14, 2025 | Responsive Streamlit calculator with instant results, zero-division guardrails, and a sleek glassmorphism UI |
| 4 | BMI Calculator | ✅ Completed | Nov 14, 2025 | Professional BMI calculator with height (cm) & weight (kg) inputs, color-coded categories, and health recommendations |
| 5 | TBD | ⏳ Pending | - | Coming soon... |
| 6 | TBD | ⏳ Pending | - | Coming soon... |
| 7 | TBD | ⏳ Pending | - | Coming soon... |
| 8 | TBD | ⏳ Pending | - | Coming soon... |
| 9 | TBD | ⏳ Pending | - | Coming soon... |
| 10 | TBD | ⏳ Pending | - | Coming soon... |
| 11 | TBD | ⏳ Pending | - | Coming soon... |
| 12 | TBD | ⏳ Pending | - | Coming soon... |
| 13 | TBD | ⏳ Pending | - | Coming soon... |
| 14 | TBD | ⏳ Pending | - | Coming soon... |
| 15 | TBD | ⏳ Pending | - | Coming soon... |

**Progress: 4/15 Days Completed (26.67%)** 🎉

---

## Day 1 – Greeting Form (`Day1/greeting_form.py`)

- Name input, age slider, and custom greeting logic
- Metrics that display name length, age, and estimated days lived
- Balloons celebration and styled submit button

Run it with:

```bash
streamlit run Day1/greeting_form.py
```

---

## Day 2 – Expense Splitter (`Day2/expense_splitter.py`)

- Accepts INR totals, friend names, and per-person contributions
- Computes equal share, detects who owes or should be reimbursed, and handles negative balances
- Highlights discrepancies between total bill and contributions
- Visualises balances and contribution comparisons using Plotly charts

Launch it with:

```bash
streamlit run Day2/expense_splitter.py
```

---

## Day 3 – Modern Calculator (`Day3/simple_calculator.py`)

- Two-number calculator with addition, subtraction, multiplication, and division
- Sleek glassmorphism-inspired card design that updates results instantly
- Handles negative values gracefully, color-coding results and flagging when outputs dip below zero
- Blocks division-by-zero mistakes with helpful warnings and shares a safety checklist in the UI

Spin it up with:

```bash
streamlit run Day3/simple_calculator.py
```

---

More mini-apps dropping daily. Have a feature idea? Jot it down so we can turn it into tomorrow’s project. 🚀
