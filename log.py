import os
import time


def write_into_log(message):
    with open(os.getcwd() + '/log/log.txt', 'a') as f:
        print(f"w: {message}")
        f.write(f"{message}\n")
        # print(f"f: {message}")


if __name__ == '__main__':

    start = time.perf_counter()

    write_into_log('one')
    write_into_log('two')
    write_into_log('three')

    finish = time.perf_counter()
    print(f"Finished in {round(finish - start, 2)} second(s).")
