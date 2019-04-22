import datetime


def to_list(func):
    def inner():
        lista = []
        for letter in func():
            lista.append(letter)
        return lista
    return inner


@to_list
def say_python():
    return 'Python'


def is_correct(*args):
    def correct(func):
        def inner():
            dic = func()
            for elem in args:
                if elem not in dic:
                    return None
            return func()
        return inner
    return correct


""""@is_correct('first_name', 'last_name')
def get_data():
    return {
        'first_name': 'Jan',
        'last_name': 'Kowalski',
        'email': 'jan@kowalski.com'
    }
"""


@is_correct('first_name', 'last_name', 'email')
def get_other_data():
    return {
        'first_name': 'Jan',
        'email': 'jan@kowalski.com'
    }


def add_date(format):
    def correct(func):
        def inner():
            dic = func()
            dat = datetime.datetime.now()
            dic['date'] = datetime.date.strftime(dat, format)
            return dic
        return inner
    return correct


@add_date('%A %d. %B %Y')
def get_data():
    return {1: 2, 'name': 'Jan'}


def main():
    print(get_data())


if __name__ == "__main__":
    main()
