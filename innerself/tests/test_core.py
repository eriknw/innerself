from pytest import raises
from innerself import innerself, innercls

global_val = 100


def test_simple_method():
    class A:
        @innerself
        def __init__(self, x):
            y = x + 1

        @innerself
        def f(self):
            z = x + y
            return z + 1

    a = A(1)
    assert a.__dict__ == {"x": 1, "y": 2}
    assert a.f() == 4
    assert a.__dict__ == {"x": 1, "y": 2, "z": 3}
    assert A.f(a) == 4


def test_simple_generator():
    class A:
        @innerself
        def gen(self, x):
            for i in range(x):
                yield i
            return 2 * x

    a = A()
    assert list(a.gen(3)) == [0, 1, 2]
    assert a.__dict__ == {"x": 3, "i": 2}
    assert list(A.gen(a, 3)) == [0, 1, 2]
    it = a.gen(5)
    try:
        while True:
            next(it)
    except StopIteration as exc:
        value = exc.value
    assert value == 10


def test_readonly():
    class A:
        @innerself
        def __init__(self, x, y):
            pass

        @innerself(readonly=True)
        def f(self, a):
            z = a + x + y
            return z + 1

        @innerself(readonly=True)
        def gen(self, a):
            for i in range(a + x + y):
                yield i

    a = A(1, 2)
    assert a.__dict__ == {"x": 1, "y": 2}
    assert a.f(3) == 7
    assert a.__dict__ == {"x": 1, "y": 2}
    assert list(a.gen(3)) == list(range(6))
    assert a.__dict__ == {"x": 1, "y": 2}


def test_outer_scope():
    closure_val = 10

    class A:
        @innerself
        def __init__(self, x, y):
            x_global = x + global_val
            y_closure = y + closure_val

    a = A(1, 2)
    assert a.__dict__ == {"x": 1, "y": 2, "x_global": 101, "y_closure": 12}


def test_exceptional():
    def func(*args):
        return args  # pragma: no cover

    with raises(TypeError, match="expects a Python function"):
        innerself(1)
    with raises(TypeError, match="only works on methods"):
        innerself(func)()
    with raises(TypeError, match="does not have `__dict__` attribute"):
        innerself(func)(1)


def classdict(cls):
    class A:
        pass

    return {key: val for key, val in cls.__dict__.items() if key not in A.__dict__}


def test_classmethods():
    class A:
        x = 1

        @innercls
        def f(cls, y):
            z = x + y
            return z + 1

    assert A.f(2) == 4
    assert classdict(A) == {"x": 1, "y": 2, "z": 3, "f": A.__dict__["f"]}
    a = A()
    assert a.f(3) == 5
    assert classdict(A) == {"x": 1, "y": 3, "z": 4, "f": A.__dict__["f"]}

    class B:
        x = 1

        @innercls(readonly=True)
        def f(cls, y):
            z = x + y
            return z + 1

        @classmethod
        @innercls(readonly=True)
        def g(cls, a):
            b = x + a
            return b + 2

        @innercls(readonly=True)
        @classmethod
        def h(cls, c):
            d = x + c
            return d + 3

        @innercls
        def gen(cls, length):
            yield from range(length)

    d = {key: B.__dict__[key] for key in ["x", "f", "g", "h", "gen"]}
    assert classdict(B) == d
    assert B.f(2) == 4
    assert classdict(B) == d
    assert B.g(3) == 6
    assert classdict(B) == d
    assert B.h(4) == 8
    assert classdict(B) == d
    b = B()
    assert list(b.gen(5)) == list(range(5))
    assert classdict(B) == dict(d, length=5)

    @innercls
    def func(cls, length):
        return x + length

    f = func.__get__(b)  # weird, but valid
    assert f(10) == 11
    assert classdict(B) == dict(d, length=10)

    @innercls(readonly=True)
    def genfunc(cls, data):
        yield data
        yield data + 1

    gen = genfunc.__get__(b)  # weird, but valid
    assert list(gen(5)) == [5, 6]
    assert classdict(B) == dict(d, length=10)
