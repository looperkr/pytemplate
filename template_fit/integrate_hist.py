def integrate_hist(widths,heights):
    integral = 0
    for width, height in zip(widths,heights):
        integral+= width*height
    return integral
