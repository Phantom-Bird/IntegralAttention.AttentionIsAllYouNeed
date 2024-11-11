# import tkinter as tk
import webview
from tkinter import messagebox
from latex import get_html
from pisolve import PiSolution
from esolve import ESolution
import ttkbootstrap as tkb

function_dict = {
    'π': PiSolution(),
    'e': ESolution(),
}

# 定义函数来处理用户输入和生成 HTML
def generate_html():
    try:
        # 获取用户输入的分子和分母
        p = int(entry_p.get())
        q = int(entry_q.get())
    except ValueError:
        messagebox.showerror("输入错误", "请输入有效的整数！")

    # 生成 HTML 文件
    with open('res.html', 'w', encoding='utf-8') as fp:
        fp.write(get_html(function_dict[compare_option_var.get()].get_latex_ans(p, q)))

    # 打开 webview 窗口显示生成的 HTML 文件
    webview.create_window('计算结果', 'res.html', width=800, height=200)
    webview.start()


# 创建主窗口
root = tkb.Window()
root.title("Attention is all you need")

largest_frame = tkb.Frame(root)
largest_frame.pack(padx=20, pady=10)

# 设置字体大小
style = tkb.Style()
font = ("黑体", 20)

frame_fraction = tkb.Frame(largest_frame)
frame_fraction.pack()

# 输入提示
label_p = tkb.Label(frame_fraction, text="输入分数：", font=font)
label_p.grid(row=0, column=0, padx=10)

# 创建分数显示框架
frame_fraction_pq = tkb.Frame(frame_fraction)
frame_fraction_pq.grid(row=0, column=1, padx=10)

# 分子输入框
entry_p = tkb.Entry(frame_fraction_pq, font=font, width=3)
entry_p.grid(row=0, column=1, padx=5, pady=5)

# 使用 Canvas 绘制分数线
canvas = tkb.Canvas(frame_fraction_pq, height=10, width=80)
canvas.create_line(0, 5, 200, 5, width=1)  # 画一条水平线
canvas.grid(row=1, column=1, padx=5, pady=5)

# 分母输入框
entry_q = tkb.Entry(frame_fraction_pq, font=font, width=3)
entry_q.grid(row=2, column=1, padx=5, pady=5)

# 按钮框架
button_frame = tkb.Frame(largest_frame)
button_frame.pack(pady=10)

# 下拉菜单
compare_option_var = tkb.StringVar()
compare_option_var.set(list(function_dict.keys())[0])  # 默认选择 π

compare_menu = tkb.OptionMenu(button_frame, compare_option_var, *list(function_dict.keys()))
compare_menu.pack(side=tkb.LEFT, padx=10)

# 创建生成按钮
generate_button = tkb.Button(button_frame, text="比较", command=generate_html)
generate_button.pack(side=tkb.LEFT, padx=10)

