from collections import namedtuple

def enum(**pairs):

    if len(set(pairs.values())) != len(pairs.values()):
        raise ValueError('enum value repeated.')

    T = namedtuple('Enum', pairs.keys())
    return T(*pairs.values())