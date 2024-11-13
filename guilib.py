import ttkbootstrap as ttkb


def frac(root, p, q):
    p.grid(row=0, column=1, padx=5, pady=5)
    q.grid(row=2, column=1, padx=5, pady=5)

    width = root.winfo_width()

    # 使用 Canvas 绘制分数线
    canvas = ttkb.Canvas(root, height=10, width=width)
    canvas.create_line(0, 5, width, 5, width=1)  # 画一条水平线
    canvas.grid(row=1, column=1, padx=5, pady=5)


def pow(root, a, x_container, x):
    x.pack(pady=(a.winfo_height(), 0))
    x_container.pack(side=ttkb.LEFT)


class ID(str):
    pass


class FUNC(str):
    pass


def fill_frame_by(root, pattern) -> dict:
    """
    ['比较', (POW, 'π', (ID('x'), IN)), '与', (FRAC, (ID('p'), IN), (ID('q'), IN))] => {'n': var1, 'p': var2, 'q': var3}
    """

    if isinstance(pattern, (str, ttkb.StringVar)):
        ttkb.Label(root, text=pattern)
        return {}

    if isinstance(pattern, list):
        id_dict = {}
        for subpattern in pattern:
            id_dict.update(fill_frame_by(root, subpattern))
        return id_dict

    if isinstance(pattern, tuple):
        if isinstance(pattern[0], ID):
            id_frame = ttkb.Frame(root)
            id_dict = fill_frame_by(id_frame, pattern[1:])
            id_dict[str(ID)] = id_frame

