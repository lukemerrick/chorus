import numpy as np


def as_uint8(data):
    ''' Return data encoded as unsigned 8 bit integer
    '''
    data = (data / 2 + 0.5).clip(0, 1)
    return (data * 255).astype(np.uint8)


def as_int8(data):
    ''' Return data encoded as signed 8 bit integer
    '''
    data = data.clip(-1, 1)
    return (data * 127).astype(np.int8)


def as_uint16(data):
    ''' Return data encoded as unsigned 16 bit integer
    '''
    data = (data / 2 + 0.5).clip(0, 1)
    return (data * 65535).astype(np.uint16)


def as_int16(data):
    ''' Return data encoded as signed 16 bit integer
    '''
    data = data.clip(-1, 1)
    return (data * 32767).astype(np.int16)