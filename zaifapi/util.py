import inspect


def method_name():
    return inspect.stack()[1][3]