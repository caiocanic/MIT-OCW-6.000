# 6.0002 Problem Set 1b: Space Change

def dp_make_weight(egg_weights, target_weight, memo = {0:0}):
    """
    Find number of eggs to bring back, using the smallest number of
    eggs. Assumes there is an infinite supply of eggs of each weight,
    and there is always a egg of value 1.
    
    Parameters:
    egg_weights - tuple of integers, available egg weights sorted
    descending
    target_weight - int, amount of weight we want to find eggs to fit
    memo - dictionary, OPTIONAL parameter for memoization (you may not
    need to use this parameter depending on your implementation)
    
    Returns: int, smallest number of eggs needed to make target weight
    """
    if target_weight == 0:
        return memo[0]
    try:
        return memo[target_weight]
    except KeyError:
        result = []
        for egg in egg_weights:
            new_target_weight = target_weight - egg
            if new_target_weight >= 0:
                result.append(1 + dp_make_weight(egg_weights,
                                                 new_target_weight))
        memo[target_weight] = min(result)
        return memo[target_weight]

if __name__ == '__main__':
    egg_weights = (1, 5, 10, 25)
    n = 99
    print("Egg weights = (1, 5, 10, 25)")
    print("n = 99")
    print("Expected ouput: 9 (3 * 25 + 2 * 10 + 4 * 1 = 99)")
    print("Actual output:", dp_make_weight(egg_weights, n))
    print()