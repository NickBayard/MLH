import sys

def error(message):
    sys.exit('Error: {}'.format(message))

def int_input(txt, min, max):
    while True:
        response = input_with_quit(txt)
        try:
            response = int(response)
        except ValueError:
            print('Response is not valid. Please try again.')
            continue

        if range:
            if response > max or response < min:
                print('Response outside of acceptable range.')
                continue
            else:   
                break
        else:
            break

def input_with_quit(txt):
    response = input(txt)
    if response.lower() == 'q' or response.lower() == 'quit':
        sys.exit()

    return response

