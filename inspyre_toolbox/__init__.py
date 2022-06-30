from typing import NewType


def __split_evenly(target):
    """
    
    Split a target list down the center.
    
    Arguments:
        target (list):
            The list you'd like to split.

    Returns:
        (list, list):
            Two lists that should be perfectly (or as perfectly as possible
            while keeping whole numbers) split in two while maintaining
            its order.

    """
    length = len(target)
    mi = length // 2

    list1 = target[:mi]
    list2 = target[mi:]

    return list1, list2


def __split_alt(target):
    """
    
    Split a given list into two columns in an alternating format.
    
    
    ========= ===========
      Col 1      Col 2
    ========= ===========
        1          2
    --------- -----------
        3          4
    ========= ===========
    
    Args:
        target:

    Returns:

    """
    list1 = []
    list2 = []

    for item in target:
        if target.index(item) % 2 == 0:
            list1.append(item)
        else:
            list2.append(item)

    return list1, list2


def split_list(target, split_method='middle'):
    """
    
    Split a given list using an indicted method.
    
    Args:
        target:
        split_method:

    Returns:

    """
    valid_split_methods = [
            'alternating_columns',
            'middle',
    ]
    """
    valid_split_methods:
        
        * alternating_columns
        * middle
    
    Note:
        The values that will be accepted for the 'split_method'
        parameter are as follows;
        
        
    
       * alternating_columns:
        
          Sort into a number of columns where ordering goes from
          left-to-right.
          
        * middle:
        
          Split a list in half results in two smaller lists containing
          elements from the original in the same order. (The Default
          parameter value)
          
    """
    if split_method.lower() not in valid_split_methods:
        raise ValueError(f"The value for 'split_method' must be one of; {', '.join(valid_split_methods)}")
    if split_method.lower() == 'middle':
        return __split_evenly(target)
    elif split_method.lower() == 'alternating_columns':
        return __split_alt(target)


ChunkifiedList = NewType('ChunkifiedList', list)


def chunkify(target: list, num_per: int) -> ChunkifiedList:
    ret_lst = lambda target, num_per: [target[i:i + num_per] for i in range(0, len(target), num_per)]

    return ChunkifiedList(ret_lst(target, num_per))
