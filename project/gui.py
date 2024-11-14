# import tkinter as tk
import sympy
import webview
from tkinter import messagebox
from latex import get_html
import ttkbootstrap as ttk
from solution import BadInput
from guilib import get_tk, EntryVariable
from config import SCALING

USER_THEMES = {
    "supercosmo": {
        "type": "light",
        "colors": {
            "border": "#ffffff",
        }
    }
}



def get_root(solutions_dict, solution_sort):
    if not solutions_dict:
        raise ValueError('No any solutions are loaded')

    # 定义函数来处理用户输入和生成 HTML
    def generate_html():
        try:
            tab_id = nb.select()
            name = nb.tab(tab_id, 'text')
            args_dict = {
                key: value.get()
                for key, value in nb_id_dicts[name].items()
                if isinstance(value, EntryVariable)
            }
        except (TypeError, ValueError):
            messagebox.showerror("输入错误", "请输入有效的数字！")
            return

        print(args_dict)
        try:
            ans_latex = solutions_dict[name](**args_dict).get_latex_ans()
        except BadInput:
            messagebox.showerror("输入错误", "请输入有效的数字！")
            return

        print('ans:', ans_latex)

        # 生成 HTML 文件
        with open('res.html', 'w', encoding='utf-8') as fp:
            fp.write(get_html(ans_latex))

        # 打开 webview 窗口显示生成的 HTML 文件
        webview.create_window('计算结果', 'res.html', width=800, height=200)
        webview.start()

    # 创建主窗口
    root = ttk.Window(scaling=SCALING)
    root.title("Attention is all you need")

    style = ttk.Style()

    # 设置Notebook的边框为0，即不显示边框
    # style.configure('TNotebook', borderwidth=0, relief='flat')
    # style.configure('TNotebook.Tab', padding=[10, 5])

    # 设置字体大小
    # style = ttkb.Style()
    # font = ("黑体", 20)

    nb_id_dicts = {}
    # {name: {id: Widget | Variable}}
    nb = ttk.Notebook(root, style='primary')
    for name in solution_sort:
        tab_frame = ttk.Frame(root)
        widget, nb_id_dicts[name] = get_tk(solutions_dict[name].gui, tab_frame)
        widget.pack()

        generate_button = ttk.Button(tab_frame, text="比较", command=generate_html)
        generate_button.pack(pady=(10, 0))

        nb.add(tab_frame, text=name, sticky='n', padding=10)
    nb.pack(pady=0)

    return root

