import eel

eel.init('gui')

@eel.expose
def say_hello_py(x):
    print('Hello from %s' % x)

say_hello_py('Python World!')


eel.start('hello.html', size=(300, 200))