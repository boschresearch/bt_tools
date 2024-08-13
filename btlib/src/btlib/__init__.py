"""Module to visualize behavior trees."""

from typing import Dict, List, Optional

from bs4 import BeautifulSoup

VALUE_MAP = Dict[int, Optional[float]]
VALUE_MAP_COLORS = Dict[int, str]
VALUE_MAP_RETURN_STATES = Dict[int, Optional[List[int]]]
XML_PER_ID = Dict[int, BeautifulSoup]
DIGITS_PER_LEVEL_FBL = 7
