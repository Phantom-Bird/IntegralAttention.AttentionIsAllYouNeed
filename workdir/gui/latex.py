# import matplotlib.pyplot as plt
from config import MATHJAX, BEFORE, AFTER, CANNOT_SOLVE
import ttkbootstrap as ttk


def get_html(latex_code):
    if latex_code is None:
        latex_code = CANNOT_SOLVE
    else:
        latex_code = f'{BEFORE} $${latex_code}$$ {AFTER}'
    return html % (MATHJAX, latex_code)


html = r'''
<!DOCTYPE html>
<html>
<head>
    <script type="text/x-mathjax-config">
        MathJax.Hub.Config({
            extensions: ["tex2jax.js"],
            jax: ["input/TeX", "output/HTML-CSS"],
            tex2jax: {
                inlineMath: [ ['$','$'], ["\\(","\\)"] ],
                displayMath: [ ['$$','$$'], ["\\[","\\]"] ],
                processEscapes: true
            },
            "HTML-CSS": { fonts: ["TeX"] }
        });
    </script>
    <script type="text/javascript" src="%s">
    </script>
</head>
<body>
    <div id="nav">
        %s
    </div>
</body>
</html>
'''

# def render(text, font_size=30):
#     """
#     see https://www.cnblogs.com/qizhou/p/18170083
#     """
#     plt.rc('text', usetex=True)  # 使用 LaTeX 渲染文本
#     plt.rc('font', size=font_size)  # 设置字体大小
#     fig, ax = plt.subplots()
#     txt = ax.text(0.5, 0.5, text, ha='center', va='center', transform=ax.transAxes)
#     ax.axis('off')  # 隐藏坐标轴
#     fig.canvas.draw()  # 需要先绘制图形以确保文本被正确测量
#     bbox = txt.get_window_extent(renderer=fig.canvas.get_renderer())
#     fig.set_size_inches(bbox.width / fig.dpi, bbox.height / fig.dpi)  # 根据文本大小调整图像大小
#     plt.savefig(RENDER_DST, transparent=False, bbox_inches='tight', pad_inches=0)
#
# def show_failed(root):
#     popup = ttk.Toplevel(root)
#     popup.title(CANNOT_SOLVE)
#
#     label = ttk.Label(popup, text=CANNOT_SOLVE)
#     label.pack(pady=10)
#
#     # 使弹出窗口为非模态，不阻塞主窗口
#     popup.transient(root)
#     popup.grab_release()
#
# def show_successful_img(root):
#     popup = ttk.Toplevel(root)
#     popup.title('Attention is all you need')
#
#     label_before = ttk.Label(popup, text=BEFORE, anchor='w', justify='left')
#     label_before.pack()
#
#     label_formula = ttk.Label(popup, image=ttk.PhotoImage(file=RENDER_DST))
#     label_formula.pack()
#
#     label_after = ttk.Label(popup, text=AFTER, anchor='w', justify='left')
#     label_after.pack()
#
#     # 使弹出窗口为非模态，不阻塞主窗口
#     popup.transient(root)
#     popup.grab_release()
#
# def show_latex(root, text):
#     if text is None:
#         show_failed(root)
#     else:
#         render(text)
#         show_successful_img(root)
#
#
# if __name__ == '__main__':
#     root = ttk.Window()
#     show_latex(root, '1+1=2')
#     root.mainloop()


