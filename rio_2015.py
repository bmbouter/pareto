import csv

import matplotlib.pyplot as plt

ma_data = '/home/bmbouter/Documents/Research/pareto/data/RIO/ma.csv'
ema_data = '/home/bmbouter/Documents/Research/pareto/data/RIO/ema.csv'
reserve_data = '/home/bmbouter/Documents/Research/pareto/data/RIO/reserve.csv'
time_vary_reserve_data = '/home/bmbouter/Documents/Research/pareto/data/RIO/time_vary_reserve.csv'

all_models_data = '/home/bmbouter/Documents/Research/pareto/data/RIO/all_models_week_99_percentile.csv'

def plot_data(data_file, xkeys, markers, labels, colors, filename, utilization_keys=None, legend_loc=2):
    plt.figure(figsize=(9, 7), dpi=300)
    for i in range(len(xkeys)):
        xkey = xkeys[i]
        marker = markers[i]
        label = labels[i]
        color = colors[i]
        Xs = []
        Ys = []
        with open(data_file, 'rb') as csvfile:
            datareader = csv.DictReader(csvfile, delimiter=',')
            if utilization_keys:
                utilization_key = utilization_keys[i]
            else:
                utilization_key = 'mean_utilization'
            for row in datareader:
                if row[xkey] == '':
                    continue
                Xs.append(float(row[xkey]))
                Ys.append(float(row[utilization_key]))
        plt.scatter(Xs, Ys, color=color, marker=marker, label=label)
    plt.xlabel('Wait Time (s)')
    plt.ylabel('Utilization')
    plt.legend(loc=legend_loc)
    plt.savefig(filename, bbox_inches='tight')
    plt.close()

xkeys = ['wait_time_by_hour_99', 'wait_time_by_day_99', 'wait_time_by_week_99', 'wait_time_mean']
markers = ['.', '*', '^', '+']
labels = ['99th Percentile per Hour', '99th Percentile per Day', '99th Percentile per Week', 'Mean']
colors = ['red', 'green', 'blue', 'black']

filename_base = '/home/bmbouter/Documents/Research/pareto/images/RIO/%s.png'

plot_data(ma_data, xkeys, markers, labels, colors, filename_base % 'ma_multi_timescale', legend_loc=4)
plot_data(ema_data, xkeys, markers, labels, colors, filename_base % 'ema_multi_timescale', legend_loc=4)
plot_data(reserve_data, xkeys, markers, labels, colors, filename_base % 'reserve_multi_timescale', legend_loc=4)
plot_data(time_vary_reserve_data, xkeys, markers, labels, colors, filename_base % 'time_vary_reserve_multi_timescale', legend_loc=4)

all_model_xkeys = ['ma_wait_time_by_week_99', 'ema_wait_time_by_week_99', 'reserve_wait_time_by_week_99', 'time_vary_wait_time_by_week_99']
all_model_labels = ['Moving Average Model', 'Exponential Moving Average Model', 'Reserve Capacity Model', 'Time Variant Reserve Capacity Model']
all_model_utilization_keys = ['ma_utilization', 'ema_utilization', 'reserve_utilization', 'time_vary_reserve_utilization']
plot_data(all_models_data, all_model_xkeys, markers, all_model_labels, colors, filename_base % 'all_models_weekly', utilization_keys=all_model_utilization_keys, legend_loc=4)

#reserve_models_xkeys = ['reserve_wait_time_by_week_99', 'time_vary_wait_time_by_week_99']
#reserve_models_labels = ['Reserve Capacity Model', 'Time Varying Reserve Capacity Model']
#reserve_models_utilization_keys = ['reserve_utilization', 'time_vary_reserve_utilization']
#plot_data(all_models_data, reserve_models_xkeys, markers, reserve_models_labels, colors, filename_base % 'reserve_models_weekly', utilization_keys=reserve_models_utilization_keys, legend_loc=4)
