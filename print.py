DIST_TABLE = [
    [99, 90, 80, 70, 60, 50, 40, 30, 20, 10, 5, 2, 1],
    [0.00, 0.02, 0.06, 0.15, 0.27, 0.45, 0.71, 1.07, 1.64, 2.71, 3.84, 5.41, 6.63],
    [0.02, 0.21, 0.45, 0.71, 1.02, 1.39, 1.83, 2.41, 3.22, 4.61, 5.99, 7.82, 9.21],
    [0.11, 0.58, 1.01, 1.42, 1.87, 2.37, 2.95, 3.66, 4.64, 6.25, 7.81, 9.84, 11.34],
    [0.30, 1.06, 1.65, 2.19, 2.75, 3.36, 4.04, 4.88, 5.99, 7.78, 9.49, 11.67, 13.28],
    [0.55, 1.61, 2.34, 3.00, 3.66, 4.35, 5.13, 6.06, 7.29, 9.24, 11.07, 13.39, 15.09],
    [0.87, 2.20, 3.07, 3.83, 4.57, 5.35, 6.21, 7.23, 8.56, 10.64, 12.59, 15.03, 16.81],
    [1.24, 2.83, 3.82, 4.67, 5.49, 6.35, 7.28, 8.38, 9.80, 12.02, 14.07, 16.62, 18.48],
    [1.65, 3.49, 4.59, 5.53, 6.42, 7.34, 8.35, 9.52, 11.03, 13.36, 15.51, 18.17, 20.09],
    [2.09, 4.17, 5.38, 6.39, 7.36, 8.34, 9.41, 10.66, 12.24, 14.68, 16.92, 19.68, 21.67],
    [2.56, 4.87, 6.18, 7.27, 8.30, 9.34, 10.47, 11.78, 13.44, 15.99, 18.31, 21.16, 23.21]
]


def print_all(args, tx, prob):
    merged_x, merged_args, merged_tx = merge_arrays(args, tx)
    chi_squared = sum(map(lambda x: pow(x[0] - x[1], 2) / x[1], zip(merged_args, merged_tx)))
    degrees_of_freedom = len(merged_x) - 2

    print("Distribution:\t\tB(100, %.4f)" % prob)
    print("Chi-squared:\t\t%.3f" % chi_squared)
    print("Degrees of freedom:\t%d" % degrees_of_freedom)
    print("Fit validity:\t\t%s" % get_validity(degrees_of_freedom, chi_squared))


def get_validity(degrees_of_freedom, chi_squared):
    idx = 0
    for i in DIST_TABLE[degrees_of_freedom]:
        if i > chi_squared:
            break
        idx += 1
    if idx != 0:
        idx -= 1
    perc = DIST_TABLE[0][idx]
    if perc == 99:
        return "P > " + str(perc) + "%"
    elif perc == 1:
        return "P < " + str(perc) + "%"
    return str(DIST_TABLE[0][idx + 1]) + "% < P < " + str(perc) + "%"


def merge_arrays(args, tx):
    range_array = [[i] for i in range(0, 9)]
    range_array, args, tx = merge_both_inferior(range_array, args, tx)
    range_array, args, tx = merge_one_inferior(range_array, args, tx)
    range_array = range_array_to_string_array(range_array)
    print_row(" x", range_array, "Total", "%s")
    print_row("Ox", args, "100", "%d")
    print_row("Tx", tx, "100", "%.1f")
    return range_array, args, tx


def merge_both_inferior(range_array, args, tx):
    for i in range(len(range_array) - 1):
        if args[i] < 10 and args[i + 1] < 10:
            range_array = range_array[:i] + [[range_array[i][0], range_array[i + 1][-1]]] + range_array[i + 2:]
            args = args[:i] + [args[i] + args[i + 1]] + args[i + 2:]
            tx = tx[:i] + [tx[i] + tx[i + 1]] + tx[i + 2:]
            range_array, args, tx = merge_both_inferior(range_array, args, tx)
            break
    return range_array, args, tx


def merge_one_inferior(range_array, args, tx):
    for i in range(len(range_array) - 1):
        if args[i] < 10 or args[i + 1] < 10:
            range_array = range_array[:i] + [[range_array[i][0], range_array[i + 1][-1]]] + range_array[i + 2:]
            args = args[:i] + [args[i] + args[i + 1]] + args[i + 2:]
            tx = tx[:i] + [tx[i] + tx[i + 1]] + tx[i + 2:]
            range_array, args, tx = merge_one_inferior(range_array, args, tx)
            break
    return range_array, args, tx


def range_array_to_string_array(range_array):
    string_array = []
    for i in range(0, len(range_array) - 1):
        if len(range_array[i]) > 1:
            string_array.append(str(range_array[i][0]) + "-" + str(range_array[i][-1]))
        else:
            string_array.append(str(range_array[i][0]))
    string_array.append(str(range_array[-1][0]) + "+")
    return string_array


def print_row(prefix, array, suffix, format_string):
    print("  %s" % prefix, end="\t| ")
    for x in array:
        print(format_string % x, end="\t| ")
    print("%s" % suffix)
