# Data Redundancy Removal System

A Python Flask-based web application designed to maintain database accuracy by identifying duplicate records, validating incoming data, and preventing redundant entries.

## Overview

The Data Redundancy Removal System provides a simple and efficient mechanism to validate user records before storing them in a database. It detects exact duplicates using email addresses and phone numbers while identifying potentially similar names for manual review.

The system ensures that only unique and verified records are added to the database.

## Features

- **Data Validation:** Validates user input before database insertion.
- **Duplicate Detection:** Identifies existing records using email addresses and phone numbers.
- **False Positive Prevention:** Flags similar names for manual review instead of automatically rejecting them.
- **Database Integrity:** Uses SQLite with a UNIQUE constraint on email addresses.
- **Secure Database Operations:** Uses parameterized SQL queries to prevent SQL injection through database inputs.
- **Web Interface:** Provides a simple interface for adding and managing records.

## Technology Stack

| Technology | Purpose |
|---|---|
| Python | Backend development |
| Flask | Web framework |
| SQLite | Database management |
| HTML & CSS | User interface |
| SQL | Data storage and validation |

## How It Works

1. A user submits a new record through the web interface.
2. The application validates the submitted information.
3. The system checks existing records for matching email addresses or phone numbers.
4. Similar names are flagged for manual verification.
5. Only unique and verified records are inserted into the database.

## Installation & Setup

**1. Clone the repository**

```bash
git clone https://github.com/sameerkhanio/CodeAlpha_DataRedundancyRemoval.git
cd CodeAlpha_DataRedundancyRemoval
```

**2. Create a virtual environment**

```bash
python -m venv .venv
```

**3. Activate the environment**

Windows:

```bash
.venv\Scripts\activate
```

Linux/macOS:

```bash
source .venv/bin/activate
```

**4. Install dependencies**

```bash
pip install -r requirements.txt
```

**5. Run the application**

```bash
python app.py
```

**6. Open in your browser**

http://127.0.0.1:5000

## Testing

The application supports the following test scenarios:

- Adding a new unique record.
- Rejecting records with duplicate email addresses.
- Detecting duplicate phone numbers.
- Flagging similar names for manual review.
- Successfully storing different unique records.

## Project Structure

```text
CodeAlpha_DataRedundancyRemoval/
│
├── app.py
├── requirements.txt
├── README.md
└── .gitignore
```

## Internship Project

Developed as part of the **CodeAlpha Cloud Computing Internship**.

**Author:** Muhammad Sameer Khan

**GitHub:** https://github.com/sameerkhanio

---

*This project is an educational prototype demonstrating data validation, redundancy detection, and database integrity concepts.*