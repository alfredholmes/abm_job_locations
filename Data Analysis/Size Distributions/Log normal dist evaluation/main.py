import random
import matplotlib.mlab as mlab
import matplotlib.pyplot as plt



def main():
    sizes = []
    for _ in range(10000):
        #age = random.randint(200, 5000)
        age = 1000
        sizes.append(generate_company(age, 4))

    plt.hist(sizes, 50)
    plt.show()

def generate_company(age, start_size):
    size = start_size
    for t in range(age):
        size *= 1 + random.gauss(0.0001, 0.001)
        if size < 1:
            size = 1
    return size

if __name__ == '__main__':
    main()
