# -*- coding: utf-8 -*-
"""
analyzer.py — анализатор продаж с защитой от ошибок и неубиваемыми путями.
"""
import sys
from pathlib import Path

# 🔑 КЛЮЧЕВОЙ МОМЕНТ:
# Path(__file__).resolve().parent всегда указывает на папку, где лежит ЭТОТ скрипт.
# Пути теперь не зависят от того, откуда запущен терминал.
SCRIPT_DIR = Path(__file__).resolve().parent
DATA_FILE = SCRIPT_DIR / "data" / "sales.txt"
OUTPUT_FILE = SCRIPT_DIR / "output" / "report.txt"

def read_sales(filepath):
    if not filepath.exists():
        print(f"Файл не найден: {filepath}")
        sys.exit(1)  # Жёстко останавливаем скрипт, если нет входных данных
        
    sales = []
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            for line_num, line in enumerate(f, 1):
                try:
                    date, city, amount_str = line.strip().split(',')
                    sales.append({'date': date, 'city': city, 'amount': int(amount_str)})
                except ValueError:
                    print(f"Пропущена строка {line_num}: неверный формат → '{line.strip()}'")
    except Exception as e:
        print(f"Ошибка чтения: {e}")
        sys.exit(1)
    return sales

def calculate_stats(sales):
    total = sum(item['amount'] for item in sales)
    by_city = {}
    for item in sales:
        by_city[item['city']] = by_city.get(item['city'], 0) + item['amount']
    return total, by_city

def save_report(total, by_city, output_path):
    # Автоматически создаёт папку output/ и все родительские, если их нет
    output_path.parent.mkdir(parents=True, exist_ok=True)
    
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write("ОТЧЁТ ПО ПРОДАЖАМ\n")
        f.write(f"Общая сумма: {total}\n")
        f.write("\nПо городам:\n")
        for city, amount in sorted(by_city.items()):
            f.write(f"  {city}: {amount}\n")

if __name__ == '__main__':
    print(f" Рабочая папка скрипта: {SCRIPT_DIR}")
    
    data = read_sales(DATA_FILE)
    total, stats = calculate_stats(data)
    save_report(total, stats, OUTPUT_FILE)
    
    print(f" Обработано {len(data)} записей")
    print(f" Общая сумма: {total}")
    print(f" Отчёт сохранён в {OUTPUT_FILE}")