# -*- coding: utf-8 -*-
"""
analyzer.py — простой анализатор продаж без pandas.
Зачем: понять, как код превращает текст в цифры.
"""

# 1. Читаем файл
def read_sales(filepath):
    """Читает текстовый файл и возвращает список словарей."""
    sales = []
    with open(filepath, 'r', encoding='utf-8') as f:
        for line in f:
            # Убираем перенос строки и разбиваем по запятой
            date, city, amount = line.strip().split(',')
            # Превращаем сумму в число
            sales.append({
                'date': date,
                'city': city,
                'amount': int(amount)
            })
    return sales

# 2. Считаем статистику
def calculate_stats(sales):
    """Возвращает общую сумму и среднее по городам."""
    total = sum(item['amount'] for item in sales)
    by_city = {}
    for item in sales:
        city = item['city']
        by_city[city] = by_city.get(city, 0) + item['amount']
    return total, by_city

# 3. Сохраняем отчёт
def save_report(total, by_city, output_path):
    """Записывает итоги в текстовый файл."""
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write("📊 ОТЧЁТ ПО ПРОДАЖАМ\n")
        f.write(f"Общая сумма: {total}\n")
        f.write("\nПо городам:\n")
        for city, amount in sorted(by_city.items()):
            f.write(f"  {city}: {amount}\n")

# 4. Запускаем всё вместе
if __name__ == '__main__':
    # Пути к файлам
    input_file = 'data/sales.txt'
    output_file = 'output/report.txt'
    
    # Выполняем шаги
    data = read_sales(input_file)
    total, stats = calculate_stats(data)
    save_report(total, stats, output_file)
    
    # Печатаем в консоль для быстрой проверки
    print(f" Обработано {len(data)} записей")
    print(f" Общая сумма: {total}")
    print(f" Отчёт сохранён в {output_file}")