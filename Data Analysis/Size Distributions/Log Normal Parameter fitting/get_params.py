import parameters

def main():
    to_fit = [2087030, 299710, 151140, 80575, 25915, 14615, 9825]
    print(parameters.get_mean_sd(to_fit))


if __name__ == '__main__':
    main()
