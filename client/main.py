#!/usr/bin/env python

import value_generator as vg
from pprint import pprint


def main():
    n_vectors = int(1e3)
    max_value = 100
    min_value = - max_value

    vector_list = []
    for i in range(2 * n_vectors):
        vector = vg.generate_vector3(min_value, max_value)
        vector_list.append(vector)
    
    # pprint(vector_list)
    


if __name__ == "__main__":
    main()
