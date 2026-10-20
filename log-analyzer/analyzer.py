import argparse
import json
import csv
import sys
from datetime import datetime
from collections import Counter

# Функция для проверки и парсинга одной строки
def parse_line(line):
    parts = line.strip().split(' | ')
    if len(parts) != 5:
        return None, "Неверное количество полей (должно быть 5)"

    ts_str, level, source, code, msg = parts
    level = level.strip()
    source = source.strip()
    code = code.strip()
    msg = msg.strip()

    # Проверка уровня
    if level not in ['TRACE', 'DEBUG', 'INFO', 'WARN', 'ERROR']:
        return None, f"Неверный уровень: {level}"

    # Проверка пустых полей
    if not code or not msg:
        return None, "Пустое поле eventCode или message"

    # Проверка времени (ISO 8601)
    try:
        # Заменяем Z на +00:00 для корректного парсинга в Python
        dt = datetime.fromisoformat(ts_str.replace('Z', '+00:00'))
    except ValueError:
        return None, f"Неверный формат времени: {ts_str}"

    return {
        'timestamp': dt,
        'level': level,
        'source': source,
        'code': code,
        'message': msg
    }, None

def main():
    # Настройка аргументов командной строки
    parser = argparse.ArgumentParser(description="Анализатор логов")
    parser.add_argument('--input', required=True, help="Путь к файлу лога")
    parser.add_argument('--from', dest='from_time', help="Начало интервала (ISO 8601)")
    parser.add_argument('--to', dest='to_time', help="Конец интервала (ISO 8601)")
    parser.add_argument('--level', help="Фильтр по уровню (ERROR, INFO и т.д.)")
    parser.add_argument('--source', help="Фильтр по источнику")
    parser.add_argument('--top', type=int, default=3, help="Топ-N кодов ошибок")
    parser.add_argument('--format', choices=['json', 'csv'], default='json', help="Формат вывода")
    parser.add_argument('--output', help="Файл для сохранения результата")

    args = parser.parse_args()


    from_dt = None
    to_dt = None
    try:
        if args.from_time:
            from_dt = datetime.fromisoformat(args.from_time.replace('Z', '+00:00'))
        if args.to_time:
            to_dt = datetime.fromisoformat(args.to_time.replace('Z', '+00:00'))
    except ValueError:
        print("Ошибка: Неверный формат даты в аргументах --from или --to")
        sys.exit(1)

    total_lines = 0
    valid_lines = 0
    invalid_lines = 0
    filtered_events = []

    levels_count = Counter()
    sources_count = Counter()
    error_codes = Counter()

    # Чтение файла построчно
    try:
        with open(args.input, 'r', encoding='utf-8') as f:
            for line_num, line in enumerate(f, 1):
                if not line.strip():
                    continue

                total_lines += 1
                data, error = parse_line(line)

                if error:
                    invalid_lines += 1
                    print(f"[Строка {line_num}] Ошибка: {error}. Текст: {line.strip()[:50]}...")
                    continue

                valid_lines += 1
                levels_count[data['level']] += 1
                sources_count[data['source']] += 1

                if data['level'] == 'ERROR':
                    error_codes[data['code']] += 1

                # Применяем фильтры
                if from_dt and data['timestamp'] < from_dt:
                    continue
                if to_dt and data['timestamp'] >= to_dt:
                    continue
                if args.level and data['level'] != args.level:
                    continue
                if args.source and data['source'] != args.source:
                    continue

                filtered_events.append({
                    'timestamp': data['timestamp'].isoformat(),
                    'level': data['level'],
                    'source': data['source'],
                    'eventCode': data['code'],
                    'message': data['message']
                })

    except FileNotFoundError:
        print(f"Ошибка: Файл '{args.input}' не найден.")
        sys.exit(1)

    # Формируем итоговый отчет
    top_errors = error_codes.most_common(args.top)

    report = {
        'statistics': {
            'total_lines': total_lines,
            'valid_lines': valid_lines,
            'invalid_lines': invalid_lines,
            'filtered_events_count': len(filtered_events)
        },
        'summary': {
            'by_level': dict(levels_count),
            'by_source': dict(sources_count),
            'top_errors': dict(top_errors)
        },
        'filtered_events': filtered_events
    }

    # Вывод в терминал (краткая сводка)
    print("\n--- СВОДКА ---")
    print(f"Всего строк: {total_lines}")
    print(f"Корректных: {valid_lines}")
    print(f"Ошибочных: {invalid_lines}")
    print(f"Прошло фильтры: {len(filtered_events)}")
    print(f"Топ-{args.top} ошибок: {dict(top_errors)}")

    # Сохранение в файл
    if args.output:
        if args.format == 'json':
            with open(args.output, 'w', encoding='utf-8') as f:
                json.dump(report, f, ensure_ascii=False, indent=2)
        elif args.format == 'csv':
            with open(args.output, 'w', encoding='utf-8', newline='') as f:
                writer = csv.writer(f)
                writer.writerow(['timestamp', 'level', 'source', 'eventCode', 'message'])
                for ev in filtered_events:
                    writer.writerow([ev['timestamp'], ev['level'], ev['source'], ev['eventCode'], ev['message']])
        print(f"Результат сохранен в {args.output} ({args.format})")

if __name__ == '__main__':
    main()
