import os
import xml.etree.ElementTree as xml
from xml.dom import minidom
 
import matplotlib
import matplotlib.pyplot as plot
import numpy as np
import sympy
 
matplotlib.use("Agg")
 
RESULTS_DIR = 'results'  # имя папки с результатами
 
# название файла скрипта (используется при именовании других файлов)
TASK_NAME = os.path.basename(__file__)[:os.path.basename(__file__).rfind('.')]
 
# имя переменной, относительно которой ведется расчет
VAR = 'x'
 
# задание
TASK = {
    'func': '-cos(x) * cos(pi) * exp(-(x - pi) ** 2)',
    'interval': (-100, 100)
}
 
 
def parse_expression(string_expression: str) -> sympy.Expr:
    """
    Функция, производящая парсинг строки в выражение sympy
    Args:
        string_expression (str): строка, содеражащая текст функции
    Returns:
        sympy.Expr: выражение sympy
    """
    return sympy.parse_expr(string_expression)
 
 
def get_callable(expr, var_name):
    """
    Преобразует выражение sympy в вызываемый объект
    Args:
        expr (sympy.Expr): выражение sympy
        var_name (str): имя переменной, относительно которой будут происходить вычисления
    """
    var = sympy.Symbol(var_name)
    return sympy.lambdify(var, expr, 'numpy')
 
 
def get_data(func, interval, quantity=500):
    """
    Вычисляет значения x и y в заданном интервале
    Args:
        func: функция y = f(x)
        interval: интервал значений по оси x
        quantity (int): количество значений по оси x в заданном интервале
    Returns:
        tuple: значения x и y
    """
    x_values = np.linspace(interval[0], interval[1], quantity)
    return x_values, func(x_values)
 
 
def create_results_dir(dir_name):
    """
    Создает папку с указанным именем. Ничего не делает если папка существует
    Args:
        dir_name (str): имя папки
    Returns:
        None
    """
    try:
        os.mkdir(dir_name)
    except FileExistsError:
        return
 
 
def save_plot(x_values, y_values, directory, task_name):
    """
    Сохраняет изображение графика
    Args:
        x_values: значения по оси абсцисс
        y_values: значения по оси ординат
        directory (str): путь, по которому будет сохранен результат (относительно __main__)
        task_name (str): имя файла (без расширения)
    Returns:
        None
    """
    create_results_dir(RESULTS_DIR)
    plot.plot(x_values, y_values)
    plot.savefig(os.path.join(directory, task_name + '.png'))
 
 
def save_xml_result(x_values, y_values, directory, filename):
    """
    Сохраняет xml документ с данными в формате указанном в задании
    Args:
        x_values: значения xdata
        y_values: значения ydata
        directory (str): путь, по которому будет сохранен результат (относительно __main__)
        task_name (str): имя файла (без расширения)
    Returns:
        None
    """
    doc = xml.Element('data')
    x_data = xml.Element('xdata')
    y_data = xml.Element('ydata')
    doc.append(x_data)
    doc.append(y_data)
 
    for value in x_values:
        element = xml.Element('x')
        element.text = str(value)
        x_data.append(element)
 
    for value in y_values:
        element = xml.Element('y')
        element.text = str(value)
        y_data.append(element)
 
    create_results_dir(RESULTS_DIR)
    with open(os.path.join(directory, filename + '.xml'), 'w') as file:
        file.write(minidom.parseString(xml.tostring(doc)).toprettyxml(indent="\t"))
 
 
def main():
    function = get_callable(parse_expression(TASK['func']), VAR)
    xs, ys = get_data(function, TASK['interval'])
    save_plot(xs, ys, RESULTS_DIR, TASK_NAME)
    save_xml_result(xs, ys, RESULTS_DIR, TASK_NAME)
 
 
# точка входа
if __name__ == '__main__':
    main()
