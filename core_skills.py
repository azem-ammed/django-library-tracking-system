import random
# rand_list =
rand_list = [random.randint(1, 20) for _ in range(10)]

# list_comprehension_below_10 =
list_comprehension_below_10 = [n for n in rand_list if n < 10]

# list_comprehension_below_10 =
filter_below_10 = list(filter(lambda n: n < 10, rand_list))

