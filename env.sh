#!/usr/bin/env bash

# Copy this file to env.sh and fill in your own values.
# Do NOT commit env.sh with real credentials.

export DBUsername="myuser"
export DBPassword="mypassword"
export DBHost="db.example.com"
export DBPort="5432"
export DBDatabase="projectdb"

export DB_URL="postgresql://${DBUsername}:${DBPassword}@${DBHost}:${DBPort}/${DBDatabase}"