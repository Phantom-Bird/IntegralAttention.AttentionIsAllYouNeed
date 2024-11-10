import matplotlib.pyplot as plt
import webbrowser


def show(latex_code):
    plt.text(0.5, 0.5, latex_code)
    plt.axis('off')
    plt.show()


def get_html(latex_code):
    return r'''
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
            <script type="text/javascript" src="http://mathjax.josephjctang.com/MathJax.js?config=TeX-MML-AM_HTMLorMML">
            </script>
        </head>
        <body>
            <div id="nav">
                %s
            </div>
        </body>
        </html>
    ''' % latex_code

