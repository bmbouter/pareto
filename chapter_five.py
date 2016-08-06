import os

import matplotlib.pyplot as plt

util_data = {
    'ma': 0.852,
    'ema': 0.8494,
    'ar': 0.8522,
    'mixed-ar': 0.8564,
    'reserve': 0.8534,
    'arhmm': 0.8515,
    'pre-known': 0.8662,
}

all_data = {
    'avg': {
        'ma': 21.13,
        'ema': 19.97,
        'ar': 21.85,
        'mixed-ar': 24.03,
        'reserve': 29.44,
        'arhmm': 28.72,
        'pre-known': 15.07,
    },
    'hour': {
        'ma': 370.05,
        'ema': 172.89,
        'ar': 444.42,
        'mixed-ar': 436.10,
        'reserve': 157.35,
        'arhmm': 226.31,
        'pre-known': 164.95,
    },
    'day': {
        'ma': 70.85,
        'ema': 57.63,
        'ar': 101.53,
        'mixed-ar': 105.15,
        'reserve': 59.97,
        'arhmm': 75.04,
        'pre-known': 43.12,
    },
    'week': {
        'ma': 42.27,
        'ema': 38.59,
        'ar': 63.88,
        'mixed-ar': 63.95,
        'reserve': 36.49,
        'arhmm': 46.17,
        'pre-known': 24.81,
    },
}

markers = {
    'ma': '1',
    'ema': 5,
    'ar': '^',
    'mixed-ar': '+',
    'reserve': 'o',
    'arhmm': 'x',
    'pre-known': 's',
}

model_label = {
    'ma': 'Moving Average',
    'ema': 'Exponential Moving Average',
    'ar': 'Autoregressive',
    'mixed-ar': 'Mixed Autoregressive',
    'reserve': 'Reserve Capacity',
    'arhmm': 'AR-HMM',
    'pre-known': 'Pre-Known Demand',
}


filename_base = '/home/bmbouter/Documents/Research/pareto/images/chapter_five/%s.png'


def plot_model_comparison(data, filename, optimal_models, loc=3, text_size=10):
    full_path = filename_base % filename
    plt.figure(figsize=(9, 7), dpi=300)
    for model, wait_time in data.iteritems():
        if model == 'pre-known':
            color = 'blue'
        elif model in optimal_models:
            color = 'g'
        else:
            color = 'r'
        plt.scatter(wait_time, util_data[model], marker=markers[model], label=model_label[model], c=color, s=60)
    plt.xlabel('Wait Time (s)')
    plt.ylabel('Utilization')
    plt.legend(loc=loc, prop={'size': text_size}, scatterpoints=1)
    plt.savefig(full_path, bbox_inches='tight')
    plt.close()


if __name__ == "__main__":
    if not os.path.isfile('chapter_five.py'):
        print 'Please run in the same directory as chapter_five.py'
        exit()
    plot_model_comparison(all_data['avg'], 'avg', ['ema', 'ar', 'mixed-ar', 'ma', 'pre-known'], loc=1)
    plot_model_comparison(all_data['hour'], 'hour', ['mixed-ar', 'reserve', 'pre-known'], loc=1)
    plot_model_comparison(all_data['day'], 'day', ['ema', 'mixed-ar', 'reserve', 'pre-known'], loc=1)
    plot_model_comparison(all_data['week'], 'week', ['mixed-ar', 'reserve', 'pre-known'], loc=1)
