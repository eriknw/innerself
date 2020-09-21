from functools import partial, update_wrapper
from inspect import isgeneratorfunction
from types import MethodType
from innerscope import scoped_function


class InnerSelf:
    _instance_name = "self"
    _is_generatorfunction = False

    def __init__(self, func, *, readonly=False):
        update_wrapper(self, func)
        self.func = func
        self.readonly = readonly
        # don't bind outer scope yet
        self._scoped_func = scoped_function(func, use_closures=False, use_globals=False)

    def __get__(self, instance, owner=None):
        if instance is None:
            return self
        return MethodType(self, instance)

    def __call__(self, *args, **kwargs):
        [rv] = self._call(*args, **kwargs)
        return rv

    def _call(self, *args, **kwargs):
        if not args:
            raise TypeError(
                f'"{self._instance_name}" argument not found.  `innerself` only works on '
                "methods.  The first argument is expected to be the bound instance "
                f'(i.e., "{self._instance_name}").'
            )
        instance = args[0]
        try:
            d = instance.__dict__
        except AttributeError:
            raise TypeError(
                f'The "{self._instance_name}" argument does not have `__dict__` attribute.  '
                "`innerself` only works on methods of objects with `__dict__` attribute.  "
                f"Got type: {type(instance)}"
            )
        func = scoped_function(self._scoped_func, d)
        scope = func(*args, **kwargs)
        if self._is_generatorfunction:
            scope = yield from scope
        else:
            yield scope.return_value
        if not self.readonly:
            scope.inner_scope.pop(self._instance_name, None)
            if hasattr(d, "update"):
                d.update(scope.inner_scope)
            else:
                for key, val in scope.inner_scope.items():
                    setattr(instance, key, val)
        return scope.return_value


class InnerSelfGeneratorFunction(InnerSelf):
    _is_generatorfunction = True

    def __call__(self, *args, **kwargs):
        gen = self._call(*args, **kwargs)
        rv = yield from gen
        return rv


def innerself(func=None, *, readonly=False):
    if func is None:
        return partial(innerself, readonly=readonly)
    if isgeneratorfunction(func):
        return InnerSelfGeneratorFunction(func, readonly=readonly)
    else:
        return InnerSelf(func, readonly=readonly)


class InnerCls(InnerSelf):
    _instance_name = "cls"
    _is_generatorfunction = False

    def __get__(self, instance, owner=None):
        if owner is None and instance is not None:
            owner = type(instance)
        return MethodType(self, owner)


class InnerClsGeneratorFunction(InnerSelfGeneratorFunction):
    _instance_name = "cls"
    _is_generatorfunction = True

    def __get__(self, instance, owner=None):
        if owner is None and instance is not None:
            owner = type(instance)
        return MethodType(self, owner)


def innercls(func=None, *, readonly=False):
    if func is None:
        return partial(innercls, readonly=readonly)
    if type(func) is classmethod:
        func = func.__func__
    if isgeneratorfunction(func):
        return InnerClsGeneratorFunction(func, readonly=readonly)
    else:
        return InnerCls(func, readonly=readonly)
