import re


def flatten_dict(dictionary):
    """Flattens a dictionary, removes the list attribute of value
    if len(val) is only 1

    Args:
        dictionary (dict) : the dictionary to flatten

    Example:
        >>> flatten_dict({
        ...     'a': {'x': 2, 'v': [1, 2], 'f': [3]},
        ...     'c': [5],
        ...     'b': [1, 2, 3, 4]
        ... })
        {'a': {'x': 2, 'v': [1, 2], 'f': 3}, 'c': 5, 'b': [1, 2, 3, 4]}
    """
    out = {}
    for key, value in dictionary.iteritems():
        is_list = re.match(r'\w+\[\]', key)
        if type(value) is dict and not is_list:
            out[key] = flatten_dict(value)
        elif type(value) is list and len(value) == 1 and not is_list:
            out[key] = value[0]
        else:
            out[key] = value
    return out


def merge_dicts(*args):
    """Merges dictionaries into one.

    :param args: List of dicts
    :return: Single dict
    """
    z = {}
    for x in args:
        y = x.copy()
        z.update(y)
    return z


def inverse_dict(dict):
    """Inverses a dictionary, from key-value to value-key.

    :param dict: The dictionary to be inversed
    :return: Inversed version of the dictionary
    """
    return {v: k for k, v in dict.iteritems()}
