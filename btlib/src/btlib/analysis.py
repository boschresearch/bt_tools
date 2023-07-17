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

from typing import Union

from btlib import VALUE_MAP, VALUE_MAP_RETURN_STATES


def get_coverage(values: Union[VALUE_MAP, VALUE_MAP_RETURN_STATES]) -> float:
    """Get coverage."""
    n_values = len(values)
    if n_values == 0:
        return 0.0
    n_values_covered = 0
    for id_ in values:
        if values[id_] is None:
            continue
        if isinstance(values[id_], list):
            if any(v is not None for v in values[id_]):  # type: ignore
                n_values_covered += (max(values[id_]) > 0)  # type: ignore
        elif isinstance(values[id_], int):
            n_values_covered += (values[id_] > 0)  # type: ignore
        else:
            raise ValueError(f'Unknown type {type(values[id_])}')
    return n_values_covered / n_values
