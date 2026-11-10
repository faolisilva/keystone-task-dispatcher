# Keystone Task Dispatcher

A lightweight, database-backed task dispatcher. It polls a SQLite database for queued tasks and executes them sequentially. 
This is currently an MVP and does not handle concurrent workers or ungraceful shutdowns.

## Usage
python -m dispatcher.main
