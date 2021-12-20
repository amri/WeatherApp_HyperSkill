try:
    exception_test()
except ZeroDivisionError:
    print("ZeroDivisionError")
except ArithmeticError:
    print("ArithmeticError")
except AssertionError:
    print("AssertionError")
except Exception:
    print("Exception")
except BaseException:
    print("BaseException")
