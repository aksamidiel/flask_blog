def buble_sort(*args):
    swapped = True
    while swapped:
        swapped = False
        for i in range(len(args)-1):
            if args[i] > args[i+1]:
                args[i], args[i + 1] = args[i+1], args[i]

                swapped = True


random_list_elem = map(int, list(input("Enter some var: ")))
mass=[]
for j in random_list_elem:
    mass.append(j)
    print(j)


buble_sort(mass)
print("Res: {0}".format(mass))


def selection_sort(nums):
    for i in range(len(nums)):
        lowest_val_index = i
        for j in range(i+1, len(nums)):
            if nums[j] < nums[lowest_val_index]:
                lowest_val_index = j
        nums[i], nums[lowest_val_index] = nums[lowest_val_index], nums[i]

random_list_of_nums = [12, 8, 10 , 5]
selection_sort(random_list_of_nums)
print(random_list_of_nums)
