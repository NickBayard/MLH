import sys

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


def poll_on_method(method, *args, timeout=20, **kwargs):
    retry = 0
    result = None
    ex = Exception('Exception not correctly caught')

    while retry < timeout:
        try:
            result = method(*args, **kwargs)
            break
        except Exception as ex:
            sleep(1)
            retry += 1
    else:
        raise ex

    return result
