import scipy.stats
import numpy as np
import sys
sys.path.append("/Users/kristinalooper/WorkArea/template_fit_py/template_fit")

from run_fit import run_fit

np.random.seed(42)
data = np.random.uniform(0,1,5)
test_b = data*0.15
test_c = data*0.25
test_l = data*0.6

test_bins = np.arange(0,1.2,0.2)

h_b = (test_b,test_bins)
h_c = (test_c,test_bins)
h_l = (test_l,test_bins)
h_data = (data,test_bins)

test_sum = test_b[0] + test_c[0] + test_l[0]

if test_sum == data[0]:
    print('test Ok')
else:
    print('Check values')

run_fit(h_b,h_c,h_l,h_data)
