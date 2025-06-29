# #list of 50 values generated within range 10 - 30
#
# # col1 = [
# #     22.45, 17.89, 13.67, 28.14, 19.02, 24.56, 11.23, 27.33, 16.87, 25.48,
# #     14.92, 23.67, 12.55, 29.04, 18.76, 21.12, 15.33, 26.99, 20.45, 13.89,
# #     24.21, 30.00, 17.02, 22.78, 12.94, 19.45, 26.54, 11.87, 23.89, 27.01,     --> f2
# #     14.78, 28.22, 16.14, 25.67, 12.41, 20.56, 29.13, 18.32, 24.45, 21.78,
# #     13.56, 27.45, 19.98, 22.34, 15.67, 30.00, 11.99, 28.56, 17.45, 25.22
# # ]
# #
# # col2 = [
# #     14.22, 25.89, 17.43, 21.67, 27.14, 12.33, 19.84, 16.25, 22.76, 30.00,
# #     13.45, 18.92, 23.58, 11.67, 26.31, 15.78, 24.09, 29.12, 20.47, 12.55,
# #     28.33, 17.22, 21.89, 30.00, 14.87, 19.05, 26.78, 13.99, 22.21, 15.56,         # ----> f1
# #     24.45, 18.77, 27.21, 20.00, 12.89, 28.50, 17.68, 25.34, 29.78, 16.94,
# #     21.23, 11.89, 23.76, 27.05, 14.12, 20.99, 18.44, 26.12, 30.00, 13.21
# # ]
# #element_count = 50
# #list of 30 values in the range 7 - 17 (col1) and 12 - 22 (col2)
#
col1 = [
    10.32, 13.87, 9.45, 15.22, 11.76, 14.04, 8.91, 16.58, 12.31, 7.93,
    14.89, 10.14, 15.67, 13.02, 11.48, 16.21, 9.76, 12.58, 7.82, 14.56,  # ----> f2
    8.33, 16.87, 11.02, 15.44, 10.89, 13.21, 8.47, 12.78, 16.09, 7.50
]


col2 = [
    18.45, 14.67, 20.12, 15.89, 19.34, 13.78, 21.05, 17.22, 16.84, 22.00,
    13.56, 19.92, 15.43, 20.87, 12.99, 18.76, 21.32, 14.21, 20.45, 17.89,  # ----> f1
    16.72, 19.11, 21.58, 13.44, 22.00, 17.55, 20.29, 14.78, 12.88, 19.63
]

def val2val(col1, col2, order_matters, element_count, error):# 0/1 ---> 0 - yes ... 1-> no

    matching_elements = 0
    setCount = 6

    print()
    print()

    if order_matters:
        col1 = sorted(col1)
        col2 = sorted(col2)
        print(sorted(col1))
        print(sorted(col2))
        for i in range(len(col1)):
            for j in range(len(col2)):
                a = col1[i]
                b = col2[j]

                if abs(col1[i] - col2[j]) <= error:
                    matching_elements = matching_elements + 1
                    del col2[j]
                    break

    else:
        for i in range(0, len(col1), setCount):
            # Take the first 3 elements from each list
            subset_col1 = col1[i:i + setCount]
            subset_col2 = col2[i:i + setCount]

            # Sort the subsets
            sorted_col1 = sorted(subset_col1)
            sorted_col2 = sorted(subset_col2)

            for num1 in sorted_col1:
                # Find elements in list2 within ±0.2 of the current element in list1
                for num2 in sorted_col2:
                    if abs(num2 - num1) <= error:
                        matching_elements = matching_elements + 1
                        sorted_col2.remove(num2)
                        break

            print(sorted_col1)
            print(sorted_col2)
            print()
    print("order matter " + str(order_matters) + " ...(0 - > yes)")
    print("The number of matching elements are " + str(matching_elements))
    print("The percentage is " + str((matching_elements / element_count) * 100) + " %")
    return (matching_elements / element_count) * 100

