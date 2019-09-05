import os
This_url = os.path.dirname(__file__)
__all__ = []
for i in os.listdir(This_url):
    if os.path.isdir(os.path.join(This_url, i)):
        __all__.append(i)
    elif i == '__init__.py':
        pass
    else:
        sp = i.split('.')
        if sp[-1] == 'py':
            __all__.append(sp[0])