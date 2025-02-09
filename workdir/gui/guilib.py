import sympy
import ttkbootstrap as ttk
from config import DEFAULT_ENTRY_WIDTH, DEFAULT_FRAC_LINE_LENGTH, DEFAULT_UP_PX


def get_tk(easy_tk_item, parent):
    """
    Using get_tk(item, parent) is better than item.get_tk(parent).
    Because get_tk can process non-EasyTkItem objects.
    list, tuple -> LeftPack
    dict -> LeftPackWithID
    """
    if isinstance(easy_tk_item, EasyTkItem):
        return easy_tk_item.get_tk(parent)
    if isinstance(easy_tk_item, (str, ttk.Variable)):
        return ttk.Label(parent, text=easy_tk_item), {}
    if isinstance(easy_tk_item, (list, tuple)):
        return LeftPack(*easy_tk_item).get_tk(parent)
    if isinstance(easy_tk_item, dict):
        return LeftPackWithID(easy_tk_item).get_tk(parent)
    else:
        raise TypeError('Not supported type.')


class EasyTkItem:
    """
    Only a pattern of tk widgets.
    Get tk instance when call get_tk.
    :param id: id of the widget, which will be the key of the id-dict returned in get_tk.
    """

    def __init__(self, *, id=None, **kwargs):
        self.id = id
        self.kwargs = kwargs

    def get_tk(self, parent: ttk.Frame | ttk.Window) \
            -> tuple[ttk.TK_WIDGETS + ttk.TTK_WIDGETS, dict[str, object]]:
        """
        Get an instance
        :param parent: outer frame
        :return: a tuple: (new frame widgets, the id-dict {id: object})
        Override _get_tk method rather than this.
        """
        widget, id_dict = self._get_tk(parent)
        if self.id is not None:
            id_dict[self.id] = widget
        return widget, id_dict

    def _get_tk(self, parent: ttk.Frame | ttk.Window) \
            -> tuple[ttk.TK_WIDGETS + ttk.TTK_WIDGETS, dict[str, object]]:
        """
        Get an instance
        :param parent: outer frame
        :return: a tuple: (new frame widgets, the id-dict {id: object})
        Override this method.
        """
        raise NotImplementedError()


Pattern = EasyTkItem | list['Pattern'] | tuple['Pattern'] | dict[str, 'Pattern']


class Label(EasyTkItem):
    def __init__(self, text, **kw):
        super().__init__(**kw)
        self.text = text

    def _get_tk(self, parent):
        return ttk.Label(parent, text=self.text), {}


class EntryVariable:
    def __init__(self, variable, func=None):
        """
        :param func: default: sympy.Rational
        """
        self.variable = variable
        if func is None:
            func = sympy.Rational
        self.func = func

    def get(self):
        return self.func(self.variable.get())


class Entry(EasyTkItem):
    def __init__(self, vid, process=None, width=DEFAULT_ENTRY_WIDTH, **kw):
        super().__init__(**kw)
        self.vid = vid
        self.width = width
        self.process = process

    def _get_tk(self, parent):
        string_var = ttk.StringVar()
        return (ttk.Entry(parent, textvariable=string_var, width=self.width),
                {self.vid: EntryVariable(string_var, self.process)})


class LeftPack(EasyTkItem):
    def __init__(self, *sub_items, **kw):
        super().__init__(**kw)
        self.sub_items = sub_items

    def _get_tk(self, parent):
        frame = ttk.Frame(parent)
        id_dict = {}

        for item in self.sub_items:
            widget, di = get_tk(item, frame)
            widget.pack(side=ttk.LEFT)
            id_dict.update(di)

        return frame, id_dict


class LeftPackWithID(EasyTkItem):
    def __init__(self, sub_items: dict, **kw):
        super().__init__(**kw)
        self.sub_items = sub_items

    def _get_tk(self, parent):
        frame = ttk.Frame(parent)
        id_dict = {}

        for id, item in self.sub_items.items():
            widget, di = get_tk(item, frame)
            widget.pack(side=ttk.LEFT)
            id_dict.update(di)
            id_dict[id] = widget

        return frame, id_dict


class Frac(EasyTkItem):
    def __init__(self, p, q, line_length=DEFAULT_FRAC_LINE_LENGTH, **kw):
        super().__init__(**kw)
        self.p = p
        self.q = q
        self.line_length = line_length

    def _get_tk(self, parent):
        frame = ttk.Frame(parent)
        p, di1 = get_tk(self.p, frame)
        q, di2 = get_tk(self.q, frame)

        p.grid(row=0, column=0)
        q.grid(row=2, column=0)

        # 使用 Canvas 绘制分数线
        canvas = ttk.Canvas(frame, height=10, width=self.line_length)
        canvas.create_line(0, 5, self.line_length, 5, width=1)
        canvas.grid(row=1, column=0, padx=0, pady=0)

        return frame, di1 | di2


class Up(EasyTkItem):
    def __init__(self, item, up_px=DEFAULT_UP_PX, **kw):
        super().__init__(**kw)
        self.item = item
        self.up_px = up_px

    def _get_tk(self, parent):
        frame = ttk.Frame(parent)

        widget, id_dict = get_tk(self.item, frame)
        widget.grid(row=0, column=0)
        ttk.Frame(frame).grid(row=1, column=0, pady=self.up_px)

        return frame, id_dict


if __name__ == '__main__':
    win = ttk.Window()
    pattern = [
        'e', Up('iπ', 10),
        '+1=',
        Frac(Entry(vid='x', width=5),
             Entry(vid='y', width=5)),
    ]
    frame, id_dict = get_tk(pattern, win)
    frame.pack()
    print(id_dict)
    win.mainloop()
