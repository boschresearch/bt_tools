import json
import os
import random

from bt_live.ros_node import SingletonBtLiveNode

from django.http import HttpResponse


def index(request):
    node = SingletonBtLiveNode()
    img_path = node.img_path

    fname_svg = img_path + '.svg'
    with open(fname_svg, 'r') as f:
        svg_str = f.read()
    assert len(svg_str)

    fname_js = os.path.join(
        os.path.dirname(__file__),
        '..',
        'bt_live_django',
        'view.js'
    )
    with open(fname_js, 'r') as f:
        js_str = f.read()
    assert len(js_str)

    index_page_str = (
        """
        <!DOCTYPE html>
        <html>
        <head>
        <title>bt_live</title>
        <!-- favicon -->
        <link rel=icon href=favicon.png sizes=32x32 type=image/png>
        <link rel=icon href=favicon.svg sizes=any type=image/svg+xml>
        <!-- jquery -->
        <script src="https://ajax.googleapis.com/ajax/libs/jquery/3.6.4/jquery.min.js"></script>
        <!-- w3 stylesheet -->
        <link rel="stylesheet" href="https://www.w3schools.com/w3css/4/w3.css">
        <link rel="stylesheet" href="https://fonts.googleapis.com/css?family=Lato">
        <link
            rel="stylesheet"
            href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/4.7.0/css/font-awesome.min.css"
        >
        <!-- pan and zoom -->
        <script src='https://unpkg.com/panzoom@9.4.0/dist/panzoom.min.js'></script>
        </head>
        <body>

        <!-- Navbar -->
        <div class="w3-top">
            <div class="w3-bar w3-black w3-card">
                <li class="w3-bar-item w3-padding-large w3-large">bt_live</li>
                <li class="w3-bar-item w3-padding-large w3-right" id="last_update">..</li>
            </div>
        </div>
        <br><br><br>
        """
        +
        f'{svg_str}'
        +
        """
        <script>
        """
        +
        f'{js_str}'
        +
        """
        </script>
        </body>
        </html>
        """)
    return HttpResponse(index_page_str)


def data(request):
    states = {i: random.randint(1, 4) for i in range(100)}
    return HttpResponse(
        json.dumps(states)
    )


def favicon_png(request):
    with open(os.path.join(
        # get_package_share_directory(''), TODO
        'doc',
        'logo32p.png'
    ), 'rb') as f:
        return HttpResponse(f.read(), content_type='image/png')


def favicon_svg(request):
    with open(os.path.join(
        # get_package_share_directory(''), TODO
        'doc',
        'logo.svg'
    ), 'rb') as f:
        return HttpResponse(f.read(), content_type='image/svg+xml')
