MATHJAX = 'mathjax-full/es5/tex-mml-chtml.js'

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
            <script type="text/javascript" src="%s">
            </script>
        </head>
        <body>
            <div id="nav">
                %s
            </div>
        </body>
        </html>
    ''' % (MATHJAX, latex_code)

