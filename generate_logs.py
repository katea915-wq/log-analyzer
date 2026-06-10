"""
generate_logs.py — генератор тестовых лог-файлов.
Создаёт sample_data/app.log с 200 записями в формате:
    YYYY-MM-DD HH:MM:SS LEVEL Message
Используется для тестирования analyzer.py.
"""


import random
from datetime import datetime, timedelta
import os 


levels = ["ERROR", "WARNING", "INFO", "DEBUG"]

messages = {
    "ERROR": [
        "Database timeout",
        "Connection refused",
        "Disk full",
        "Out of memory",
        "Permission denied",
        "File not found",
        "Broken pipe",
        "Authentication failed",
        "SSL handshake failed",
        "Unable to resolve host"
    ],

    "WARNING": [
        "High memory usage",
        "Slow query detected",
        "CPU usage exceeded threshold",
        "Low disk space",
        "Deprecated API usage",
        "Retry attempt failed",
        "Cache miss rate is high",
        "Configuration value missing",
        "Response time above normal",
        "Connection pool nearly exhausted"
    ],

    "INFO": [
        "User logged in",
        "Service started",
        "Configuration loaded",
        "Database connection established",
        "Backup completed successfully",
        "User logged out",
        "Scheduled task executed",
        "Cache refreshed",
        "File uploaded successfully",
        "Application shutdown completed"
    ],

    "DEBUG": [
        "Entering function process_data",
        "Executing SQL query",
        "Request payload received",
        "Response payload generated",
        "Cache lookup performed",
        "Session token validated",
        "Retry counter incremented",
        "Loading configuration file",
        "Thread acquired lock",
        "Processing batch item"
    ]
}

weights = [2, 5, 20, 10]  # частота - ERROR реже всего INFO чаще 
start = datetime.now() - timedelta(days=30) #даты за 30 дней с сегодняшнего дня

result = []

for i in range(200):
    level = random.choices(levels, weights = weights, k = 1)[0] # [0] чтобы вернуть не список а строку, учитвается вес и берется 1 строчка
    message = random.choice(messages[level])
   
    random_date = start + timedelta(seconds=random.randint(0, 30*24*3600))  #формат 2026-05-15 10:23:45
    line = f"{random_date.strftime('%Y-%m-%d %H:%M:%S')} {level} {message}"
    result.append(line)


result.sort() #сортировка по дате

os.makedirs("log_data", exist_ok=True)# если нет папки - создать

with open("log_data/app.log", "w") as f:
    for i in result:
        f.write(i + "\n")

print("Лог записан: log_data/app.log")