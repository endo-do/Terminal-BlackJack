""" Functions that assist in Time """


def convert_time(time):
    """
    Converts time in seconds to a more human-readable format
    :arg time(int): time in seconds
    :return: string of time in human-readable format
    """
    if time > 60:
        time /= 60
        if time > 60:
            if time > 24:
                return f"{round(time / 1440, 2)} d"
            else:
                return f"{round(time / 60, 2)} h"
        else:
            return f"{round(time)} m"
    else:
        return f"{time} s"