import tkinter as tk
import webview
from tkinter import messagebox
from latex import get_html
from pisolve import pi_get_latex_ans

# 定义函数来处理用户输入和生成 HTML
def generate_html():
    try:
        # 获取用户输入的分子和分母
        p = int(entry_p.get())
        q = int(entry_q.get())

        # 生成 HTML 文件
        with open('res.html', 'w', encoding='utf-8') as fp:
            fp.write(get_html(pi_get_latex_ans(p, q)))

        # 打开 webview 窗口显示生成的 HTML 文件
        webview.create_window('计算结果', 'res.html', width=800, height=200)
        webview.start()
    except ValueError:
        messagebox.showerror("输入错误", "请输入有效的整数！")


# 创建主窗口
root = tk.Tk()
root.title("Attention is all you need")

# 设置字体大小
font = ("黑体", 20)

frame_fraction = tk.Frame(root)
frame_fraction.pack()

# 输入提示
label_p = tk.Label(frame_fraction, text="输入分数：", font=font)
label_p.grid(row=0, column=0, padx=0, pady=0)

# 创建分数显示框架
frame_fraction_pq = tk.Frame(frame_fraction)
frame_fraction_pq.grid(row=0, column=1, padx=0, pady=0)

# 分子输入框
entry_p = tk.Entry(frame_fraction_pq, font=font, width=3)
entry_p.grid(row=0, column=1, padx=5, pady=5)

# 使用 Canvas 绘制分数线
canvas = tk.Canvas(frame_fraction_pq, height=10, width=80)
canvas.create_line(0, 5, 200, 5, width=1)  # 画一条水平线
canvas.grid(row=1, column=1, padx=5, pady=5)

# 分母输入框
entry_q = tk.Entry(frame_fraction_pq, font=font, width=3)
entry_q.grid(row=2, column=1, padx=5, pady=5)

# 创建生成按钮
generate_button = tk.Button(root, text="和 π 比较", command=generate_html, font=font)
generate_button.pack(pady=10)

