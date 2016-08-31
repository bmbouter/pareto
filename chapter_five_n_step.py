import csv
import os

import matplotlib.pyplot as plt


data_base = '/home/bmbouter/Documents/Research/pareto/data/n_step/gamma_departure/%s/results.csv'
output_image_base = '/home/bmbouter/Documents/Research/pareto/images/chapter_five_paper/n_step_gamma/%s.png'


def plot_model_comparison(timescale_data, timescale, x_label, text_size=10):
    markers = {
                  'autoregressive': 's',
                  'exponential_moving_average': 'v',
                  'moving_average': 'x',
                  'reserve': 'D',
    }
    model_labels = {
        'autoregressive': 'Autoregressive n-step',
        'exponential_moving_average': 'Exponential Moving Average n-step',
        'moving_average': 'Moving Average n-step',
        'reserve': 'Reserve Capacity n-step',
    }
    colors = {
        'autoregressive': 'r',
        'exponential_moving_average': 'b',
        'moving_average': 'g',
        'reserve': 'k',
    }
    full_path = output_image_base % timescale
    plt.figure(figsize=(9, 7), dpi=300)
    for model_name, model_data in timescale_data.iteritems():
        plt.scatter(model_data['x_data'], model_data['y_data'], marker=markers[model_name],
                    label=model_labels[model_name], c=colors[model_name], s=60)
    plt.xlabel(x_label)
    plt.ylabel('Utilization')
    plt.legend(loc=2, prop={'size': text_size}, scatterpoints=1)
    plt.savefig(full_path, bbox_inches='tight')
    plt.close()


def get_timescale_data(timescale):
    model_names = ['autoregressive', 'exponential_moving_average', 'moving_average', 'reserve']
    timescale_data = {}
    for model_name in model_names:
        timescale_data[model_name] = {'x_data': [], 'y_data': []}
        model_results_filename = data_base % model_name
        with open(model_results_filename, 'rb') as csvfile:
            data_reader = csv.DictReader(csvfile)
            for row in data_reader:
                for key in row.keys():
                    row[key.strip()] = row[key].strip()
                    del row[key]
                timescale_data[model_name]['x_data'].append(float(row[timescale]))
                timescale_data[model_name]['y_data'].append(float(row['mean_utilization']))
    return timescale_data


if __name__ == "__main__":
    if not os.path.isfile('chapter_five_n_step.py'):
        print 'Please run in the same directory as chapter_five_n_step.py'
        exit()
    timescales = ['wait_time_by_hour_99', 'wait_time_by_day_99', 'wait_time_by_week_99',
                  'wait_time_mean']
    x_labels = {
                   'wait_time_by_hour_99': 'Waiting Time 99th Percentile Per Hour',
                   'wait_time_by_day_99': 'Waiting Time 99th Percentile Per Day',
                   'wait_time_by_week_99': 'Waiting Time 99th Percentile Per Week',
                   'wait_time_mean': 'Waiting Time Mean'
    }
    for timescale in timescales:
        model_data = get_timescale_data(timescale)
        plot_model_comparison(model_data, timescale, x_labels[timescale])
