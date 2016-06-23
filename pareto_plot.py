import csv

import matplotlib.pyplot as plt

base_image_dir = '/home/bmbouter/Documents/Research/pareto/images/'

time_vary_point_type_map = {12: 'd',
                            144: '*',
                            288: '^',
                            2016: '+'}

all_model_point_type_map = {'window_size': 'd',
                            'seats': '*',
                            'R': '^',
                            'alpha': '+',
                            'k': '8'}

all_model_model_name_map = {'window_size': 'Time Varying Reserve Capacity',
                            'seats': 'Fixed Capacity',
                            'R': 'Reserve Capacity',
                            'alpha': 'Exponential Moving Average',
                            'k': 'Moving Average'}

def plot_pareto_frontier(Xs, Ys, labels, maxX=True, maxY=True, xlabel="Objective 1", ylabel="Objective 2", title=None, filename=None, legend_loc=2, label_modulus=1, pareto_labeling=False, multi_model_plot=False):
    '''Pareto frontier selection process'''
    legend_list = []
    sorted_list = sorted([[Xs[i], Ys[i], labels[i]] for i in range(len(Xs))], reverse=maxX)
    pareto_front = [sorted_list[0]]
    non_pareto_front = []
    for pair in sorted_list[1:]:
        if maxY:
            if pair[1] >= pareto_front[-1][1]:
                pareto_front.append(pair)
            else:
                non_pareto_front.append(pair)
        else:
            if pair[1] <= pareto_front[-1][1]:
                pareto_front.append(pair)
            else:
                non_pareto_front.append(pair)
    
    '''Plotting process'''
    if filename:
        plt.figure(figsize=(18, 13), dpi=300)
    else:
        plt.figure()
    npf_X = [pair[0] for pair in non_pareto_front]
    npf_Y = [pair[1] for pair in non_pareto_front]
    npf_labels = [pair[2] for pair in non_pareto_front]
    for i in range(len(npf_X)):
        if multi_model_plot:
            if 'window_size' in npf_labels[i]:
                model_param_name = 'window_size'
            else:
                model_param_name = npf_labels[i].rpartition('=')[0]
            key_tuple = (model_param_name, 'NP')
            if key_tuple in legend_list:
                label = None
            else:
                label = 'Pareto SubOptimal, %s' % all_model_model_name_map[model_param_name]
                legend_list.append(key_tuple)
            plt.scatter(npf_X[i], npf_Y[i], marker=all_model_point_type_map[model_param_name], color='red', label=label)
        elif 'window_size' in npf_labels[i]:
            window_size = int(npf_labels[i].rpartition('window_size=')[2])
            key_tuple = (window_size, 'NP')
            if key_tuple in legend_list:
                label = None
            else:
                label = 'Pareto SubOptimal, W=%s' % window_size
                legend_list.append(key_tuple)
            plt.scatter(npf_X[i], npf_Y[i], marker=time_vary_point_type_map[window_size], color='red', label=label)
        else:
            plt.scatter(npf_X[i], npf_Y[i], color='red', label='Pareto SubOptimal')

    pf_X = [pair[0] for pair in pareto_front]
    pf_Y = [pair[1] for pair in pareto_front]
    pf_labels = [pair[2] for pair in pareto_front]
    for i in range(len(pf_X)):
        if multi_model_plot:
            if 'window_size' in pf_labels[i]:
                model_param_name = 'window_size'
            else:
                model_param_name = pf_labels[i].rpartition('=')[0]
            key_tuple = (model_param_name, 'P')
            if key_tuple in legend_list:
                label = None
            else:
                label = 'Pareto Optimal, %s' % all_model_model_name_map[model_param_name]
                legend_list.append(key_tuple)
            plt.scatter(pf_X[i], pf_Y[i], marker=all_model_point_type_map[model_param_name], color='green', label=label)
        elif 'window_size' in pf_labels[i]:
            window_size = int(pf_labels[i].rpartition('window_size=')[2])
            key_tuple = (window_size, 'P')
            if key_tuple in legend_list:
                label = None
            else:
                label = 'Pareto Optimal, W=%s' % window_size
                legend_list.append(key_tuple)
            plt.scatter(pf_X[i], pf_Y[i], marker=time_vary_point_type_map[window_size], color='green', label=label)
        else:
            plt.scatter(pf_X[i], pf_Y[i], color='green', label='Pareto Optimal')

    if pareto_labeling == True:
        for i in range(len(pf_X)):
            if i % label_modulus != 0:
                continue
            label_point(plt, pf_X[i], pf_Y[i], pf_labels[i])
    else:
        for i in range(len(Xs)):
            if i % label_modulus != 0:
                continue
            label_point(plt, Xs[i], Ys[i], labels[i])
            
    #if title:
    #    plt.title(title)
    plt.xlabel(xlabel)
    plt.ylabel(ylabel)
    plt.legend(loc=legend_loc)
    if filename:
        plt.savefig(filename, bbox_inches='tight')
    else:
        plt.show()
    plt.close()

def label_point(plt, x, y, label):
    if 'window_size' in label:
        label = label.replace('window_size', 'W')
    if 'percentile' in label:
        label = label.replace('percentile', 'Q')
    plt.annotate(
        label, 
        xy = (x, y), xytext = (-20, 20),
        textcoords = 'offset points', ha = 'right', va = 'bottom',
        bbox = dict(boxstyle = 'round,pad=0.5', fc = 'yellow', alpha = 0.5),
        arrowprops = dict(arrowstyle = '->', connectionstyle = 'arc3,rad=0'))

def read_data(data_file, xkey, param):
    Xs = []
    Ys = []
    labels = []
    with open(data_file, 'rb') as csvfile:
        datareader = csv.DictReader(csvfile, delimiter=',')
        for i, row in enumerate(datareader):
            Xs.append(row[xkey])
            Ys.append(row['utilization'])
            if isinstance(param, tuple):
                labels.append([row[param_name] for param_name in param])
            else:
                labels.append(row[param])
    if isinstance(param, tuple):
        new_labels = []
        for label_list in labels:
            label_dimensions = []
            for i, label in enumerate(label_list):
                label_dimensions.append("%s=%s" % (param[i], label))
            new_labels.append(','.join(label_dimensions))
        labels = new_labels
    else:
        labels = ["%s=%s" % (param, label) for label in labels]
    return (Xs, Ys, labels)

def iterate_xkeys(func, model_label):
    timescales = ['hour', 'day', 'week', 'month', 'year']
    statistics = ['50', '95', '99', 'mean']
    for timescale in timescales:
        for statistic in statistics:
            xkey = 'bp_by_%s_%s' % (timescale, statistic)
            if statistic == 'mean':
                xlabel = 'Mean Blocking Probability per %s' % timescale.capitalize()
            else:
                xlabel = '%sth Percentile Blocking Probability per %s' % (statistic, timescale.title())
            image_filename = '%s%s/%s_%s_%s.png' % (base_image_dir, model_label, model_label, timescale, statistic)
            func(xlabel=xlabel, xkey=xkey, image_filename=image_filename)

def ma_chart(xlabel='Batch Mean Blocking Probability', xkey='bp_batch_mean', image_filename=None, plot=True):
    data_file = '/home/bmbouter/Documents/Research/pareto/data/ma.csv'
    Xs, Ys, labels = read_data(data_file, xkey, param='k')
    title = "Moving Average Pareto Efficiency\nUtilization vs %s" % xlabel
    if plot:
        plot_pareto_frontier(Xs, Ys, labels, maxX=False, maxY=True, xlabel=xlabel, ylabel="Utilization", title=title, filename=image_filename, legend_loc=4, label_modulus=5)
    return (Xs, Ys, labels)

def ema_chart(xlabel='Batch Mean Blocking Probability', xkey='bp_batch_mean', image_filename=None, plot=True):
    data_file = '/home/bmbouter/Documents/Research/pareto/data/ema.csv'
    Xs, Ys, labels = read_data(data_file, xkey, param='alpha')
    title = "Exponential Moving Average Pareto Efficiency\nUtilization vs %s" % xlabel
    if plot:
        plot_pareto_frontier(Xs, Ys, labels, maxX=False, maxY=True, xlabel=xlabel, ylabel="Utilization", title=title, filename=image_filename, legend_loc=4, label_modulus=5)
    return (Xs, Ys, labels)
    
def fixed_chart(xlabel='Batch Mean Blocking Probability', xkey='bp_batch_mean', image_filename=None, plot=True):
    data_file = '/home/bmbouter/Documents/Research/pareto/data/fixed.csv'
    Xs, Ys, labels = read_data(data_file, xkey, param='seats')
    title = "Fixed Capacity Pareto Efficiency\nUtilization vs %s" % xlabel
    if plot:
        plot_pareto_frontier(Xs, Ys, labels, maxX=False, maxY=True, xlabel=xlabel, ylabel="Utilization", title=title, filename=image_filename, legend_loc=4, label_modulus=7)
    return (Xs, Ys, labels)

def reserve_chart(xlabel='Batch Mean Blocking Probability', xkey='bp_batch_mean', image_filename=None, plot=True):
    data_file = '/home/bmbouter/Documents/Research/pareto/data/reserve.csv'
    Xs, Ys, labels = read_data(data_file, xkey, param='R')
    title = "Reserve Capacity Pareto Efficiency\nUtilization vs %s" % xlabel
    if plot:
        plot_pareto_frontier(Xs, Ys, labels, maxX=False, maxY=True, xlabel=xlabel, ylabel="Utilization", title=title, filename=image_filename, legend_loc=4, label_modulus=7)
    return (Xs, Ys, labels)

def time_vary_reserve_chart(xlabel='Batch Mean Blocking Probability', xkey='bp_batch_mean', image_filename=None, plot=True):
    data_file = '/home/bmbouter/Documents/Research/pareto/data/time_vary_reserve.csv'
    Xs, Ys, labels = read_data(data_file, xkey, param=('percentile', 'window_size'))
    title = "Time Varying Reserve Capacity Pareto Efficiency\nUtilization vs %s" % xlabel
    if plot:
        plot_pareto_frontier(Xs, Ys, labels, maxX=False, maxY=True, xlabel=xlabel, ylabel="Utilization", title=title, filename=image_filename, legend_loc=4, label_modulus=4, pareto_labeling=True)
    return (Xs, Ys, labels)

def all_on_one_chart(xlabel='Batch Mean Blocking Probability', xkey='bp_batch_mean', image_filename=None, plot=True):
    data = []
    data.append(ma_chart(xkey=xkey, plot=False))
    data.append(ema_chart(xkey=xkey, plot=False))
    data.append(fixed_chart(xkey=xkey, plot=False))
    data.append(reserve_chart(xkey=xkey, plot=False))
    #data.append(time_vary_reserve_chart(xkey=xkey, plot=False))
    total_Xs = []
    total_Ys = []
    total_labels = []
    for Xs, Ys, labels in data:
        for i in range(len(Xs)):
            total_Xs.append(Xs[i])
            total_Ys.append(Ys[i])
            total_labels.append(labels[i])
    title = "All Models Pareto Efficiency\nUtilization vs %s" % xlabel
    if plot:
        plot_pareto_frontier(total_Xs, total_Ys, total_labels, maxX=False, maxY=True, xlabel=xlabel, ylabel="Utilization", title=title, filename=image_filename, legend_loc=4, label_modulus=8, pareto_labeling=True, multi_model_plot=True)

def build_pareto_timescale_charts():
    #iterate_xkeys(ma_chart, 'ma')
    #iterate_xkeys(ema_chart, 'ema')
    iterate_xkeys(fixed_chart, 'fixed')
    #iterate_xkeys(reserve_chart, 'reserve')
    #iterate_xkeys(time_vary_reserve_chart, 'time_vary_reserve')
    #iterate_xkeys(all_on_one_chart, 'all_on_one')

if __name__=='__main__':
    build_pareto_timescale_charts()

