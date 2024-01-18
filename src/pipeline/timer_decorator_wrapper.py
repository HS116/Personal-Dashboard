import logging
import time


def timer_decorator(original_function):
    # Function to be later used as a decorators to measure time performance of a particular function

    def wrapper_function(*args, **kwargs):
        logging.info(f"Starting {original_function.__name__}")

        start = time.time()

        return_value = original_function(*args, **kwargs)

        end = time.time()

        logging.info(f"Time taken for {original_function.__name__}: {end-start} seconds")

        return return_value

    return wrapper_function
