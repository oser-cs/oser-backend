"""Definition of field tests.

See FieldTestMeta docstring for available field tests.
"""

# Toggle to True to print a message when a field test method is called.
PRINT_FIELD_TEST_CALLS = False


class UnsupportedFieldTest(ValueError):
    """Raised when trying to use an unsupported field test."""


class FieldTestMeta(type):
    """Abstract field test meta.

    Manages the creation of field test methods.
    """

    SUPPORTED_TESTS_DOCSTRING = """\n
    Supported tests
    ---------------
    Boolean value test:
        'unique': True
    Verbose name equality test:
        'verbose_name': 'my-field-verbose-name'
    Field choices equality test:
        'choices': (('C1', 'option 1'), ('C2', 'option 2'))
    Equality test (the default):
        'my_attr': 'my-attr-value'
    """

    def __new__(metacls, name, bases, namespace):
        cls = super().__new__(metacls, name, bases, namespace)
        if not cls.__doc__:
            cls.__doc__ = ""
        cls.__doc__ += FieldTestMeta.SUPPORTED_TESTS_DOCSTRING
        cls._generated_tests = []
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
    def add_test_method(metacls, cls, field_name, attr, value):
        field_test_method = metacls.find_test_method(cls, attr, value)
        test_method = field_test_method.create(field_name, attr, value)
        test_name = test_method.__name__
        cls._generated_tests.append(test_name)
        setattr(cls, test_name, test_method)

    @classmethod
    def find_test_method(metacls, cls, attr, value):
        for field_test_method in FieldTestMethod.all():
            if field_test_method.accepts(attr, value):
                return field_test_method
        raise UnsupportedFieldTest(attr)


class FieldTestMethodMeta(type):
    """Meta FieldTestMethod class to hold all created field test methods."""

    METHODS = []

    def __init__(cls, name, bases, namespace):
        super().__init__(name, bases, namespace)
        abstract = namespace.get('abstract', False)
        cls.abstract = abstract
        if abstract is not True:
            type(cls).METHODS.append(cls)


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
    abstract = True

    def create(self, field_name, attr, value):
        if not self.name_formatter:
            raise ValueError(
                f'Name formatter not defined for {self.__class____name__}')
        test_method = self._get_test_method(field_name, attr, value)
        test_method.__name__ = self.name_formatter.format(
            field=field_name, attr=attr, value=value).lower()

        if PRINT_FIELD_TEST_CALLS:
            test_method = print_called(test_method)

        return test_method

    def accepts(self, attr, value):
        raise NotImplementedError

    @staticmethod
    def test_field(self, field, attr, value):
        raise NotImplementedError

    def _get_test_method(self, field_name, attr, value):
        test_field = self.test_field

        def test_method(self):
            field = self.model._meta.get_field(field_name)
            test_field(self, field, attr, value)

        return test_method

    @staticmethod
    def all():
        """Return the list of available field test methods."""
        return [method_cls() for method_cls in FieldTestMethodMeta.METHODS]


# Register field test methods here

class BoolFieldTestMethod(FieldTestMethod):
    """Test that a field attribute is True or False according to value."""

    name_formatter = 'test_{field}_{attr}_is_{value}'

    def accepts(self, attr, value):
        return isinstance(value, bool)

    @staticmethod
    def test_field(self, field, attr, value):
        if value is True:
            self.assertTrue(getattr(field, attr))
        else:
            self.assertFalse(getattr(field, attr))


class AttrEqualsTestMethod(FieldTestMethod):
    """Test a field attribute value for equality."""

    name_formatter = 'test_{field}_{attr}_value'

    def accepts(self, attr, value):
        return attr not in ('verbose_name', 'choices')

    @staticmethod
    def test_field(self, field, attr, value):
        self.assertEqual(getattr(field, attr), value)


class VerboseNameFieldTestMethod(AttrEqualsTestMethod):
    """Test a field verbose name."""

    name_formatter = 'test_{field}_verbose_name'

    def accepts(self, attr, value):
        return attr == 'verbose_name'


class ChoicesEqualTestMethod(AttrEqualsTestMethod):
    """Test the choices of a field."""

    name_formatter = 'test_{field}_{attr}_value'

    def accepts(self, attr, value):
        return attr == 'choices'
