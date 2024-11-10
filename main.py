# from latex import get_html
# from pisolve import pi_get_latex_ans
# import webbrowser
#
# p = int(input('分子：'))
# q = int(input('分母：'))
#
# with open('res.html', 'w') as fp:
#     fp.write(get_html(pi_get_latex_ans(p, q)))
#
# webbrowser.open('res.html')

from gui import root
root.mainloop()
