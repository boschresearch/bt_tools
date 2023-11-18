# Copyright (c) 2023 - see the NOTICE file for details

# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at

#     http://www.apache.org/licenses/LICENSE-2.0

# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

from hashlib import sha256
from math import log
import os
import tempfile
from typing import Dict, List, Optional, Union

from btlib import VALUE_MAP
from btlib import VALUE_MAP_COLORS
from btlib import VALUE_MAP_RETURN_STATES
from btlib.bts import NAME
from btlib.common import NODE_STATE
import matplotlib as mpl
import matplotlib.colors as colors
import matplotlib.pyplot as plt
import networkx as nx
from PIL import Image, ImageColor


WIDTH = 1920
HEIGHT = 1080

BG_IMG_FOLDER = os.path.join(
    tempfile.gettempdir(),
    'bt_imgs')
NODE_WIDTH_IN = 2.5
NODE_HEIGHT_IN = 0.8
DPI = 150

L = '99'
M = 'CC'
H = 'FF'
GRAY = f'#{M}{M}{M}'
COLORS_PER_RETURN_STATE = {
    None: GRAY,
    NODE_STATE.SUCCESS: f'#{L}{H}{L}',
    NODE_STATE.FAILURE: f'#{H}{L}{L}',
    NODE_STATE.RUNNING: f'#{H}{H}{L}',
    NODE_STATE.IDLE: f'#{L}{L}{H}',
}
COLORS_PER_RETURN_STATE_VALUE = {
    rs.value: COLORS_PER_RETURN_STATE[rs]
    for rs in NODE_STATE
}
COLORS_PER_RETURN_STATE_VALUE[None] = COLORS_PER_RETURN_STATE[None]


def my_hash(s: object) -> str:
    return sha256(str(s).encode()).hexdigest()[:20]


def _colormap(cm_name: str, value: Optional[float]) -> str:
    if value is None:
        # grey for missing values
        return GRAY
    try:
        cmap = mpl.colormaps[cm_name]
    except AttributeError:
        cmap = mpl.cm.get_cmap(cm_name)
    norm = colors.Normalize(vmin=0, vmax=1)
    rgba = cmap(norm(value))
    # make color brighter
    rgba = (rgba[0] * 0.5 + 0.5,
            rgba[1] * 0.5 + 0.5,
            rgba[2] * 0.5 + 0.5, 1)
    return f'#{int(rgba[0] * 255):02x}'\
        f'{int(rgba[1] * 255):02x}{int(rgba[2] * 255):02x}'


def format_label(attrs: Dict[str, str]) -> str:
    label = f'<b>{attrs[NAME]}</b>'
    attributes = sorted(attrs.keys())
    for attr in attributes:
        if attr == NAME:
            continue
        label += f'<br/><sub>{attr}: {attrs[attr]}</sub>'
    return f'<{label}>'


def _plus_minus_log(x):
    if x == 0:
        return 0
    elif x > 0:
        return log(x + 1)
    else:  # x < 0
        return -log(-x + 1)


def _log_normalize(
    values: Union[VALUE_MAP, VALUE_MAP_RETURN_STATES],
    vmin=0.,
    vmax=1.
) -> Union[VALUE_MAP, VALUE_MAP_RETURN_STATES]:
    ret_values = values.copy()
    # take log to make small values more visible
    min_value = 1E10
    max_value = -1E10
    values_log = {}
    for k, v in values.items():
        if v is None:
            continue
        elif isinstance(v, int) or isinstance(v, float):
            values_log[k] = _plus_minus_log(v)
            min_value = min(values_log[k], min_value)
            max_value = max(values_log[k], max_value)
        elif isinstance(v, list):
            values_log[k] = [_plus_minus_log(x) for x in v]
            min_value = min(min(values_log[k]), min_value)
            max_value = max(max(values_log[k]), max_value)
        else:
            raise ValueError(f'Unknown value type: {type(v)}')
    abs_max = max(abs(min_value), abs(max_value))
    # normalize to [vmin, vmax] with (vmax + vmin) / 2 as center
    center = (vmax + vmin) / 2
    scale = 1 / abs_max * (vmax - vmin) / 2
    for k, v in values_log.items():
        if isinstance(v, int) or isinstance(v, float):
            ret_values[k] = v * scale + center
        elif isinstance(v, list):
            ret_values[k] = [x * scale + center for x in v]  # type: ignore
    return ret_values


def _make_return_value_bargraph(
        retvalues_counts: Optional[List[float]],
        max_count: int):
    if retvalues_counts is None:
        return None
    if not os.path.exists(BG_IMG_FOLDER):
        os.makedirs(BG_IMG_FOLDER)
    img_hash = my_hash(tuple(retvalues_counts))
    img_path = os.path.join(
        BG_IMG_FOLDER,
        f'{img_hash}.png')
    if os.path.exists(img_path):
        return img_path
    plt.figure(figsize=(NODE_WIDTH_IN, NODE_HEIGHT_IN), dpi=DPI)
    plt.axis('off')
    plt.bar(
        x=range(len(retvalues_counts)),
        height=retvalues_counts,
        width=1,
        color=[COLORS_PER_RETURN_STATE[i] for i in NODE_STATE],
        align='edge',
    )
    plt.xlim(0, len(retvalues_counts))
    plt.ylim(0, max_count)
    plt.tight_layout()
    plt.savefig(img_path, bbox_inches='tight', pad_inches=0)
    plt.close()
    return img_path


def _make_history_image(
        states: Optional[List[int]]):
    if states is None:
        return None
    if not os.path.exists(BG_IMG_FOLDER):
        os.makedirs(BG_IMG_FOLDER)
    img_hash = my_hash(tuple(states))
    img_path = os.path.join(
        BG_IMG_FOLDER,
        f'h{img_hash}.png')
    if os.path.exists(img_path):
        return img_path
    width_px = int(NODE_WIDTH_IN * DPI)
    height_px = int(NODE_HEIGHT_IN * DPI)
    img = Image.new('RGB', (len(states), 1), color=(255, 255, 255))
    for i, state in enumerate(states):
        color = ImageColor.getrgb(
            COLORS_PER_RETURN_STATE_VALUE[state])
        img.putpixel((i, 0), color)
    try:
        img = img.resize(
            (width_px, height_px),
            resample=Image.Resampling.NEAREST)
    except AttributeError:
        img = img.resize(
            (width_px, height_px),
            resample=Image.NEAREST)
    img.save(img_path)
    return img_path


def draw_pygraphviz(
    g: nx.Graph,
    fname: str,
    modifier,
):
    A = nx.nx_agraph.to_agraph(g)  # convert to a graphviz graph
    for node in A.nodes():
        # for node attributes see https://graphviz.org/docs/nodes/
        node.attr['id'] = node
        node.attr['shape'] = 'box'
        node.attr['fontname'] = 'Bitstream Vera Sans Mono'
        node.attr['label'] = format_label(g.nodes[int(node)])
        node.attr['width'] = str(NODE_WIDTH_IN)
        node.attr['height'] = str(NODE_HEIGHT_IN)
        if modifier is not None:
            modifier(node)
    # remove labels from edges
    for edge in A.edges():
        edge.attr['label'] = ''
    for ext in ['svg', 'png']:
        A.draw(
            f'{fname}.{ext}',
            prog='dot',
            # ordering of the outedges
            args='-Gordering=out'
        )


def draw_pygraphviz_w_valuemod(
    g: nx.Graph,
    fname: str,
    value_mod: VALUE_MAP,
):
    g = g.copy()
    value_color: VALUE_MAP = _log_normalize(
        value_mod, vmin=0, vmax=1)  # type: ignore
    for node in g.nodes:
        g.nodes[node]['value'] = value_mod[node]
    draw_pygraphviz(
        g,
        fname,
        lambda node: node.attr.update(
            style='filled',
            fillcolor=_colormap('RdYlGn', value_color[int(node)]),
            label=format_label(g.nodes[int(node)]),
        )
    )


def _values_to_str(value_states: Optional[List[int]]) -> str:
    out = ''
    if value_states is None:
        return out
    for state in NODE_STATE:
        out += f'{state.name[0]}: {value_states[state.value-1]} '
    return out


def draw_pygraphviz_w_returnstates(
    g: nx.Graph,
    fname: str,
    value_states: VALUE_MAP_RETURN_STATES
):
    g = g.copy()
    value_bars = _log_normalize(value_states, -1, 1)
    max_count = 1
    for node in g.nodes:
        g.nodes[node]['values'] = _values_to_str(value_states[node])
    if os.path.exists(BG_IMG_FOLDER):
        for f in os.listdir(BG_IMG_FOLDER):
            os.remove(os.path.join(BG_IMG_FOLDER, f))

    def modifier(node):
        if value_bars[int(node)] is None:
            node.attr.update(
                style='filled',
                fillcolor='gray',
            )
        else:
            node.attr.update(
                image=_make_return_value_bargraph(
                    value_bars[int(node)],
                    max_count
                ),
                label=format_label(g.nodes[int(node)])
            )

    draw_pygraphviz(
        g,
        fname,
        modifier=modifier
    )


def draw_pygraphviz_w_colorvalues(
    g: nx.Graph,
    fname: str,
    value_color: VALUE_MAP_COLORS
):
    g = g.copy()
    draw_pygraphviz(
        g,
        fname,
        lambda node: node.attr.update(
            style='filled',
            fillcolor=value_color[int(node)],
        )
    )


def draw_pygraphviz_w_history(
    g: nx.Graph,
    fname: str,
    value_history: VALUE_MAP_RETURN_STATES,
):
    g = g.copy()
    if os.path.exists(BG_IMG_FOLDER):
        for f in os.listdir(BG_IMG_FOLDER):
            os.remove(os.path.join(BG_IMG_FOLDER, f))

    def modifier(node):
        if value_history[int(node)] is None:
            node.attr.update(
                style='filled',
                fillcolor='gray',
            )
        else:
            node.attr.update(
                image=_make_history_image(
                    value_history[int(node)]
                ),
                label=format_label(g.nodes[int(node)])
            )

    draw_pygraphviz(
        g,
        fname,
        modifier=modifier
    )
