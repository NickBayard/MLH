import sys
from functools import wraps

from time import sleep


def int_input(txt, min, max):
    while True:
        response = input_with_quit(txt)
        try:
            response = int(response)
        except ValueError:
            print('Response is not valid. Please try again.')
            continue

        if response > max or response < min:
            print('Response outside of acceptable range.')
            continue
        else:
            break

    return response


def input_with_quit(txt):
    response = input(txt)
    if response.lower() == 'q' or response.lower() == 'quit':
        sys.exit()

    return response


def poll_on_method(method, timeout=20):
    @wraps(method)
    def wrapper(*args, **kwargs):
        retry = 0
        result = None
        exc = Exception('Exception not correctly caught')

        while retry < timeout:
            try:
                result = method(*args, **kwargs)
                break
            except Exception as ex:
                retry += 1
                exc = ex
                sleep(1)
        else:
            raise exc

        return result
    return wrapper
