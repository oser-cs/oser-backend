"""Definition of field tests.

See FieldTestMeta docstring for available field tests.
"""

from numbers import Number


# Toggle to True to print a message when a field test method is called.
PRINT_FIELD_TEST_CALLS = False


class UnsupportedFieldTest(ValueError):
    """Raised when trying to use an unsupported field test."""


class FieldTestMethodMeta(type):
    """Meta FieldTestMethod class to hold all created field test methods."""

    CLASSES = []

    def __init__(cls, name, bases, namespace):
        super().__init__(name, bases, namespace)
        if name != 'FieldTestMethod':
            type(cls).CLASSES.append(cls)


def print_called(f):
    """Decorator, prints a message when a function is called."""
    def decorated(*args, **kwargs):
        print(f'\nCalled: {f.__name__}')
        return f(*args, **kwargs)
    decorated.__name__ = f.__name__
    return decorated


class FieldTestMethod(metaclass=FieldTestMethodMeta):
    """Field test method factory.

    Use .create(attr, value) to create a test method for a specific
    (attr, value) pair.
    """

    name_formatter = None

    @classmethod
    def create(cls, field, attr, value):
        if not cls.name_formatter:
            raise ValueError(f'Name formatter not defined for {cls.__name__}')
        test_method = cls.get_test_method(field, attr, value)
        test_method.__name__ = cls.name_formatter.format(
            attr=attr, value=value)

        if PRINT_FIELD_TEST_CALLS:
            test_method = print_called(test_method)

        return test_method

    @classmethod
    def get_test_method(cls, field, attr, value):
        raise NotImplementedError

    @classmethod
    def accepts(cls, attr, value):
        raise NotImplementedError

    @staticmethod
    def all():
        """Return the list of available field test methods."""
        return FieldTestMethodMeta.CLASSES

    @staticmethod
    def name_from_func(f):
        words = f.__name__.split('_')
        name = ''.join(word.capitalize() for word in words)
        return '{}FieldTestMethod'.format(name)


def field_test_method(name_formatter=None, accept=None):
    """Decorator to easily create field test methods."""
    if accept is None:
        def accept(attr, value):
            return True

    def create_test_method(f):
        formatter = name_formatter

        class MyFieldTestMethod(FieldTestMethod):

            name_formatter = formatter

            @classmethod
            def get_test_method(cls, field_name, attr, value):
                def test_method(self):
                    field = self.model._meta.get_field(field_name)
                    f(self, field, attr, value)
                return test_method

            @classmethod
            def accepts(cls, attr, value):
                acc = accept(attr, value)
                # status = 'accepted' if acc else 'rejected'
                # print(f'{cls.__name__} {status} {attr}')
                return acc

        MyFieldTestMethod.__name__ = FieldTestMethod.name_from_func(f)

    return create_test_method


@field_test_method(name_formatter='test_{attr}_is_{value}',
                   accept=lambda attr, value: isinstance(value, bool))
def test_bool(self, field, attr, value):
    """Test that a field attribute is True or False according to value."""
    if value is True:
        self.assertTrue(getattr(field, attr))
    else:
        self.assertFalse(getattr(field, attr))


@field_test_method(name_formatter='test_{attr}_value',
                   accept=lambda attr, value: isinstance(value, str))
def test_string_equals(self, field, attr, value):
    """Test that a field attribute is the given string value."""
    self.assertEqual(getattr(field, attr), value)


@field_test_method(name_formatter='test_{attr}_value',
                   accept=lambda attr, value: isinstance(value, Number))
def test_number_equals(self, field, attr, value):
    """Test that a field attribute is the given number value."""
    self.assertEqual(getattr(field, attr), value)


@field_test_method(name_formatter='test_{attr}_choices',
                   accept=lambda attr, value: attr == 'choices')
def test_choices_equals(self, field, attr, value):
    """Test that a field choices are the given choice tuple."""
    self.assertEqual(getattr(field, 'choices'), value)


class FieldTestMeta(type):
    """Abstract field test meta.

    Manages the creation of field test methods.
    """

    SUPPORTED_TESTS_DOCSTRING = """\n
    Supported tests
    ---------------
    Boolean value test:
        'unique': True
    String equality test:
        'verbose_name': 'my-field-verbose-name'
    Number equality test:
        'max_length': 200
    Field choices equality test:
        'choices': (('C1', 'option 1'), ('C2', 'option 2'))
    """

    def __new__(metacls, name, bases, namespace):
        cls = super().__new__(metacls, name, bases, namespace)
        cls.__doc__ += FieldTestMeta.SUPPORTED_TESTS_DOCSTRING
        return cls

    def __init__(cls, name, bases, namespace):
        super().__init__(name, bases, namespace)
        type(cls).before_dispatch(cls, name, bases, namespace)
        type(cls).dispatch(cls)

    def before_dispatch(cls, name, bases, namespace):
        """Callback called before the field test methods are created."""
        pass

    @classmethod
    def dispatch_field(metacls, cls, tests, field_name):
        """Create test methods for a single field."""
        for attr, value in tests.items():
            type(cls).add_test_method(cls, field_name, attr, value)

    @classmethod
    def dispatch(metacls, cls):
        raise NotImplementedError('Subclasses must implement dispatch()')

    @classmethod
    def add_test_method(metacls, cls, field, attr, value):
        test_method_cls = metacls.find_test_method(cls, attr, value)
        test_method = test_method_cls.create(field, attr, value)
        setattr(cls, test_method.__name__, test_method)

    @classmethod
    def find_test_method(metacls, cls, attr, value):
        for test_method_cls in FieldTestMethod.all():
            if test_method_cls.accepts(attr, value):
                return test_method_cls
        raise ValueError(f'Unsupported field test: {attr}')
