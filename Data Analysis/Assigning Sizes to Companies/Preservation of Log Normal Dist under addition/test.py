from scipy.stats import lognorm, norm
from scipy import integrate
import matplotlib.pyplot as plt
import numpy as np

mean = 0.001
sd   = 0.01

age_mean = 2.5
age_sd   = 1

def main():
    plt.plot([x/50 for x in range(1, 100)], [pdf(x/50) for x in range(1, 100)], label='pdf')
    mean, variance = mean_variance()

    ln_variance = np.log(1 + variance / mean ** 2)
    ln_sd = np.sqrt(ln_variance)
    ln_mean = np.log(mean / np.sqrt(1 + variance / mean ** 2))

    plt.plot([x / 50 for x in range(1, 100)], [lognorm.pdf(x / 50, ln_sd, scale=np.exp(ln_mean)) for x in range(1, 100)])

    #plt.legend()
    plt.savefig('distributions.png')
    plt.show()

def mean_variance():
    mean = integrate.quad(lambda t: t * pdf(t), 0.01, np.inf)[0]
    variance = integrate.quad(lambda t: t * t * pdf(t), 0.01, np.inf)[0] - mean ** 2

    return mean, variance

def pdf(x):
    return integrate.quad(lambda t: lognorm.pdf(t, age_sd, scale=np.exp(age_mean)) * lognorm.pdf(x, t * sd, scale=np.exp(t * mean)), 0, np.inf)[0]

if __name__ == '__main__':
    main()
