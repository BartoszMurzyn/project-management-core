# Project Management Core

This repository contains the **core business logic and models** for the Project Management system.  
It is designed as a **separate module** that can be imported into other repositories (e.g., the `API` repository) to ensure clean separation of concerns, reusability, and maintainability.

---

## 🚀 Features
- Core domain models (Projects, Users, Documents, etc.)
- Business logic and validation
- Utilities and shared components
- Database schema definitions (PostgreSQL)

This repo **does not expose an API** itself — instead, it is intended to be used by other services.

---

## 📦 Installation

### 1. Clone the Repository

Clone this repository and install it as a package inside the environment of your `API` project.

```bash
git clone https://github.com/BartoszMurzyn/project-management-core.git
cd project-management-core
pip install -e .
```

### 2. Create and Configure env.sh

Copy the example environment configuration file:
```bash
cp env.sh.example env.sh
```

Open env.sh and set your database connection details:

```bash
#!/usr/bin/env bash

# Database connection components
export DBUsername="myuser"
export DBPassword="mypassword"
export DBHost="db.example.com"
export DBPort="5432"
export DBDatabase="projectdb"

# Construct the full DB_URL
export DB_URL="postgresql+asyncpg://${DBUsername}:${DBPassword}@${DBHost}:${DBPort}/${DBDatabase}"
```
Replace the placeholder values with your actual database credentials.

### 3. Load Environment Variables
```bash
source env.sh
```
### 4. Install Dependencies
```bash
pip install -r requirements.txt
```