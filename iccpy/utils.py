from numpy import *

class Struct:
    """
    Generic class that converts named constructor arguments into class members
    """
    def __init__(self, *args, **kwds):
        for arg in args:
            self.__dict__.update(arg)
        self.__dict__.update(kwds)
        
    def __repr__(self):
        return str(self.__dict__)

def match(arr1, arr2, arr2_sorted=False):
    """
    For each element in arr1 return the index of the element with the
    same value in arr2, or -1 if there is no element with the same value.
    Setting arr2_sorted=True will save some time if arr2 is already sorted
    into ascending order.

    It is assumed that each element in arr1 only occurs once in arr2.
    """

    # Workaround for a numpy bug (<=1.4): ensure arrays are native endian
    # because searchsorted ignores endian flag
    if not(arr1.dtype.isnative):
        arr1_n = asarray(arr1, dtype=arr1.dtype.newbyteorder("="))
    else:
        arr1_n = arr1
    if not(arr2.dtype.isnative):
        arr2_n = asarray(arr2, dtype=arr2.dtype.newbyteorder("="))
    else:
        arr2_n = arr2

    # Sort arr2 into ascending order if necessary
    tmp1 = arr1_n
    if arr2_sorted:
        tmp2 = arr2_n
        idx = slice(0,len(arr2_n))
    else:
        idx = argsort(arr2_n)
        tmp2 = arr2_n[idx]

    # Find where elements of arr1 are in arr2
    ptr  = searchsorted(tmp2, tmp1)

    # Make sure all elements in ptr are valid indexes into tmp2
    # (any out of range entries won't match so they'll get set to -1
    # in the next bit)
    ptr[ptr>=len(tmp2)] = 0
    ptr[ptr<0]          = 0

    # Return -1 where no match is found
    ind  = tmp2[ptr] != tmp1
    ptr[ind] = -1

    # Put ptr back into original order
    ind = arange(len(arr2_n))[idx]
    ptr = where(ptr>= 0, ind[ptr], -1)

    return ptr