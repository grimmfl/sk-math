from typing import List


def flatten(nested_list: List) -> List:
    flat_list = []
    for item in nested_list:
        if type(item) == list:
            flat_list += flatten(item)
        else:
            flat_list.append(item)
    return flat_list
