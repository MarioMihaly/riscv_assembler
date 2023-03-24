class InvalidLabelException(Exception):
    '''
        Exception to raise when empty label is provided, e.g. ":", ":Label".
    '''
    pass

class InvalidTokenException(Exception):
    '''
        Exception to raise when unsupported token found in assembly code.
    '''
    pass

class InvalidArgumentException(Exception):
    '''
        Exception to raise when incorrect number of arguments given.
    '''
    pass

class InvalidRegisterException(Exception):
    '''
        Exception to raise when incorrect register is provided as argument.
    '''
    pass

class InvalidAddressException(Exception):
    '''
        Exception to raise when memory address provided as hexadecimal is not valid.
    '''