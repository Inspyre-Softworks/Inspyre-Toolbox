# ==============================================================================
#  Copyright (c) Inspyre Softworks 2022.                                       =
#                                                                              =
#  Author:                 T. Blackstone                                       =
#  Author Email:    <t.blackstone@inspyre.tech>                                =
#  Created:              2/19/22, 11:19 PM                                     =
# ==============================================================================


"""main_package.py

Example module showing some basic usage of the functions found in
'inspyre_softworks/__init__.py'

"""
from inspyre_toolbox import chunkify

my_lst = list(range(114))

chunked = chunkify(my_lst, 10)
print(len(chunked))
print(f'Length of element 0: {len(chunked[0])}')
print(f'Length of the last element: {len(chunked[-1])}')
print(chunked)
