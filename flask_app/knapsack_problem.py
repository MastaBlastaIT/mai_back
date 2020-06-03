from random import randint


# Генерация списков весов/ценностей
def generate_random_list(n: int, rng: tuple):
    return [randint(*rng) for _ in range(n)]


# Генерация начальных данных
def set_initials(solution_type: str = "random_values", test_values_set_number=0):
    if solution_type == "test_values":
        if test_values_set_number == 0:
            return {
                "total_count": 4,
                "total_weight": 14,
                "weights": [5, 10, 6, 5],
                "values": [3, 5, 4, 2],
            }
        else:
            return {
                "total_count": 3,
                "total_weight": 50,
                "weights": [10, 20, 30],
                "values": [60, 100, 120],
            }
    else:
        stud_n = 24
        total_count = stud_n + 30
        return {
            "total_count": total_count,
            "total_weight": 200 + stud_n * 3,
            "weights": generate_random_list(total_count, (100, 501)),
            "values": generate_random_list(total_count, (10, 41)),
        }


# Перевод начальных значений в кортеж для дальнейшей передачи в качестве аргументов функции
def initials_to_func_args(initials_dict: dict):
    return tuple(initials_dict.values())


# Реализация задачи о рюкзаке 0-1 методом динамического программирования
# Нахождение максимального значения, которое можно положить в рюкзак вместимостью W
def knapsack_problem(
    count: int, carrying_capacity: int, items_weights: list, items_values: list
):
    # m[k][w] — максимальная ценность предметов, полученных из первых k имеющихся предметов, с суммарным весом,
    # не превышающим w.
    m = [[0 for _ in range(carrying_capacity + 1)] for _ in range(count + 1)]

    # Построение двумерного массива m[][] снизу вверх
    for i in range(count + 1):
        for j in range(carrying_capacity + 1):
            if i == 0 or j == 0:
                m[i][j] = 0
            elif items_weights[i - 1] <= j:
                m[i][j] = max(
                    items_values[i - 1] + m[i - 1][j - items_weights[i - 1]],
                    m[i - 1][j],
                )
            else:
                m[i][j] = m[i - 1][j]

    return m[count][carrying_capacity]


if __name__ == "__main__":
    # Тестовые значения
    #
    # Набор 1:
    # Кол-во: 4,
    # Грузоподъемность: 14,
    # Веса: [5, 10, 6, 5],
    # Ценности: [3, 5, 4, 2]
    test_args = initials_to_func_args(set_initials("test_values"))
    print("Решение на наборе тестовых значений 1")
    print(knapsack_problem(*test_args))

    # Набор 2:
    # Кол-во: 3,
    # Грузоподъемность: 50,
    # Веса: [10, 20, 30],
    # Ценности: [60, 100, 120]
    test_args = initials_to_func_args(set_initials("test_values", 1))
    print("Решение на наборе тестовых значений 2")
    print(knapsack_problem(*test_args))

    # Сгенерированные случайным образом значения
    random_args = initials_to_func_args(set_initials("random_values"))
    print("Решение на случайных значениях")
    print(knapsack_problem(*random_args))
