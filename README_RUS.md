# Log Analyzer CLI

Инструмент командной строки на Python для парсинга и анализа лог-файлов.
Может использоваться для обработки задач технической поддержки: фильтрация ошибок,
определение пиковых часов сбоев, экспорт диагностических отчётов в CSV.

## Возможности
	- Читать лог-файлы
	- Фильтровать записи по уровню логирования(ERROR, WARNING, INFO, DEBUG)
	- Фильтровать записи по дате
	- Фильтровать записи по ключевому слову в сообщении
	- Подсчитывать статистику сообщений
	- Находить топ n ERROR-сообщения
	- Строить график ошибок по часам
	- Экспортировать результаты в CSV
	- Показывать результат в txt или json формате

## Требования
	- Python 3.10 or higher

	Проект использует только стандартные библиотки Python:
		- argparse
		- csv
		- collections
		- datetime
		- os
		- sys
		- logging
		- json

## Запуск

```bash
# Анализ всего файла
python analyzer.py --file log_data/app.log 

# Анализ логов за определенную дату
python analyzer.py --file log_data/app.log --date 2026-05-20   

# Фильтр по уровню
python analyzer.py --file log_data/app.log --level DEBUG  

# Топ 5 ошибок вместо 3
python analyzer.py --file log_data/app.log --n 5 

# Поиск по ключевому слову
python analyzer.py --file log_data/app.log --keyword "timeout"

# Вывод в JSON
python analyzer.py --file log_data/app.log --format json

# Сохранить CSV в другое место
python analyzer.py --file log_data/app.log --output results/my_report.csv

# Комбинация фильтров 
python analyzer.py --file log_data/app.log --level ERROR --keyword "timeout" --date 2026-05-20 --format json
```

## Пример вывода
```
WARNING: Skipped 2 malformed lines
=== Log Report ===
Total lines: 200
ERROR: 13
WARNING: 32
INFO: 104
DEBUG: 51

Top 3 ERROR messages:
1. Permission denied (x4)
2. SSL handshake failed (x2)
3. Disk full (x2)

=== Hourly Error Distribution ===
00:00  ██ 2
01:00  █ 1
02:00  █ 1
..
INFO: CSV saved: reports/report.csv
```

## Структура проекта
log-analyzer/
├── analyzer.py
├── generate_logs.py
├── log_data/
│   └── app.log
├── reports/
│   └── report.csv
|── README_EN.md
└── README_RU.md