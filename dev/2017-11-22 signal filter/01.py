import matplotlib.pyplot as plt
import numpy as np

def kernel_gaussian(sigma=5):
    size=sigma*10
    points=np.exp(-np.power(np.arange(size)-size/2,2)/(2*np.power(sigma,2)))
    return points/sum(points)

if __name__=="__main__":
    
    # create some noisy data
    nPoints=1000
    signal=np.arange(nPoints)
    signal=np.sin(signal/20)
    signal+=np.random.random_sample(len(signal))
    
    plt.figure(figsize=(12,6))
    plt.subplot(121)
    plt.step(np.arange(len(signal)),signal,label="signal",color='.8')
    
    for sigma in [2,5,20]:
        
        plt.subplot(121)
        kernel=kernel_gaussian(sigma=sigma)
        smooth=np.convolve(signal,kernel,mode='same')
        plt.plot(np.arange(len(smooth)),smooth,label=str(sigma))
        plt.legend()
        
        plt.subplot(122)
        Xs=np.arange(len(kernel))-len(kernel)/2
        plt.plot(Xs,kernel/np.max(kernel),label=str(sigma))
        plt.legend()

    plt.subplot(121)
    plt.axis([100,175,-1,2])    
    plt.show()
    
    print("DONE")