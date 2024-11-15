from gui.maingui import get_root
import solution
import os

if __name__ == '__main__':  # Only 4 showing running button in Pycharm
    os.chdir(os.path.dirname(__file__))

    for file_name in os.listdir('solutions'):
        if not file_name.endswith('.py'):
            continue
        __import__(f'solutions.{file_name[:-3]}')

    get_root(solution.solutions, solution.solution_sort).mainloop()
