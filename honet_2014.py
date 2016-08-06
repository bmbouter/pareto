import csv

import matplotlib.pyplot as plt

fixed_data = '/home/bmbouter/Documents/Research/pareto/data/fixed.csv'
reserve_data = '/home/bmbouter/Documents/Research/pareto/data/reserve.csv'
ema_data = '/home/bmbouter/Documents/Research/pareto/data/ema.csv'

all_models_data = '/home/bmbouter/Documents/Research/pareto/data/HONET/honet_all_models_week_99_percentile.csv'

def plot_data(data_file, xkeys, markers, labels, filename, utilization_keys=None, legend_loc=2):
    plt.figure(figsize=(9, 7), dpi=300)
    for i in range(len(xkeys)):
        xkey = xkeys[i]
        marker = markers[i]
        label = labels[i]
        Xs = []
        Ys = []
        with open(data_file, 'rb') as csvfile:
            datareader = csv.DictReader(csvfile, delimiter=',')
            if utilization_keys:
                utilization_key = utilization_keys[i]
            else:
                utilization_key = 'utilization'
            for row in datareader:
                if row[xkey] == '':
                    continue
                Xs.append(float(row[xkey]))
                Ys.append(float(row[utilization_key]))
        plt.scatter(Xs, Ys, color='black', marker=marker, label=label)
    plt.xlabel('Blocking Probability')
    plt.ylabel('Utilization')
    plt.legend(loc=legend_loc)
    plt.savefig(filename, bbox_inches='tight')
    plt.close()

xkeys = ['bp_by_hour_99', 'bp_by_day_99', 'bp_by_week_99', 'bp_batch_mean']
markers = ['.', '*', '^', '+']
labels = ['99th Percentile per Hour', '99th Percentile per Day', '99th Percentile per Week', 'Annual Mean']

filename_base = '/home/bmbouter/Documents/Research/pareto/images/HONET/%s.png'

plot_data(fixed_data, xkeys, markers, labels, filename_base % 'fixed_multi_timescale')
plot_data(reserve_data, xkeys, markers, labels, filename_base % 'reserve_multi_timescale', legend_loc=4)
plot_data(ema_data, xkeys, markers, labels, filename_base % 'ema_multi_timescale', legend_loc=4)

all_model_xkeys = ['fixed_bp_by_week_99', 'ema_bp_by_week_99', 'reserve_bp_by_week_99']
all_model_labels = ['Fixed Capacity Model', 'Exponential Moving Average Model', 'Reserve Capacity Model']
all_model_utilization_keys = ['fixed_utilization', 'ema_utilization', 'reserve_utilization']
plot_data(all_models_data, all_model_xkeys, markers, all_model_labels, filename_base % 'all_models_weekly', utilization_keys=all_model_utilization_keys, legend_loc=4)