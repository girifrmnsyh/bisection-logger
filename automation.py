import pandas as pd
import datetime
import time

# fungsi
fx = '3x-6' # SAMAKAN INI DENGAN y
def f(x):
    y = 3*x-6
    return y

# increment search
def incrementSearch(start, interval):
    log_time = []
    log_left = []
    log_right = []
    log_fleft = []
    log_fright = []
    log_status = []

    left = start
    right = start + interval
    while True:
        time.sleep(1)
        if f(left) * f(right) > 0:
            log_time.append(datetime.datetime.now().strftime("%Y%m%d_%H%M%S"))
            log_left.append(left)
            log_fleft.append(f(left))
            log_fright.append(f(right))
            log_right.append(right)
            log_status.append("invalid")
            left = right
            right = right + interval
            continue
        else:
            log_time.append(datetime.datetime.now().strftime("%Y%m%d_%H%M%S"))
            log_left.append(left)
            log_fleft.append(f(left))
            log_fright.append(f(right))
            log_right.append(right)
            log_status.append("valid")
            break
    return log_time, log_left, log_right, log_fleft, log_fright, log_status   
log_time, log_left, log_right, log_fleft, log_fright, log_status = incrementSearch(-75, 7)

#_________________________________________________________________________________

# execute
execute_path = 'data_log/execute.csv'

with open(execute_path, "a") as file:
    file.write(f'\n{log_time[0]},{fx},{log_left[0]},{log_right[0]-log_left[0]},{log_time[-1]}')

# iteration details
iteration_details_path = 'data_log/iteration_details.csv'

with open(iteration_details_path, "a") as file:
    for i in range(len(log_time)):
        file.write(f"\n{log_time[i]},{log_left[i]},{log_right[i]},{log_fleft[i]},{log_fright[i]},{log_status[i]},{log_time[0]}")

print('data log berhasil di tambahkan.')


