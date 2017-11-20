import functools


def cache(ctype=''):
    import json
    import pickle
    from os.path import exists

    def decorator(func):
        def clean(kw, key, default=None):
            if key in kw:
                return kw.pop(key)
            return default

        @functools.wraps(func)
        def wrapper(*args, **kw):
            verbose = clean(kw, 'cverbose', True)
            usecache = clean(kw, 'usecache', True)
            if 'cache' in kw and not kw['cache']:
                kw.pop('cache')
                return func(*args, **kw)
            # read cache
            if usecache and 'cache' in kw and exists(kw['cache']):
                if verbose:
                    print('@{} reading cache'.format(func.__name__))
                if ctype == 'json':
                    with open(kw['cache']) as rf:
                        return json.load(rf)
                elif ctype == 'pickle':
                    with open(kw['cache'], 'rb') as rf:
                        return pickle.load(rf)
                elif ctype == 'text':
                    with open(kw['cache'], encoding='utf-8') as rf:
                        return rf.read()
            # create cache
            dbkey = clean(kw, 'dbkey', None)
            cachepath = clean(kw, 'cache', None)
            ret = func(*args, **kw)
            if usecache and cachepath and ret is not None:
                if verbose:
                    print('@{} creating cache'.format(func.__name__))
                if ctype == 'json':
                    with open(cachepath, 'w') as f:
                        json.dump(ret, f, indent=4)
                elif ctype == 'pickle':
                    with open(cachepath, 'wb') as f:
                        pickle.dump(ret, f)
                elif ctype == 'text':
                    with open(cachepath, 'w', encoding='utf-8') as f:
                        f.write(ret)
            return ret
        return wrapper
    return decorator


if __name__ == '__main__':
    import util
    import json

    @util.cache('text')
    def test_text():
        return 'hi'

    @util.cache('json')
    def test_json():
        return {
            '1': 1
        }

    test_json(usecache=True, cache='test_json.json')
    test_text(usecache=True, cache='test_text.json')
