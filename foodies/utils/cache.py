#!/usr/bin/env python
# -*- coding: utf-8 -*-
import json
import time


class CacheMng(object):
    def __new__(cls, *args, **kwargs):
        if '_inst' not in vars(cls):
            cls._inst = super(CacheMng, cls).__new__(cls)
            cls._inst.cache_map = {}
        return cls._inst

    def get_or_create(self, func, *args, **kwargs):
        func_name = func.__name__
        args_key = json.dumps([str(i) for i in args])
        kwargs_key = json.dumps(['%s:%s' % (k, v) for k, v in kwargs.items()])
        self.cache_map.setdefault(func_name, {})
        self.cache_map[func_name].setdefault(args_key, {})
        self.cache_map[func_name][args_key].setdefault(kwargs_key, None)
        if not self.cache_map[func_name][args_key][kwargs_key]:
            value = func(*args, **kwargs)
            if value:
                cache = Cache(func_name, args_key, kwargs_key, value)
                self.cache_map[func_name][args_key][kwargs_key] = cache
            else:
                del self.cache_map[func_name][args_key][kwargs_key]
                return value
        return self.cache_map[func_name][args_key][kwargs_key]

    def remove(self, cache):
        func_name = cache.func_name
        args_key = cache.args_key
        kwargs_key = cache.kwargs_key
        del self.cache_map[func_name][args_key][kwargs_key]


class Cache(object):
    def __init__(self, func_name, args_key, kwargs_key, value=None):
        self.create_time = time.time()
        self.func_name = func_name
        self.args_key = args_key
        self.kwargs_key = kwargs_key
        self.value = value


class SetupCache(object):
    def __init__(self, timeout=3600):
        self.timeout = timeout

    def __call__(self, func):
        def __call__(*args, **kwargs):
            now = time.time()
            cachemng = CacheMng()
            cache = cachemng.get_or_create(func, *args, **kwargs)
            if cache:
                if now - cache.create_time > self.timeout:
                    cachemng.remove(cache)
                    cache = cachemng.get_or_create(func, *args, **kwargs)
                return cache.value
            else:
                return cache
        return __call__


@SetupCache(timeout=5)
def text(p, c):
    print('new call')
    return p, c

class Text(object):

    @SetupCache(timeout=5)
    def text(self, p, c):
        print('new call')
        return p, c

    @property
    @SetupCache(timeout=5)
    def text2(self):
        print('new set')
        return 'text2'



if __name__ == '__main__':
    print(text(5, 2))
    print(text(5, 2))
    time.sleep(2)
    print(text(5, 2))
    print(text(5, 2))
    print(text(5, 3))
    print(text(5, 2))
    time.sleep(3)
    print(text(5, 2))
    print('-------------------')
    t = Text()
    t2 = Text()
    print(t.text(5, 2))
    print(t2.text(5, 2))
    print(t.text(5, 2))
    print(t2.text(5, 2))
    print(t.text2)
    print(t.text2)
    print(t2.text2)
    print(t2.text2)
    time.sleep(2)
    print(t.text(5, 2))
    print(t.text(5, 2))
    print(t.text(5, 3))
    print(t.text(5, 2))
    print(t.text2)
    print(t2.text2)
    time.sleep(3)
    print(t.text(5, 2))
    print(t.text2)
    print(t2.text2)
    print(t.text2)
    print(t2.text2)