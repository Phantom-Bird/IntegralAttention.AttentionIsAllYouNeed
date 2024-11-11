# import tkinter as tk
import webview
from tkinter import messagebox
from latex import get_html
import ttkbootstrap as ttkb
from solution import BadInput

def get_root(solutions_dict, top_solution_name):
    if not solutions_dict:
        raise ValueError('No any solutions are loaded')

    solution_names = list(solutions_dict.keys())
    solution_names.remove(top_solution_name)
    solution_names.insert(0, top_solution_name)
    ENTRY_WIDTH = 5

    # 定义函数来处理用户输入和生成 HTML
    def generate_html():
        try:
            # 获取用户输入的分子和分母
            p = int(entry_p.get())
            q = int(entry_q.get())
        except (ValueError, BadInput):
            messagebox.showerror("输入错误", "请输入有效的整数！")

        ans_latex = solutions_dict[compare_option_var.get()](p, q).get_latex_ans()
        print('ans:', ans_latex)

        # 生成 HTML 文件
        with open('res.html', 'w', encoding='utf-8') as fp:
            fp.write(get_html(ans_latex))

        # 打开 webview 窗口显示生成的 HTML 文件
        webview.create_window('计算结果', 'res.html', width=800, height=200)
        webview.start()


    # 创建主窗口
    root = ttkb.Window()
    root.title("Attention is all you need")

    largest_frame = ttkb.Frame(root)
    largest_frame.pack(padx=20, pady=10)

    # 设置字体大小
    # style = ttkb.Style()
    font = ("黑体", 20)

    frame_fraction = ttkb.Frame(largest_frame)
    frame_fraction.pack()

    # 输入提示
    label_p = ttkb.Label(frame_fraction, text="输入分数：", font=font)
    label_p.grid(row=0, column=0, padx=10)

    # 创建分数显示框架
    frame_fraction_pq = ttkb.Frame(frame_fraction)
    frame_fraction_pq.grid(row=0, column=1, padx=10)

    # 分子输入框
    entry_p = ttkb.Entry(frame_fraction_pq, font=font, width=ENTRY_WIDTH)
    entry_p.grid(row=0, column=1, padx=5, pady=5)

    # 使用 Canvas 绘制分数线
    canvas = ttkb.Canvas(frame_fraction_pq, height=10, width=20 * ENTRY_WIDTH + 20)
    canvas.create_line(0, 5, 200, 5, width=1)  # 画一条水平线
    canvas.grid(row=1, column=1, padx=5, pady=5)

    # 分母输入框
    entry_q = ttkb.Entry(frame_fraction_pq, font=font, width=ENTRY_WIDTH)
    entry_q.grid(row=2, column=1, padx=5, pady=5)

    # 按钮框架
    button_frame = ttkb.Frame(largest_frame)
    button_frame.pack(pady=10)

    # 下拉菜单
    compare_option_var = ttkb.StringVar()
    compare_option_var.set(top_solution_name)  # 默认选择 π

    compare_menu = ttkb.OptionMenu(button_frame, compare_option_var, *solution_names)
    compare_menu.pack(side=ttkb.LEFT, padx=10)

    # 创建生成按钮
    generate_button = ttkb.Button(button_frame, text="比较", command=generate_html)
    generate_button.pack(side=ttkb.LEFT, padx=10)

    return root

