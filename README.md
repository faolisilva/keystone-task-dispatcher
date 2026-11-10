# Keystone Task Dispatcher

A lightweight, database-backed task dispatcher. It polls a SQLite database for queued tasks and executes them sequentially. 

## Current Status (MVP)
This is currently a v0.1 internal tool. It does not handle concurrent workers, graceful shutdowns, or worker crashes yet. We just needed a quick replacement for a cron job. 

## Usage
python -m dispatcher.main
