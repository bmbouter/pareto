import os
import re

import matplotlib.pyplot as plt
import numpy


# R_VALUES_INCREASING_PATH = '~/Documents/Research/matlab/R_values_increasing/'
# ERROR_PATH = '~/Documents/Research/matlab/sim_vs_numerical_software__error_investigation/'
# TRAFFIC_INTENSITY_PATH = '~/Documents/Research/matlab/increasing_traffic_intensity/'

SIM_VARY_INTENSITY_01 = '~/Documents/Research/matlab/80_percent_violation_sim_only/vary_R_intensity_01/'
SIM_VARY_INTENSITY_05 = '~/Documents/Research/matlab/80_percent_violation_sim_only/vary_R_intensity_05/'
SIM_VARY_INTENSITY_10 = '~/Documents/Research/matlab/80_percent_violation_sim_only/vary_R_intensity_10/'
SIM_VARY_R = '~/Documents/Research/matlab/80_percent_violation_sim_only/vary_traffic_intensity/'


DATA_DIR = os.path.expanduser(SIM_VARY_INTENSITY_01)


def get_queue_length_data():
    pattern_match = re.compile('queue_length_distribution.*({.*})')
    queue_length_data = {}
    for root, sub_folders, filenames in os.walk(DATA_DIR):
        for filename in filenames:
            # if filename == 'results.txt':
            if filename == 'sim_output.txt':
                test_name = root.split(os.sep)[-1]
                full_path = os.path.join(root, filename)
                with open(full_path, 'r') as file_handle:
                    full_text = file_handle.read()
                for match in pattern_match.finditer(full_text):
                    data = eval(match.group(1))
                    queue_length_data[test_name] = data
    return queue_length_data


if __name__ == "__main__":
    if not os.path.isfile('queue_length_charts.py'):
        print 'Please run in the same directory as queue_length_charts.py'
    data = get_queue_length_data()
    x_values = []
    mean_data = []
    percentile_99_data = []
    for key in sorted(data.keys()):
        values_dict = data[key]
        values_list = [values_dict[i] for i in sorted(values_dict.keys())]
        percentile_99_data.append(numpy.percentile(values_list, 99))
        mean_data.append(numpy.mean(values_list))
        x_values.append(re.findall(r'\d+', key)[0])
    chart_path = DATA_DIR + 'queue_depth.png'
    plt.plot(x_values, mean_data, label='Mean')
    plt.plot(x_values, percentile_99_data, label='99th Percentile')
    plt.legend(loc='upper right', shadow=True, fontsize='x-large')
    plt.savefig(chart_path)
    plt.close()