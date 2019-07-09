from ROOT import TH1F, TFile
import matplotlib.pyplot as plt

import sys
sys.path.append("/Users/kristinalooper/WorkArea/template_fit_py/template_fit")
from roothist_to_numpy import roothist_to_numpy

test_np,test_bins = roothist_to_numpy("/Users/kristinalooper/WorkArea/template_fit_py/template_fit/test/test_hist.root","h")

print(len(test_np))
print(len(test_bins[0]))

plt.bar(test_np,test_bins[0])
plt.show()
