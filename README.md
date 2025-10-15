# Streamlit Application Suite

Three production-ready Streamlit applications demonstrating authentication systems, financial transactions, and data management.

[![Python](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/)
[![Streamlit](https://img.shields.io/badge/streamlit-1.0+-red.svg)](https://streamlit.io/)
[![License](https://img.shields.io/badge/license-MIT-green.svg)](LICENSE)

---

## 🚀 Quick Start

```bash
# Clone repository
git clone https://github.com/riffarhan/Streamlit-Application-Suite.git
cd streamlit-suite

# Install dependencies
pip install streamlit

# Run any application
streamlit run case1p4.py  # Authentication Portal
streamlit run case2p4.py  # Cash Receipt System
streamlit run case3p4.py  # Sales Manager
```

---

## 📦 Projects

### 1. Authentication Portal (`case1p4.py`)

Singapore NRIC-based authentication system with age computation.

**Features:**
- Role-based access control (Admin/Citizen)
- NRIC format validation using regex patterns
- Dynamic age calculation from ID numbers
- Input normalization and error handling

**Tech Stack:** `re`, `datetime`, session state management

```python
# Supports multiple authentication methods
Admin: A001/B001 + @Dmin
S-Series NRIC: S#######[A-Z] + g>nZ
T-Series NRIC: T#######[A-Z] + Gen* (with age computation)
```

---

### 2. Cash Receipt System (`case2p4.py`)

SGD cash register with denomination breakdown and transaction logging.

**Features:**
- Greedy algorithm for optimal change calculation
- SGD denominations: $50, $10, $5, $2, $1, $0.50, $0.20, $0.10, $0.05
- Automatic 5-cent rounding (Singapore standard)
- Transaction logging with auto-incrementing receipt numbers
- Integer-cents arithmetic to prevent float precision errors

**Tech Stack:** File I/O, session state, mathematical optimization

```python
# Handles real-world cash scenarios
✓ Underpayment validation
✓ Exact payment handling  
✓ Large change calculations
✓ Automatic collections.txt logging
```

---

### 3. Sales CSV Manager (`case3p4.py`)

Monthly sales uploader with automated yearly aggregation and reporting.

**Features:**
- Standardized file naming: `SalesYYYYMM.csv`
- 12-month agent performance aggregation
- Robust CSV parsing (commas, negatives, mixed case)
- Agent name normalization with display preservation
- Processing metrics and telemetry

**Tech Stack:** `csv`, `os`, data normalization, file management

```python
# Data aggregation intelligence
✓ Handles messy CSV inputs
✓ Agent-month matrix generation
✓ Grand totals with transparency metrics
✓ Automatic sales/ folder management
```

---

## 💻 Application Screenshots

### Authentication Portal
```
🔐 User Authentication Portal
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Enter User ID: T0509999C
Enter Password: ••••
[Enter]

✓ Welcome back, my Singaporean friend at your 20 years old
```

### Cash Receipt System
```
🧾 Singapore Cash Receipting App
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Amount Payable: $25.30
Amount Tendered: $100.00
[Calculate & Record]

✓ Change to be returned: $74.70

💵 Notes Dispensed
1 × $50 note
2 × $10 note
2 × $2 note

🪙 Coins Dispensed
1 × $0.50 coin
1 × $0.20 coin

✓ Transaction recorded to collections.txt
```

### Sales CSV Manager
```
📁 Sales CSV Uploader
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Year: 2025 | Month: 1
[Upload CSV] ✓ Sales202501.csv

📊 Agent Sales Summary for 2025
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Agent  | 01      | 02   | ... | TOTAL
Alice  | 1150.00 | 0    | ... | 1150.00
Bob    | 300.00  | 0    | ... | 300.00

Grand Total: 1450.00
Files processed: 1 | Skipped rows: 0
```

---

## 🔧 Technical Implementation

### Case 1: Authentication
```python
# Pre-compiled regex for performance
PATTERN_S = re.compile(r"S\d{7}[A-Z]")
PATTERN_T = re.compile(r"T\d{7}[A-Z]")

# Dynamic age computation
yy = int(user_id[1:3])
age = datetime.now().year - (2000 + yy)
```

### Case 2: Change Calculation
```python
# Integer-cents model for precision
def to_cents(x: float) -> int:
    return int(round(x * 100))

# 5-cent floor rounding
remainder = change_cents % 5
if remainder != 0:
    change_cents -= remainder
```

### Case 3: Data Normalization
```python
# Separate logic key from display label
def _norm_agent_key(name: str) -> str:
    return name.strip().upper()  # For aggregation

def _label(name: str) -> str:
    return name.strip()  # For display
```

---

## 📊 Key Features

| Feature | Case 1 | Case 2 | Case 3 |
|---------|--------|--------|--------|
| Input Validation | ✅ Regex | ✅ Numeric | ✅ CSV |
| Error Handling | ✅ Try/Except | ✅ Guards | ✅ Per-file |
| Data Persistence | ❌ | ✅ TXT Log | ✅ CSV Files |
| State Management | ✅ Session | ✅ Receipt# | ❌ |
| Algorithm | Pattern Match | Greedy | Aggregation |

---

## 🧪 Testing Coverage

Each application includes comprehensive test cases:

- **Happy Path**: Standard valid inputs
- **Edge Cases**: Boundary values, exact matches
- **Error Handling**: Invalid inputs, malformed data
- **Data Quality**: Mixed formats, special characters
- **System Behavior**: File operations, state persistence

---

## 📁 Project Structure

```
streamlit-suite/
├── case1p4.py              # Authentication Portal
├── case2p4.py              # Receipt System
├── case3p4.py              # Sales Manager
├── collections.txt         # Generated receipt log
├── sales/                  # Generated sales data
│   └── Sales202501.csv
└── README.md
```

---

## 🛠️ Technologies

- **Python 3.8+**
- **Streamlit** - Web framework
- **Standard Library**: `re`, `csv`, `datetime`, `os`
- **Algorithms**: Greedy (change), Regex (validation), Aggregation (sales)

---

## 📋 Requirements

```txt
streamlit>=1.0.0
python>=3.8
```

---

## 🎯 Use Cases

**Case 1**: User authentication, identity verification, age-gated systems  
**Case 2**: Point-of-sale systems, cash handling, transaction logging  
**Case 3**: Sales reporting, data aggregation, monthly/yearly analytics

---

## 🚦 Running Tests

```bash
# Case 1: Test various NRIC formats
User: A001, Pass: @Dmin → Admin access
User: S1234567A, Pass: g>nZ → Old SG citizen
User: T0509999C, Pass: Gen* → New SG (age 20)

# Case 2: Test change scenarios
Payable: $25.30, Tendered: $100.00 → $74.70 change
Payable: $25.30, Tendered: $25.30 → No change
Payable: $25.30, Tendered: $20.00 → Error

# Case 3: Upload test CSV
Month: 1, Year: 2025, File: test.csv → Sales202501.csv
View summary → Agent totals displayed
```

---

## 💡 Design Decisions

1. **Integer Arithmetic** (Case 2): Prevents float precision errors in financial calculations
2. **Pre-compiled Regex** (Case 1): Improves performance and code clarity
3. **Normalized Keys** (Case 3): Handles inconsistent agent name casing
4. **Action Buttons**: Prevents duplicate transactions on input changes
5. **Graceful Degradation**: Continues processing even with partial data errors

---

## 📝 License

This project is available for educational and portfolio purposes.

---

## 👤 Author

**Arif Farhan Bukhori**  
[GitHub](https://github.com/yourusername) • [LinkedIn](https://linkedin.com/in/yourprofile)

---

## 🤝 Contributing

This is a portfolio project. Feel free to fork and adapt for your own use.

---

*Built with Python and Streamlit*
