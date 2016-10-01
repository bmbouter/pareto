import os
import re

import matplotlib.pyplot as plt


SIM_VARY_R = {
    'paths':
        [
            '~/Documents/Research/matlab/80_percent_violation_sim_only/vary_R_intensity_01/',
            '~/Documents/Research/matlab/80_percent_violation_sim_only/vary_R_intensity_05/',
            '~/Documents/Research/matlab/80_percent_violation_sim_only/vary_R_intensity_10/',
        ],
    'x_label': 'R value',
    'output_image': '~/Documents/Research/matlab/80_percent_violation_sim_only/vary_R_diff_intensity.png',
}

SIM_VARY_INTENSITY_80 = {
    'paths':
        [
            '~/Documents/Research/matlab/80_percent_violation_sim_only/vary_traffic_intensity/'
        ],
    'x_label': 'Offered Traffic Load (Rho)',
    'output_image': '~/Documents/Research/matlab/80_percent_violation_sim_only/increase_intensity.png',
}

SIM_VARY_INTENSITY_20 = {
    'paths':
        [
            '~/Documents/Research/matlab/20_percent_violation_sim_only/vary_traffic_intensity/'
        ],
    'x_label': 'Offered Traffic Load (Rho)',
    'output_image': '~/Documents/Research/matlab/20_percent_violation_sim_only/increase_intensity.png',
}

SIM_M_M_S_20 = {
    'paths':
        [
            '~/Documents/Research/matlab/80_vs_20_queue_depth_data/20_percent_vary_traffic_intensity_M_M_20'
        ],
    'x_label': 'Offered Traffic Load (Rho)',
    'output_image': '~/Documents/Research/matlab/20_percent_violation_sim_only/20_percent_case.png',
}

SIM_M_M_S_80 = {
    'paths':
        [
            '~/Documents/Research/matlab/80_vs_20_queue_depth_data/80_percent_vary_traffic_intensity_M_M_20'
        ],
    'x_label': 'Offered Traffic Load (Rho)',
    'output_image': '~/Documents/Research/matlab/20_percent_violation_sim_only/80_percent_case.png',
}

MARKOV_VARY_INTENSITY = {
    'paths':
        [
            '~/Documents/Research/matlab/queue_lengths'
        ],
    'x_label': 'Offered Traffic Load (Rho)',
    'output_image': '~/Documents/Research/matlab/queue_lengths/queue_length_increase_rho.png',
    'Markov': True,
}


CURRENT_RUN = MARKOV_VARY_INTENSITY


def plot_single_folder(image_output_path, queue_length_pdf):
    """
    Plot the queue length data for a single run.

    :param image_output_path: The full path to the text file containing the data. The output image
                              will be a peer of this file.
    :type image_output_path: basestring

    :param queue_length_pdf: A list of queue length probabilities by position. queue_length_pdf[0]
                             is the probability of 0 queue length. queue_length_pdf[1] is the
                             probability of a queue length of 1 and so forth.
    :type queue_length_pdf: A list of floats 0.0 <= queue_length_pdf <= 1.0
    """
    plt.plot(range(len(queue_length_pdf)), queue_length_pdf)
    plt.xlabel(CURRENT_RUN['x_label'])
    plt.ylabel('Queue Length')
    plt.legend(loc='best', shadow=True, fontsize='medium')
    plt.savefig(image_output_path)
    plt.close()


def plot_single_series(image_output_path, series_data):
    """
    Plots a single series of data.

    :param image_output_path: The full path to the text file containing the data. The output image
                              will be a peer of this file.
    :type image_output_path: basestring

    :param series_data: A dictionary of all data within a series. The dict has 3 keys:
                        'mean_values', '99_percentile_values', and 'x_values'. Each key contains a
                        list of numeric values.
    :type series_data: dict with keys 'mean_values', '99_percentile_values', and 'x_values' which
                       each contain a list.
    """
    plt.plot(series_data['x_values'], series_data['mean_values'], label='Mean')
    plt.plot(series_data['x_values'], series_data['99_percentile_values'], label='99th Pecentile')
    plt.xlabel(CURRENT_RUN['x_label'])
    plt.ylabel('Queue Length')
    plt.legend(loc='best', shadow=True, fontsize='medium')
    plt.savefig(image_output_path)
    plt.close()


def get_data_pattern():
    """
    Returns the correct, compiled regular expression object for the run.

    This object is different depending on if it is a markov run or not.

    :return: The correct compiled regular expression
    """
    if is_markov():
        return re.compile('queue_length_distribution.*({.*})')
    else:
        return re.compile('queue_depth probabilities.*(\[.*\])')


def get_list_from_dict(data):
    """
    Return a list of data from the dict.

    A Markov run outputs its queue length data as a dictionary with the keys being the queue length
    and the values being the probability. This returns a list with the probability at the queue
    length position.

    :return: A list of queue length probabiliteis with the queue length being the list position
    """
    if not is_markov():
        raise RuntimeError('The dict->list transform is for Markov runs only. Something is wrong.')
    sorted_queue_lengths = sorted(data.keys())
    return [data[queue_length] for queue_length in sorted_queue_lengths]


def get_and_plot_queue_length_data(full_path):
    """
    Parses and plots the queue length probability data from the text file.

    It also calls plot of the data that is fetched.

    :param full_path: The full path to the text file with the data
    :type full_path: basestring

    :return: A list of queue length probabilities by position. queue_length_pdf[0] is the
             probability of 0 queue length. queue_length_pdf[1] is the probability of a queue
             length of 1 and so forth.
    :rtype: A list of floats 0.0 <= queue_length_pdf <= 1.0
    """
    pattern_match = get_data_pattern()
    with open(full_path, 'r') as file_handle:
        full_text = file_handle.read()
    for match in pattern_match.finditer(full_text):
        data = eval(match.group(1))
    if is_markov():
        data = get_list_from_dict(data)
    image_output_path = os.sep.join([os.path.dirname(full_path), 'queue_length.png'])
    plot_single_folder(image_output_path, data)
    return data


def compute_mean_and_percentile(queue_length_pdf):
    """
    Takes a list of queue length probabilities and return the mean and 99th percentile queue length

    :param queue_length_pdf: A list of queue length probabilities by position. queue_length_pdf[0]
                             is the probability of 0 queue length. queue_length_pdf[1] is the
                             probability of a queue length of 1 and so forth.
    :type queue_length_pdf: A list of floats 0.0 <= queue_length_pdf <= 1.0

    :return: Dictionary with the mean queue length keyed as 'mean' and the 99th percentile of queue
             length keyed as '99_percentile'. Each value is a list.
    :rtype: dictionary containing keys 'mean' and '99_percentile'
    """
    queue_length_sums = []
    for queue_length in range(len(queue_length_pdf)):
        queue_length_sums.append(queue_length * queue_length_pdf[queue_length])
    mean_queue_length = sum(queue_length_sums)

    accumulator = 0
    for queue_length in range(len(queue_length_pdf)):
        accumulator += queue_length_pdf[queue_length]
        if accumulator > 0.99:
            percentile_99 = queue_length
            break

    return {'mean': mean_queue_length, '99_percentile': percentile_99}


def is_markov():
    """
    Return True if CURRENT_RUN contains a key called 'Markov' with the value True, otherwise False

    :return: True if CURRENT_RUN is a Markov run, False otherwise
    """
    try:
        is_markov = CURRENT_RUN['Markov']
    except KeyError:
        return False
    else:
        if is_markov:
            return True
        else:
            return False


def get_data_filename():
    """
    Return the filename that contains the data.

    If CURRENT_RUN is a Markov run, return 'results.txt'. Otherwise returns 'sim_output.txt'
    which is the default.

    :return: Either 'sim_output.txt' or 'results.txt'
    """
    if is_markov():
        return 'results.txt'
    else:
        return 'sim_output.txt'


def handle_data_series(path):
    """
    Gather and sort mean and percentile data in all subfolders of path.

    :param path: The full path to the folder to search for data within
    :type path: basestring

    :return: A dictionary of all data within subfolders of path. The dict has 3 keys: 'mean_values',
             '99_percentile_values', and 'x_values'. Each key contains a list of numeric values.
             The final values will be sorted by x_values.
    :rtype: dict with keys 'mean_values', '99_percentile_values', and 'x_values' which each contain
            a list.
    """
    x_values = []
    mean_values = []
    percentile_99_values = []
    for root, sub_folders, filenames in os.walk(path):
        for filename in filenames:
            if filename == get_data_filename():
                test_name = root.split(os.sep)[-1]
                full_path = os.path.join(root, filename)
                data = get_and_plot_queue_length_data(full_path)
                data_statistics = compute_mean_and_percentile(data)
                x_values.append(int(re.findall(r'\d+', test_name)[0]))
                mean_values.append(data_statistics['mean'])
                percentile_99_values.append(data_statistics['99_percentile'])

    series_data = {
        'x_values': x_values,
        'mean_values': mean_values,
        '99_percentile_values': percentile_99_values
    }

    sorted_series_data = sort_data_series(series_data)

    full_output_image_path = os.sep.join([path, 'queue_length.png'])
    plot_single_series(full_output_image_path, sorted_series_data)

    return sorted_series_data


def chart_all_series(image_output_path, all_data, x_label):
    """
    :param image_output_path: The full path to the text file containing the data. The output image
                              will be a peer of this file.
    :type image_output_path: basestring

    :param all_data: All data series to be charted. Each series is expected to provide 'x_values',
                     'mean_values', and '99_percentile_values', and 'name'.
    :type all_data: list of dicts. Each list item is a single series of data containing both mean
                    and percentile information.

    :param x_label: The label of the x axis
    :type x_label: str
    """
    for series in all_data:
        mean_name = series['name'] + ' mean'
        plt.plot(series['x_values'], series['mean_values'], label=mean_name)
        percentile_99_name = series['name'] + ' 99th percentile'
        plt.plot(series['x_values'], series['99_percentile_values'], label=percentile_99_name)
    plt.xlabel(x_label)
    plt.ylabel('Queue Length')
    plt.legend(loc='best', shadow=True, fontsize='medium')
    plt.savefig(image_output_path)
    plt.close()


def sort_data_series(data_series):
    """
    Sorts the data so x_values, mean_values, and 99_percentile_values are all increasing
    :param data_series: The data to sort
    :type data_series: dict with 3 keys 'x_values', 'mean_values', and '99_percentile_values'.

    :return: The sorted data, sorted by x_values increasing
    :rtype: dict
    """
    tuples = zip(data_series['x_values'], data_series['mean_values'], data_series['99_percentile_values'])
    tuples.sort()
    new_data_series = {'x_values': [], 'mean_values': [], '99_percentile_values': []}
    for item in tuples:
        new_data_series['x_values'].append(item[0])
        new_data_series['mean_values'].append(item[1])
        new_data_series['99_percentile_values'].append(item[2])
    return new_data_series


if __name__ == "__main__":
    if not os.path.isfile('queue_length_charts.py'):
        print 'Please run in the same directory as queue_length_charts.py'
    all_data = []
    for path in CURRENT_RUN['paths']:
        full_path = os.path.expanduser(path)
        sorted_data = handle_data_series(full_path)
        sorted_data['name'] = path.split(os.sep)[-2]
        all_data.append(sorted_data)
    full_output_image_path = os.path.expanduser(CURRENT_RUN['output_image'])
    chart_all_series(full_output_image_path, all_data, CURRENT_RUN['x_label'])
