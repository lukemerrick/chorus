import numpy as np
import math

def get_phase(data, new_volume = 1.0):
    ''' Takes a np array of a wave and returns the phase shift
        needed to keep the sound going without popping sounds
    '''
    downstroke = data[-2] - data[-1] > 0
    raw_phase = np.arcsin(data[-1] / new_volume) / (math.pi*2)
    if downstroke:
        if data[-1] > 0:
            return(.5-raw_phase)
        else:
            return(1+(-.5-raw_phase))
    else:
        if data[-1] > 0:
            return raw_phase
        else:
            return 1+raw_phase