function data_no_DC = removeDC(data)
    data_mean = mean(data);
    data_no_DC = data - data_mean;

    