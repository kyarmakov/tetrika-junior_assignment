def strict(func):
    def wrapper(*args, **kwargs):
        annotations = func.__annotations__

        for i, (arg_name, arg_type) in enumerate(annotations.items()):
            if i < len(args) and not isinstance(args[i], arg_type):
                raise TypeError(f'Аргумент {arg_name}: "{args[i]}" не соответствует типу {arg_type}')

        for arg_name, arg_value in kwargs.items():
            if arg_name in annotations and not isinstance(arg_value, annotations[arg_name]):
                raise TypeError(f'Аргумент {arg_name}: "{arg_value}" не соответствует типу {annotations[arg_name]}')

        return func(*args, **kwargs)

    return wrapper


@strict
def add_two(a: int, b: int) -> int:
    return a + b


@strict
def check_str(val: str) -> str:
    return val


@strict
def check_diff_types(x: int, y: float, flag: bool):
    return (x, y, flag)


def run_tests():
    # Позитивные проверки
    assert add_two(2, 3) == 5
    assert check_str('Test string') == 'Test string'
    assert check_diff_types(12, 2.71, True) == (12, 2.71, True)

    # Негативные проверки
    try:
        add_two(2.71, 3)
        raise Exception("add_two(2.71, 3) не выбросил исключение TypeError")
    except TypeError as err:
        pass

    try:
        add_two(2, 3.0)
        raise Exception("add_two(2, 3.0) не выбросил исключение TypeError")
    except TypeError as err:
        pass

    try:
        check_str(123)
        raise Exception("check_str не выбросил исключение TypeError")
    except TypeError as err:
        pass

    try:
        check_diff_types(12.5, 2.71, True)
        raise Exception('check_diff_types(12.5, 2.71, True) не выбросил исключение TypeError')
    except TypeError as err:
        pass

    try:
        check_diff_types(12, 'Test string', True)
        raise Exception("check_diff_types(12, 'Test string', True) не выбросил исключение TypeError")
    except TypeError as err:
        pass

    try:
        check_diff_types(12, 3.14, 1)
        raise Exception('check_diff_types(12, 3.14, 1) не выбросил исключение TypeError')
    except TypeError as err:
        pass


if __name__ == "__main__":
    run_tests()
