# Usage
## Visualizing a `fbl` log
```
ros2 run bt_view bt_view --bt_log_fbl_fnames <path_to_fbl_log>
```
The tool will output images about 
- the count of calls with the suffix `_count.png` and
- the return states with the suffix `_states.png` 
to the same folder that the `fbl` log is in.

## Calculate coverage
```
ros2 run bt_view bt_view --bt_log_fbl_fnames <path_to_fbl_log> --coverage-threshold <threshold>
```
The tool will count the percentage of nodes that have been executed in the giben fbl file(s). Iff above the threshold, it will return 0.