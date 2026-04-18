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
    count = len(sales)
    # Защита от деления на ноль: если данных нет, avg = 0
    avg = total / count if count > 0 else 0  

    # Группируем суммы по городам
    by_city = {}
    for item in sales:
        city = item['city']
        by_city[city] = by_city.get(city, 0) + item['amount']

    # Находим город с максимальной суммой
    top_city = max(by_city, key=by_city.get) if by_city else "Нет данных"
    
    # Возвращаем 4 значения вместо 2
    return total, avg, by_city, top_city

def save_report(total, avg, by_city, top_city, output_path):
    output_path.parent.mkdir(parents=True, exist_ok=True)
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write("📊 ОТЧЁТ ПО ПРОДАЖАМ\n")
        f.write(f"Общая сумма: {total:.0f}\n")
        f.write(f"Средний чек: {avg:.1f}\n")
        f.write(f"Лидер по выручке: {top_city}\n\n")
        f.write("Детализация по городам (по убыванию):\n")
        # Сортируем города от большего к меньшему
        sorted_cities = sorted(by_city.items(), key=lambda x: x[1], reverse=True)
        for city, amount in sorted_cities:
            f.write(f"  {city}: {amount:.0f}\n")

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
            # Убираем пробелы из ключей и значений # clean_row = {k.strip(): v.strip() for k, v in row.items()}
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
    total, avg, by_city, top_city = calculate_stats(data)  # распаковка 4 значений
    save_report(total, avg, by_city, top_city, output_path)
    print(f"✅ Готово: {len(data)} записей, сумма {total}")