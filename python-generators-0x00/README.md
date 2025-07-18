# 🌀 Python Generators Project

This project demonstrates efficient data handling using **Python generators** with MySQL.

## 📘 Overview

You'll learn how to:
- Stream SQL data using generators
- Batch process large datasets
- Paginate SQL results lazily
- Compute average values efficiently

## 🛠️ Setup

- Python 3.x
- MySQL Server
- Install MySQL connector:

```bash
pip install mysql-connector-python
```

## 📂 Files

- `seed.py` – Seed MySQL with user data from CSV
- `0-stream_users.py` – Stream users one by one
- `1-batch_processing.py` – Batch process users
- `2-lazy_paginate.py` – Paginate data lazily
- `4-stream_ages.py` – Calculate average user age

## 🚀 Run

```bash
python3 <filename>.py
```

> Make sure MySQL is running and credentials match in `.env`
