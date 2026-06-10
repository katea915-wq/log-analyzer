import os
import sys
import csv
from datetime import datetime
from collections import Counter, defaultdict
import argparse
import logging
import json

logging.basicConfig(
    level=logging.INFO,
    format="%(levelname)s: %(message)s"
)
logger = logging.getLogger(__name__)


#==========cоздание папки и аргементов для выбора файла лога===============
def parse_arguments():
    parser = argparse.ArgumentParser(description="Log Analyzer")
    parser.add_argument("--file", required=True, help="Path to log file")
    parser.add_argument("--output", default="reports/report.csv", help="Path for CSV export")
    parser.add_argument("--format", choices=["text", "json"], default="text", help="Output format")


    parser.add_argument("--level", help="Filter by level: ERROR, WARNING, INFO, DEBUG")
    parser.add_argument("--n",type=int,help = "Top n ERROR rows", default= 3)
    parser.add_argument("--date", help="Filter by date: YYYY-MM-DD")
    parser.add_argument("--keyword", help="Filter messages containing keyword")
    return parser.parse_args()

#функция разделения лог-файла на части==================
# 1. дата и время
# 2. уровень сообщения (ERROR/INFO/WARNING/DEBUG)
# 3. содержание сообщения

def parse_line(line: str) -> dict | None:
    part = line.strip().split(" ", maxsplit=3)
    if len(part) < 4:
        return None  #не подходящий формат строки   -->
    return {
        "date": part[0] + " " + part[1],
        "level": part[2],
        "message": part[3]
    }


#функция чтения файла и заполнения логов в спсиок  =======
def load_report(filepath: str) -> list[dict]:
     report = []
     skipped = 0

     with open(filepath, "r", encoding="utf-8") as f:
         for line in f:
             parsed = parse_line(line)

             if parsed:
                 report.append(parsed)
             else:   #-->
                 skipped += 1

     if skipped > 0:
        logger.warning(f"Skipped {skipped} malformed lines")
     return report

#-keyword запись в файл только логов где присутсвует определенгое слово(напр. timeout)==

def filter_level(report: list[dict], level: str) -> list[dict]:
    return [row for row in report if row["level"] == level.upper()]

#-level запись в файл только определенного вида сообщени(ERROR,INFO...)========
def filter_keyword(report: list[dict], keyword: str) -> list[dict]:
    return [row for row in report if  keyword.lower() in row["message"].lower()]

#=Фильтр по дате  =======================

def filter_date(report: list[dict], date: str) -> list[dict]:
    return [row for row in report if row["date"].startswith(date)]


#  Сохранение CSV ================= data,level,message в отдельных столбцах
def save_csv(report: list[dict], output_path: str):
    with open(output_path, "w", newline="") as f1:
        writer = csv.writer(f1, delimiter=";")
        writer.writerow(["date", "level", "message"])
        for row in report:
            writer.writerow([row["date"], row["level"], row["message"]])

# =================Блок статистики==========================================================

#====Топ n ERROR сообщений

def get_top_errors(report: list[dict], n: int):
    error_messages = [row["message"] for row in report if row["level"] == "ERROR"]
    return Counter(error_messages).most_common(n)

#===============ошибки по часам=======

def get_errors_by_hour(report: list[dict]):
    errors_by_hour = defaultdict(int)
    for row in report:
        if row["level"] != "ERROR":
            continue
        dt = datetime.strptime(row["date"], "%Y-%m-%d %H:%M:%S")
        errors_by_hour[dt.hour] += 1
    return errors_by_hour

def main():
    #==создание папки и аргументов для выбора файла лога===============
    args = parse_arguments()
    output_dir = os.path.dirname(args.output)
    if output_dir:
        os.makedirs(output_dir, exist_ok=True)
    #===проверка существования файла===============

    if not os.path.exists(args.file):
        logger.error(f"File not found: {args.file}")
        sys.exit(1)
    #==загрузка логов===============

    report = load_report(args.file)

    #фильтр по слову в сообщении ==============

    if args.keyword:
        report = filter_keyword(report, args.keyword)

    #==фильтр по уровню===============

    if args.level:
        report = filter_level(report, args.level)

    #==фильтр по дате===============
    if args.date:
        report = filter_date(report, args.date)

    #==сохранение csv===============
    save_csv(report, args.output)

    #===подсчет каждого вида сообщения
    counts = Counter(row["level"] for row in report)

    top_errors = get_top_errors(report,args.n)


    #=======Вывод при выборе формата вывода в json
    if args.format == "json":
        output = {
            "total": len(report),
            "counts": dict(counts),
            "top_errors": [{"message": m, "count": c} for m, c in top_errors]
         }
        print(json.dumps(output, indent=2))
    else:  #иначе текстовый вывод(default)

        print("=== Log Report ===")
        print(f"Total lines: {len(report)}")
    #отчет по каждому виду сообщений ====
        for level in ["ERROR", "WARNING", "INFO", "DEBUG"]:
            print(f"{level}: {counts[level]}") 
        print(f"\nTop {args.n} ERROR messages:")
        if top_errors:
            for i, (message, count) in enumerate(top_errors, start=1):
                print(f"{i}. {message} (x{count})")
        else:
            print("No ERROR messages")
    #ERROR по часам ==========
    errors_by_hour =  get_errors_by_hour(report)
    print("\n=== Hourly Error Distribution ===")
    for hour in range(24):
        count = errors_by_hour[hour]
        bar = "█" * count
        print(f"{hour:02d}:00  {bar} {count if count else ''}")

    logger.info(f"CSV saved: {args.output}")


if __name__ == "__main__":
       main()
