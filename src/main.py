import solutions
from gui.maingui import get_root
import solution
import os

if __name__ == '__main__':  # Only 4 showing running button in Pycharm
    os.chdir(os.path.dirname(__file__))
    print(os.path.abspath('.'))

    get_root(solution.solutions, solution.solution_sort).mainloop()
