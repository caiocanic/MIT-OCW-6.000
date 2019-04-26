# Permutations

def get_permutations(sequence):
    '''
    Enumerate all permutations of a given string

    sequence (string): an arbitrary string to permute. Assume that it is
    a non-empty string.

    Returns: a list of all permutations of sequence
    '''
    if len(sequence) == 1:
        return [sequence]
    result = []
    for i, value in enumerate(sequence):
        for p in get_permutations(sequence[:i] + sequence[i + 1:]):
            result += [value + p]
    return result
        

def test_get_permutations(example_input, expected_output):
    '''
    Test for the get_permutations function.
        
    example_input (string): an arbitrary string to permute. Assume that
    it is a non-empty string.
    expected_output (string): the expected output for get_permutations(
    example_input)
    
    Returns: True if get_permutations returns the expected_output; False
    otherwise
    '''
    print("Input:", example_input)
    expected_output.sort()
    print("Expected Output:", expected_output)
    actual_output = get_permutations(example_input)
    actual_output.sort()
    print("Actual Output:", actual_output)
    if actual_output == expected_output:
        print("Success!")
        return True
    else:
        print("Fail!")
        return False

if __name__ == '__main__':
    example_input = ["ACE", "ABY", "LAW"]
    expected_output = [["ACE", "CAE", "EAC", "AEC", "CEA", "ECA"],
                       ["ABY", "BAY", "YAB", "AYB", "BYA", "YBA"],
                       ["LAW", "ALW", "WLA", "LWA", "AWL", "WAL"]]
    
    for i in range(len(example_input)):
        test_get_permutations(example_input[i],expected_output[i])