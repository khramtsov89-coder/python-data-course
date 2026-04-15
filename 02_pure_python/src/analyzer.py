# -*- coding: utf-8 -*-
import sys
import argparse
from pathlib import Path

# Пути строятся от папки проекта, а не от папки src/
SCRIPT_DIR = Path(__file__).resolve().parent  # .../02_pure_python/src/
PROJECT_DIR = SCRIPT_DIR.parent               # .../02_pure_python/
DEFAULT_INPUT = PROJECT_DIR / "data" / "sales.txt"
DEFAULT_OUTPUT = PROJECT_DIR / "output" / "report.txt"

def read_sales(filepath):
    if not filepath.exists():
        print(f"❌ Файл не найден: {filepath}")
        sys.exit(1)
    sales = []
    with open(filepath, 'r', encoding='utf-8') as f:
        for line_num, line in enumerate(f, 1):
            try:
                date, city, amount_str = line.strip().split(',')
                sales.append({'date': date, 'city': city, 'amount': int(amount_str)})
            except ValueError:
                print(f"⚠️ Пропущена строка {line_num}: '{line.strip()}'")
    return sales

def calculate_stats(sales):
    total = sum(item['amount'] for item in sales)
    by_city = {}
    for item in sales:
        by_city[item['city']] = by_city.get(item['city'], 0) + item['amount']
    return total, by_city

def save_report(total, by_city, output_path):
    output_path.parent.mkdir(parents=True, exist_ok=True)
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write("📊 ОТЧЁТ ПО ПРОДАЖАМ\n")
        f.write(f"Общая сумма: {total}\n\nПо городам:\n")
        for city, amount in sorted(by_city.items()):
            f.write(f"  {city}: {amount}\n")

def parse_args():
    parser = argparse.ArgumentParser(description="📊 Анализатор продаж")
    parser.add_argument("--input", default=str(DEFAULT_INPUT), help="Входной файл")
    parser.add_argument("--output", default=str(DEFAULT_OUTPUT), help="Файл отчёта")
    return parser.parse_args()

if __name__ == '__main__':
    print(f"🔍 Запуск: {__file__}")
    args = parse_args()  # ← КРИТИЧЕСКИ ВАЖНО: здесь скрипт "слушает" консоль
    
    input_path = Path(args.input)
    output_path = Path(args.output)
    print(f"📂 Input: {input_path}")
    print(f"📁 Output: {output_path}")
    
    data = read_sales(input_path)
    total, stats = calculate_stats(data)
    save_report(total, stats, output_path)
    print(f"✅ Готово: {len(data)} записей, сумма {total}")