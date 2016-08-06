import os

import matplotlib.pyplot as plt

hourly_data = {
    'vary_startup': {
        'ma': [380.21, 380.21, 530.75],
        'ema': [195.13, 195.13, 361.63],
        'ar': [447.26, 447.26, 671.63],
        'mixed-ar': [428.63, 428.63, 675.26],
        'reserve': [179.78, 179.78, 320.31],
        'arhmm': [257.21, 257.21, 428.07],
    },
    'vary_shutdown': {
        'ma': [362.68, 380.21, 380.21, 353.68],
        'ema': [195.13, 195.13, 195.13, 189.33],
        'ar': [461.73, 447.26, 447.26, 405.84],
        'mixed-ar': [447.26, 428.63, 428.63, 388.84],
        'reserve': [184.82, 179.78, 179.78, 179.87],
        'arhmm': [290.28, 257.21, 257.21, 238.46],
    }
}

markers = {
    'ma': '1',
    'ema': 5,
    'ar': '^',
    'mixed-ar': '+',
    'reserve': 'o',
    'arhmm': 'x',
}

model_label = {
    'ma': 'Moving Average',
    'ema': 'Exponential Moving Average',
    'ar': 'Autoregressive',
    'mixed-ar': 'Mixed Autoregressive',
    'reserve': 'Reserve Capacity',
    'arhmm': 'AR-HMM',
}


filename_base = '/home/bmbouter/Documents/Research/pareto/images/chapter_five_paper/%s.png'


def plot_model_comparison(data, filename, x_times, x_label, loc=3, text_size=10):
    full_path = filename_base % filename
    plt.figure(figsize=(9, 7), dpi=300)
    for model, wait_time in data.iteritems():
        plt.scatter(x_times, data[model], marker=markers[model], label=model_label[model], c='k', s=60)
    plt.xlabel(x_label)
    plt.ylabel('Waiting Time 99th Percentile per Hour (s)')
    plt.legend(loc=loc, prop={'size': text_size}, scatterpoints=1)
    plt.savefig(full_path, bbox_inches='tight')
    plt.close()


if __name__ == "__main__":
    if not os.path.isfile('chapter_five_as_paper_startup_shutdown.py'):
        print 'Please run in the same directory as chapter_five_as_paper_startup_shutdown.py'
        exit()
    plot_model_comparison(hourly_data['vary_startup'], 'vary_startup', [120, 300, 480], 'Startup Delay (s)', loc=2)
    plot_model_comparison(hourly_data['vary_shutdown'], 'vary_shutdown', [0, 120, 300, 480], 'Shutdown Delay (s)', loc=1)
