import scipy.stats
import scipy.optimize as opt
import numpy as np
import matplotlib.pyplot as plt
from integrate_hist import integrate_hist

def run_fit(b_array,c_array,l_array,data):
    #convert histograms into pdfs
    b_dist = scipy.stats.rv_histogram(b_array)
    c_dist = scipy.stats.rv_histogram(c_array)
    l_dist = scipy.stats.rv_histogram(l_array)

    print("data[1]: ",data[1])
    bin_widths = np.diff(data[1])
    print("diff: ",bin_widths)
    bin_centers = data[1][:-1] + bin_widths/2.
    integral = integrate_hist(bin_widths, data[0])
    fig=plt.figure(figsize=(8,10))
    ax1=fig.add_subplot(2,1,1)
    plt.yscale('log')
    ax2=fig.add_subplot(2,1,2, sharex=ax1)
    plt.yscale('log')
    ax1.set_title('Distributions before fitting')
    ax1.set_xlabel('Neural net weight')
    ax1.set_ylabel('Events')
    ax1.bar(bin_centers, b_array[0], width=bin_widths, label='b')
    ax1.bar(bin_centers, c_array[0], width=bin_widths, bottom=b_array[0],label='c')
    ax1.bar(bin_centers, l_array[0], width=bin_widths, bottom=b_array[0]+c_array[0],label='l')
    ax1.scatter(bin_centers,data[0],label='data',zorder=1000)
    ax1.legend()

    #fit data to pdf of template sums
    #pdf=b*(b_dist)+c*(c_dist)+(1-(b+c))*(l_dist)
    def pdf_sum(x,b,c):
        return (b*b_dist.pdf(x)+c*c_dist.pdf(x)+(1-b-c)*l_dist.pdf(x))*integral
    par, cov = opt.curve_fit(pdf_sum, bin_centers, data[0],p0=[0.04,0.06])

    #use parameters from fit to rescale template distributions for plotting
    #par[0] = 0.0296
    #par[1] = 0.0609
    print(par[0])
    print(par[1])
    b_integral = integrate_hist(bin_widths, b_array[0])
    c_integral = integrate_hist(bin_widths, c_array[0])
    l_integral = integrate_hist(bin_widths, l_array[0])
    print("b integral: ", b_integral)
    scale_b = integral*par[0]/b_integral
    scale_c = integral*par[1]/c_integral
    scale_l = integral*(1-par[0]-par[1])/l_integral

    b_array_scaled = b_array[0]*scale_b
    c_array_scaled = c_array[0]*scale_c
    l_array_scaled = l_array[0]*scale_l

    print('b scaled integral: ', integrate_hist(bin_widths,b_array_scaled))

    print('data',data[0][3])
    print('mc',b_array_scaled[3]+c_array_scaled[3]+l_array_scaled[3])

    ax2.set_title('Distributions after fitting')
    ax2.set_xlabel('Neural net weight')
    ax2.set_ylabel('Events')
    ax2.bar(bin_centers, b_array_scaled, width=bin_widths, label='b')
    ax2.bar(bin_centers, c_array_scaled,width=bin_widths, bottom=b_array_scaled, label='c')
    ax2.bar(bin_centers, l_array_scaled,width=bin_widths, bottom=b_array_scaled+c_array_scaled, label='l')
    ax2.scatter(bin_centers,data[0],label='data',zorder=1000)
    ax2.legend()
    plt.show()

    return par
