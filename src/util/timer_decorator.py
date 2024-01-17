import time
import logging

def timer_decorator(original_function):

    # Function to be later used as a decorators to measure time performance of a particular function

    def wrapper_function(*args, **kwargs):

        start = time.time()

        return_value = original_function(*args, **kwargs)

        end = time.time()

        logging.info(f"Time taken: {end-start} seconds")
        
        return return_value
    
    return wrapper_function