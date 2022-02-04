from ulab import numpy as np
import gc

from .computation import solve_eig_qr, standardise, solve_gen_eig_prob
    
class CCA(): 
    def __init__(self, stim_freqs, fs, Nh=2):
        self.Nh = Nh
        self.stim_freqs = stim_freqs
        self.fs = fs
        
    def compute_corr(self, X_test):            
        result = {}
        Cxx = np.dot(X_test, X_test.transpose()) # precompute data auto correlation matrix
        for f in self.stim_freqs:
            Y = harmonic_reference(f, self.fs, np.max(X_test.shape), Nh=self.Nh, standardise_out=False)
            rho = self.cca_eig(X_test, Y, Cxx=Cxx) # canonical variable matrices. Xc = X^T.W_x
            result[f] = rho
        return result
    
    @staticmethod
    def cca_eig(X, Y, Cxx=None, eps=1e-6):
        if Cxx is None:
            Cxx = np.dot(X, X.transpose()) # auto correlation matrix
        Cyy = np.dot(Y, Y.transpose()) 
        Cxy = np.dot(X, Y.transpose()) # cross correlation matrix
        Cyx = np.dot(Y, X.transpose()) # same as Cxy.T

        M1 = np.dot(np.linalg.inv(Cxx+eps), Cxy) # intermediate result
        M2 = np.dot(np.linalg.inv(Cyy+eps), Cyx)

        lam, _ = solve_eig_qr(np.dot(M1, M2), 20)
        return np.sqrt(lam)
    
class UnivariateMsetCCA():
    """
    Multiset CCA algorithm for SSVEP decoding.
    
    Computes optimised reference signal set based on historical observations
    and uses ordinary CCA for final correlation computation given a new test
    signal.
    
    Note: this is a 1 channel implementation (Nc=1)
    """
    
    def __init__(self):
        self.Ns, self.Nt = None, None
        
    def fit(self, X, compress_ref=True):
        """
        Expects a training matrix X of shape Nt x Ns. If `compress_ref=True`, the `Nt` components
        in optimised reference signal Y will be averaged to form a single reference vector. This
        can be used for memory optimisation but will likely degrade performance slightly.         
        """
        if X.shape[0] > X.shape[1]:
            print("Warning: received more trials than samples. This is unusual behaviour: check orientation of X"
                 )
        R = np.dot(X, X.transpose()) # inter trial covariance matrix
        S = np.eye(len(R))*np.diag(R) # intra-trial diag covariance matrix

        lam, V = solve_gen_eig_prob((R-S), S) # solve generalised eig problem
        w = V[:, np.argmax(lam)] # find eigenvector corresp to largest eigenvalue
        Y = np.array([x*w[i] for i, x in enumerate(X)]) # store optimised reference vector Nt x Ns
        self.Y  = Y
        if compress_ref:
            self.Y = np.mean(Y, axis=0).reshape((1, max(Y.shape))) # this will average Nt components in Y: Nc x Nt -> 1 x Nt
        
    def compute_corr(self, X_test):
        if self.Y is None:
            raise ValueError("Reference matrix Y must be computed using `fit` before computing corr")
        if len(X_test.shape) == 1:
            X_test = X_test.reshape((1, len(X_test)))
        return CCA.cca_eig(X_test, self.Y)[0]
    
class MsetCCA_SSVEP():
    """
    Extension/utility class for the `UnivariateMsetCCA` class that encapsulates multiple
    independent MsetCCA models for the stimulus frequencies of interest. 
    
    Note: this is a 1 channel implementation (Nc=1) inteded for multiple stim freqs.
    """
    
    def __init__(self, stim_freqs):
        self.stim_freqs = stim_freqs
        self.models = {f: UnivariateMsetCCA() for f in stim_freqs} # init independent TRCA models per stim freq

    def fit(self, data, compress_ref=True):
        '''
        Fit the independent Nf MsetCCA models using input data map. Expects this data map to 
        be of the form {7: X_7, 10: X_10, ...} where Xi is the training data matrix for freq i
        and has shape Nt x Ns. Nc is assumed to be 1 in this implementation.
        '''
        for stim_freq in data:
            if stim_freq not in self.stim_freqs:
                raise ValueError("Expected data map to only contain stim freqs")
            self.models[stim_freq].fit(data[stim_freq], compress_ref=compress_ref)
    
    def classify(self, X_test):        
        return {f: self.models[f].compute_corr(X_test) for f in self.stim_freqs}        

def harmonic_reference(f0, fs, Ns, Nh=1, standardise_out=False):
    
    '''
    Generate reference signals for canonical correlation analysis (CCA)
    -based steady-state visual evoked potentials (SSVEPs) detection [1, 2].
    function [ y_ref ] = cca_reference(listFreq, fs,  Ns, Nh) 
    Input:
      f0        : stimulus frequency
      fs              : Sampling frequency
      Ns              : # of samples in trial
      Nh          : # of harmonics
    Output:
      y_ref           : Generated reference signals with shape (Nf, Ns, 2*Nh)
    '''  
    X = np.zeros((Nh*2, Ns))
    
    for harm_i in range(Nh):
        # Sin and Cos
        X[2*harm_i, :] = np.sin(np.arange(1,Ns+1)*(1/fs)*2*np.pi*(harm_i+1)*f0)
        gc.collect()
        X[2*harm_i+1, :] = np.cos(np.arange(1,Ns+1)*(1/fs)*2*np.pi*(harm_i+1)*f0)
        gc.collect()

    # print(micropython.mem_info(1))
    if standardise_out: # zero mean, unit std. dev
        return standardise(X)
    return X
