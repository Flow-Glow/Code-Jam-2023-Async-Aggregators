import time
from typing import Any, Callable


def measure_execution_time(func: Callable) -> Any:
    """
    Measure the execution time of a function

    :param func: function to measure
    :return:
    """

    def wrapper(*args: Any, **kwargs: Any) -> Any:
        """
        Wrapper function

        :param args: arguments
        :param kwargs: keyword arguments
        :return:
        """
        start_time = time.time()
        result = func(*args, **kwargs)
        end_time = time.time()
        execution_time = end_time - start_time
        print(f"Function {func.__name__} took {execution_time:.4f} seconds to execute")
        return result

    return wrapper
