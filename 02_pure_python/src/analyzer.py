# -*- coding: utf-8 -*-
import csv
import sys
import argparse
from pathlib import Path

# Пути строятся от папки проекта, а не от папки src/
SCRIPT_DIR = Path(__file__).resolve().parent  # .../02_pure_python/src/
PROJECT_DIR = SCRIPT_DIR.parent               # .../02_pure_python/
DEFAULT_INPUT = PROJECT_DIR / "data" / "messy_sales.csv"
DEFAULT_OUTPUT = PROJECT_DIR / "output" / "messy_report.txt"

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

def read_messy_csv(filepath):
    records = []
    skipped = 0
    with open(filepath, 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for i, row in enumerate(reader, 1):
            # Убираем пробелы из ключей и значений
            clean_row = {k.strip(): v.strip() for k, v in row.items()}
            amount_str = clean_row.get('amount', '').strip()
            
            try:
                amount = float(amount_str)
            except ValueError:
                skipped += 1
                print(f"⚠️ Строка {i}: пропущена (amount='{amount_str}')")
                continue
                
            records.append({
                'date': clean_row['date'],
                'city': clean_row['city'],
                'amount': amount,
                'manager': clean_row.get('manager', 'Unknown')
            })
    print(f"📊 Загружено: {len(records)} | Пропущено: {skipped}")
    return records
if __name__ == '__main__':
    print(f"🔍 Запуск: {__file__}")
    args = parse_args()  # ← КРИТИЧЕСКИ ВАЖНО: здесь скрипт "слушает" консоль
    
    input_path = Path(args.input)
    output_path = Path(args.output)
    print(f"📂 Input: {input_path}")
    print(f"📁 Output: {output_path}")
    
    data = read_messy_csv(input_path)
    total, stats = calculate_stats(data)
    save_report(total, stats, output_path)
    print(f"✅ Готово: {len(data)} записей, сумма {total}")