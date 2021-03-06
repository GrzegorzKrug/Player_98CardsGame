import numpy as np
import sklearn.neural_network
# import sklearn.multioutput
from time import time
import shelve
from supervised_data_grab import Grab_Teaching_Data


def __run_count__(readonly=False, step=1):
    num = 0
    try:
        with open('__run_count__.txt', 'r') as file:
            num = int(file.read())

    except FileNotFoundError:
        num = 0
    if not readonly:
        num += step
        with open('__run_count__.txt', 'w') as file:
            file.write(str(num))

    return str(num)


def time_decorator_tell_me_duration(func):
    def wrapper(*args, **kwargs):

        time0 = time()
        out = func(*args, **kwargs)
        duration = time() - time0
        return duration
    return wrapper


samples_count = 15  # [k]
score_min = 75
nn_dimensions = (98*97, int(8*4/2))
max_iter = 500

data = Grab_Teaching_Data()
name = 'NN_supervised_' + __run_count__()

# input('Are you sure you want to retrain your network? ...')
print('Ok, collecting samples...')
samples = data.generate_random_states(samples_count, score_min=score_min)

print('Got {0} samples'.format(len(samples)))
print('Average good moves from 1 sample: {}%'.format(str(len(samples)/samples_count/1000*100)))

X = []
Y = []
for sample in samples:
    new_sample = np.concatenate((sample['hand'], sample['piles']))
    X.append(new_sample)
    Y.append(sample['move'])

print('Learning {} ...'.format(name))
nn1 = sklearn.neural_network.MLPRegressor(nn_dimensions, max_iter=max_iter,)


time_before = time()  # Not decorated
nn1.fit(X, Y)
learning_time = time() - time_before  # Not decorated

print('Time elapsed:', learning_time)
print('Saving to file....')


comment = 'One move per sample, begin samples, end samples'
with shelve.open('NN\\' + name, 'n') as file:
    file['supervised'] = nn1
    file['comment'] = comment

with open('learning_log.txt', 'a') as file:
    file.write('NN name:          {}\n'.format(name))
    file.write('NN comment:       {}\n'.format(comment))
    file.write('All samples:      {} 000\n'.format(samples_count))
    file.write('Samples grabbed:  {} %\n'.format(round((len(Y) / samples_count / 10), 4)))
    file.write('Learning layers:  {}\n'.format(nn_dimensions))
    file.write('Max iters:        {}\n'.format(max_iter))
    file.write('Learning Time:    {} m\n\n'.format(round(learning_time/60, 2)))
