#!/bin/bash
echo "Запуск тестов и формирование HTML-отчета..."
python3 -m pytest test_analyzer.py --html=report.html --self-contained-html -v
echo "Готово! Отчет сохранен в файл report.html"
