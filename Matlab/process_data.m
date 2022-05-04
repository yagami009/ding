load sample

% https://github.com/mnakanishi/TRCA-SSVEP
% Stimulus frequencies : 8.0 - 15.8 Hz with an interval of 0.2 Hz
% Number of channels : 9 (1: Pz, 2: PO5,3: PO3, 4: POz, 5: PO4, 6: PO6, 7: O1, 8: Oz, and 9: O2)
% Number of recording blocks : 6
% Length of an epoch : 5 s
% Sampling rate : 250 Hz

% [# of targets, # of channels, # of sampling points, # of blocks] = size(eeg);
% increments of 0.2hz starting at 8 hz
% target index 1 -> 8hz, 11 -> 10hz, 21 -> 12hz

for c = 1:9
    for b = 1:6
        str = sprintf("/Users/rishil/Desktop/FYP/EEG-decoding/eeg_lib/log/mnakanishi/12hz/12hz_channel_%02d_%02d",c,b);
        data = squeeze(eeg(21,c,:,b))';
        csvwrite(str,data)
    end
end
