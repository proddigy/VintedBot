"""
This is the main file of the project. It is responsible for running the whole program.
"""
import threading

from script import vinted_script


def main():
    """
    Runs different scripts depending on marketplace in different threads
    """
    category = 'vetements'
    threading.Thread(target=vinted_script(category)).start()
    # threading.Thread(target=grailed_script).start()


if __name__ == '__main__':
    main()
