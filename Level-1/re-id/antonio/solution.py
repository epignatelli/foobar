def solution(data, n):
    # Ricreata, mi sono scordato di salvarla prima di fare submit...
    def clean_next(data, elem_number, max_occurences):
        elem_value = data[elem_number]
        num_occurrences = sum([x==elem_value for x in data])
        if num_occurrences > max_occurences:
            new_data = [x in data if not(x==elem_value)]
            return new_data, False
        return data, True

    elemnumber = 0
    while elemnumber < len(data):
        data, kept = clean_next(data, elemnumbe, n)
        if kept:
            elemnumber += 1
    return data