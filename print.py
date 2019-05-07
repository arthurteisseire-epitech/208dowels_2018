def print_arrays(args, tx):
    range_array = [[i] for i in range(0, 9)]
    range_array, args, tx = modify_arrays(range_array, args, tx)
    range_array = range_array_to_string_array(range_array)
    print_row(" x", range_array, "Total", "%s")
    print_row("Ox", args, "100", "%d")
    print_row("Tx", tx, "100", "%.1f")


def modify_arrays(range_array, args, tx):
    for i in range(len(range_array) - 1):
        if args[i] < 10 or args[i + 1] < 10:
            range_array = range_array[:i] + [[range_array[i][0], range_array[i + 1][-1]]] + range_array[i + 2:]
            args = args[:i] + [args[i] + args[i + 1]] + args[i + 2:]
            tx = tx[:i] + [tx[i] + tx[i + 1]] + tx[i + 2:]
            range_array, args, tx = modify_arrays(range_array, args, tx)
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
