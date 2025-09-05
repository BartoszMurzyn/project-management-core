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

Clone this repository and install it as a package inside the environment of your `API` project.

```bash
git clone https://github.com/BartoszMurzyn/project-management-core.git
cd project-management-core
pip install -e .