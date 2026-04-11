# -*- coding: utf-8 -*-
"""
analyzer.py — простой анализатор продаж без pandas.
Зачем: понять, как код превращает текст в цифры.
"""

# 1. Читаем файл
def read_sales(filepath):
    sales = []
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            for line_num, line in enumerate(f, 1):
                try:
                    date, city, amount_str = line.strip().split(',')
                    amount = int(amount_str)  # Может упасть, если там текст
                    sales.append({'date': date, 'city': city, 'amount': amount})
                except ValueError:
                    print(f" Пропущена строка {line_num}: неверный формат числа → '{line.strip()}'")
                except Exception as e:
                    print(f" Ошибка в строке {line_num}: {e}")
    except FileNotFoundError:
        print(f" Файл не найден: {filepath}")
        return []
    except Exception as e:
        print(f" Ошибка чтения файла: {e}")
        return []
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
        f.write(" ОТЧЁТ ПО ПРОДАЖАМ\n")
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