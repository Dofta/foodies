#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os
from datetime import datetime
from typing import Callable, Sequence, Text
from functools import wraps
import logging
from logging.handlers import TimedRotatingFileHandler
from functools import partial


class Logger(object):
    def __new__(cls):
        if '_inst' not in vars(cls):
            cls._inst = super(Logger, cls).__new__(cls)
            cls._inst.formatter = logging.Formatter(
                "%(asctime)s - %(name)s::%(lineno)s - %(message)s",
                datefmt="%Y-%m-%d %H:%M:%S")
            cls._inst.fhs = []
            cls._inst.ch = logging.StreamHandler()
            cls._inst.init()
        return cls._inst

    def init(self) -> None:
        self.init_file_handler('debug.log', logging.DEBUG)
        self.init_file_handler('error.log', logging.ERROR)
        self.init_file_handler('info.log', logging.INFO)
        self.init_file_handler('warning.log', logging.WARNING)
        self.init_stream_handler()

    def init_file_handler(self, logname: str, level: int) -> None:
        root = os.path.join(os.path.abspath(''), 'log')
        if not os.path.isdir(root):
            os.makedirs(root)
        path = os.path.join(root, logname)
        fh = TimedRotatingFileHandler(filename=path, when='D', backupCount=7, encoding='utf-8')
        fh.setLevel(level)
        fh.setFormatter(self.formatter)
        self.fhs.append(fh)

    def init_stream_handler(self) -> None:
        self.ch = logging.StreamHandler()
        self.ch.setLevel(logging.INFO)
        self.ch.setFormatter(self.formatter)

    def get_logger(self, name: str) -> logging.Logger:
        name = os.path.basename(name)
        logger = logging.getLogger(name)
        if not logger.handlers:
            logger.setLevel(logging.DEBUG)
            if not self.ch is None:
                logger.addHandler(self.ch)
            for fh in self.fhs:
                logger.addHandler(fh)
        return logger


def log_func(name='', shield_args=(), log_return=True, logger=Logger().get_logger(__file__)):
    # type: (Text, Sequence[Text], bool, logging.Logger) -> Callable
    """
    用于函数日志记录的装饰器

    Args:
        name: 函数注释
        shield_args: 屏蔽的参数列表
        log_return: 是否将 return 值记录到日志中
        logger: 设置发送报警的 logger，默认用全局的 logger

    Examples:
        在定义需要日志记录的函数时使用 ::

            @log_method('函数作用', shield_args=['password'])
            def function(user, password):
                pass
    """

    def wrapper(func):
        arg_names = func.__code__.co_varnames
        func.__doc__ = '{name}\n{doc}'.format(name=name, doc=func.__doc__)

        @wraps(func)
        def wrapper_func(*args, **kwargs):
            # 处理参数为 kwargs
            for key, value in zip(arg_names, args):
                if key in kwargs:
                    raise TypeError("{func_name}() got multiple values for argument '{arg_name}'".format(
                        func_name=func.__name__,
                        arg_name=key,
                    ))
                kwargs[key] = value

            func_str = '{module_name}.{func_name}'.format(
                module_name=func.__module__,
                func_name=func.__name__,
            )
            args_str = ', '.join('{arg_name}={arg_value}'.format(
                arg_name=key,
                arg_value=value if key not in shield_args else '***',
            ) for key, value in kwargs.items())
            logger.debug(hidden_text('-> %s(%s): %s' % (func_str, name, args_str)))

            begin = datetime.now()
            try:
                result = func(**kwargs)
            except Exception as error:
                logger.error(
                    hidden_text(
                        '<-!! %s(%.2fs): (%s) %s' % (
                            func_str,
                            (datetime.now() - begin).total_seconds(),
                            type(error).__name__,
                            Text(error)
                        )
                    )
                )
                error.func_str = '{func_str}({name})'.format(
                    func_str=func_str,
                    name=name,
                )
                raise
            else:
                logger.debug(
                    hidden_text(
                        '<- %s(%.2fs): %s' % (
                            func_str,
                            (datetime.now() - begin).total_seconds(),
                            Text(result) if log_return else '***'
                        )
                    )
                )
            return result

        return wrapper_func

    return wrapper


def log_method(name='', shield_args=(), log_return=True, logger=Logger().get_logger(__file__)):
    # type: (Text, Sequence[Text], bool, logging.Logger) -> Callable
    """
    用于类方法日志记录的装饰器

    Args:
        name: 函数注释
        shield_args: 屏蔽的参数列表
        log_return: 是否将 return 值记录到日志中
        logger: 设置发送报警的 logger，默认用全局的 logger

    Examples:
        在定义需要日志记录的类方法时使用 ::

            class CustomClass(object):
                @log_method('方法作用', shield_args=['password'])
                def function(user, password):
                    pass
    """

    def wrapper(func):
        arg_names = func.__code__.co_varnames[1:]
        func.__doc__ = '{name}\n{doc}'.format(name=name, doc=func.__doc__)

        @wraps(func)
        def wrapper_func(self, *args, **kwargs):
            # 处理参数不对的情况
            for key, value in zip(arg_names, args):
                if key in kwargs:
                    raise TypeError("{func_name}() got multiple values for argument '{arg_name}'".format(
                        func_name=func.__name__,
                        arg_name=key,
                    ))
                kwargs[key] = value

            func_str = '{class_name}.{func_name}'.format(
                class_name=self.__class__.__name__,
                func_name=func.__name__,
            )
            args_str = ', '.join('{arg_name}={arg_value}'.format(
                arg_name=key,
                arg_value=value if key not in shield_args else '***',
            ) for key, value in kwargs.items())
            logger.debug(hidden_text('-> %s(%s): %s' % (func_str, name, args_str)))

            begin = datetime.now()
            try:
                result = func(self, **kwargs)
            except Exception as error:  # pylint: disable=broad-except
                logger.error(
                    hidden_text(
                        '<-!! %s(%.2fs): (%s) %s' % (
                            func_str,
                            (datetime.now() - begin).total_seconds(),
                            type(error).__name__,
                            Text(error)
                        )
                    )
                )
                error.func_str = '{func_str}({name})'.format(
                    func_str=func_str,
                    name=name,
                )
                raise
            else:
                logger.debug(
                    hidden_text(
                        '<- %s(%.2fs): %s' % (
                            func_str,
                            (datetime.now() - begin).total_seconds(),
                            Text(result) if log_return else '***'
                        )
                    )
                )
            return result

        return wrapper_func

    return wrapper


def make_decorator_for_func(name: str) -> log_func:
    return partial(log_func, logger=Logger().get_logger(name))


def make_decorator_for_method(name: str) -> log_method:
    return partial(log_method, logger=Logger().get_logger(name))


def hidden_text(text, max_len=1000):
    if len(text) > max_len:
        text = text[:max_len] + ' ......长度超出%s的信息自动隐藏，请合理控制输出' % max_len
    return text


if __name__ == '__main__':

    logger = Logger().get_logger(__file__)
    logger.debug('debug')
    logger.info('info')
    logger.warning('warning')
    logger.error('error1')
    logger = Logger().get_logger('aaaaaaaaa')
    logger.debug('debug')
    logger.info('info')
    logger.warning('warning')
    logger.error('error2')

    log_method = partial(log_method, logger=logger)
    log_func = partial(log_func, logger=logger)

    class MyLog(object):
        @log_method(name='测试类方法打日志')
        def run(self, a, b):
            return a + b   # aaabbb

    my_log = MyLog()
    my_log.run('aaa', 'bbb')

    @log_func(name='测试函数打日志')
    def my_log_func(a, b):
        return a + b

    my_log_func('aaa', 'bbb')

