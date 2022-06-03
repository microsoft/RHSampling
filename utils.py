def format_e(n):
    '''Return a string representing the exponential notation of n (n is of Decimal type)
    '''
    a = '%E' % n
    return a.split('E')[0].rstrip('0').rstrip('.') + 'E' + a.split('E')[1]

def colored(r, g, b, text):
    '''Return text in color as per r, g, and b values
    '''
    return "\033[38;2;{};{};{}m{} \033[38;2;255;255;255m".format(r, g, b, text)

def InclusiveRange(start, stop):
    return range(start, stop + 1)