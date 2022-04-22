clear all

sevenhz = dir("C:\Users\RISHI\Desktop\FYP\EEG-decoding\eeg_lib\log\fs512hz_gain255_30s\7hz");
tenhz = dir("C:\Users\RISHI\Desktop\FYP\EEG-decoding\eeg_lib\log\fs512hz_gain255_30s\10hz");
twelvehz = dir("C:\Users\RISHI\Desktop\FYP\EEG-decoding\eeg_lib\log\fs512hz_gain255_30s\12hz");

sevenhz_process = {};
tenhz_process = {};
twelvehz_process = {};

for i = 1:length(sevenhz)
    if sevenhz(i).isdir ~= 1
        sevenhz_process = [sevenhz_process, strcat(sevenhz(i).folder,'\',sevenhz(i).name)];
    end
end

for i = 1:length(tenhz)
    if tenhz(i).isdir ~= 1
        tenhz_process = [tenhz_process, strcat(tenhz(i).folder,'\',tenhz(i).name)];
    end
end

for i = 1:length(twelvehz)
    if twelvehz(i).isdir ~= 1
        twelvehz_process = [twelvehz_process, strcat(twelvehz(i).folder,'\',twelvehz(i).name)];
    end
end

paths = [sevenhz_process, tenhz_process, twelvehz_process];

result_arr = [];
decoded = [];

for p = 1:length(paths)
    
    f = fopen(string(paths(p)));
    data = textscan(f,'%s');
    fclose(f);
    data = removeDC(str2double(data{1}(2:end-1))');
    data = bandpass(data,[1 37],512);
    
    X = (data) / (max(data));
    
    
    fs = 512; % Sampling frequency (samples per second) 
    dt = 1/fs; % seconds per sample 
    StopTime = 1; % seconds 
    t = (0:dt:StopTime)'; % seconds 
    
    results = [];
    last = 512;
    step = 512;
    
    while last < length(X)
        % #########################################################################
        F = 7; % Sine wave frequency (hertz) 
        data = sin(2*pi*F*t);
        Y = data(1:end-1,:)';
        [r7, Wx7, Wy7] = cca_calc(X(:,last-step+1:last),Y);
        % #########################################################################
        F = 10; % Sine wave frequency (hertz) 
        data = sin(2*pi*F*t);
        Y = data(1:end-1,:)';
        [r10, Wx10, Wy10] = cca_calc(X(:,last-step+1:last),Y);
        % #########################################################################
        F = 12; % Sine wave frequency (hertz) 
        data = sin(2*pi*F*t);
        Y = data(1:end-1,:)';
        [r12, Wx12, Wy12] = cca_calc(X(:,last-step+1:last),Y);
        % #########################################################################
        
        if r12 > r10 && r12 > r7
            results(end+1) = 12;
        elseif r10 > r7
            results(end+1) = 10;
        else
            results(end+1) = 7;
        end
        
        last = last+step;
    end
    
    res = [sum(results(:) == 12) sum(results(:) == 10) sum(results(:) == 7)];
    result_arr = [result_arr; res];
    [M,I] = max(res);
    
    if I == 1
        decoded(end+1) = 12;
    elseif I == 2
        decoded(end+1) = 10;
    else
        decoded(end+1) = 7;
    end
end

T = table(paths', decoded', result_arr);
