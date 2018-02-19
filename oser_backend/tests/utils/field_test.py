"""Definition of field tests.

See FieldTestMeta docstring for available field tests.
"""

from django.core.exceptions import FieldDoesNotExist

# Toggle to True to print a message when a field test method is called.
PRINT_FIELD_TEST_CALLS = False


def print_called(f):
    """Decorator, prints a message when a function is called."""
    def decorated(*args, **kwargs):
        print('\nCalled: {}'.format(f.__name__))
        return f(*args, **kwargs)
    decorated.__name__ = f.__name__
    return decorated


class UnsupportedFieldTest(ValueError):
    """Raised when trying to use an unsupported field test."""


class UnsupportedModelTest(ValueError):
    """Raised when trying to use an unsupported model test."""


class ModelTestCaseMeta(type):
    """Metaclass for ModelTestCase.

    Dynamically creates tests based on the class' field_tests and
    model_tests dictionaries.
    """

    SUPPORTED_TESTS_DOCSTRING = """\n
    Supported field tests
    ---------------------
    Boolean value test:
        'unique': True
    Verbose name equality test:
        'verbose_name': 'my-field-verbose-name'
    Field choices equality test:
        'choices': (('C1', 'option 1'), ('C2', 'option 2'))
    Equality test (the default):
        'my_attr': 'my-attr-value'

    Supported model tests
    ---------------------
    """

    model_attr_name = 'model'
    _field_tests_attr_name = 'field_tests'
    _model_tests_attr_name = 'model_tests'

    def __new__(metacls, name, bases, namespace):
        cls = super().__new__(metacls, name, bases, namespace)
        # registry of test methods generated for a model test case
        cls._generated_tests = []
        return cls

    def __init__(cls, name, bases, namespace):
        super().__init__(name, bases, namespace)
        type(cls).before_dispatch(cls, name, bases, namespace)
        type(cls).dispatch(cls)

    @classmethod
    def add_test_method(metacls, cls, attr, value, kind, not_found_exception,
                        **kwargs):
        """Add a test method to a model test case."""
        factory = metacls.find_factory(
            cls, attr, value, kind, not_found_exception)
        test_method = factory.create(attr, value, **kwargs)
        test_name = test_method.__name__
        cls._generated_tests.append(test_name)
        setattr(cls, test_name, test_method)

    @classmethod
    def find_factory(metacls, cls, attr, value, kind, not_found_exception):
        """Find a test method accepting the (attr, value) pair."""
        model_cls = getattr(cls, metacls.model_attr_name)
        for factory in BaseTestFactory.all(model_cls):
            if factory.kind == kind and factory.accepts(attr, value):
                return factory
        raise not_found_exception(attr)

    @classmethod
    def before_dispatch(metacls, cls, name, bases, namespace):
        """Called before test methods are created."""
        model_attr_name = metacls.model_attr_name
        if not hasattr(cls, model_attr_name):
            raise AttributeError(
                '{} attribute not defined for {}'.format(model_attr_name,
                                                         cls.__name__))

        if ('tests' in namespace and
                cls._field_tests_attr_name not in namespace):
            raise AttributeError(
                '{} field tests should be defined in {}, not tests (in {})'
                .format(model_attr_name, cls._field_tests_attr_name,
                        cls.__name__)
            )

    @classmethod
    def dispatch_field(metacls, cls, tests, field_name):
        """Create test methods for a single field."""
        for attr, value in tests.items():
            type(cls).add_test_method(
                cls, attr, value, 'field', UnsupportedFieldTest,
                field_name=field_name)

    @classmethod
    def dispatch_model(metacls, cls, tests):
        """Create test methods for the model."""
        for attr, value in tests.items():
            type(cls).add_test_method(
                cls, attr, value, 'model', UnsupportedModelTest)

    @classmethod
    def dispatch(metacls, cls):
        """Create the test methods for the model test case."""
        # create model tests
        model_tests = getattr(cls, metacls._model_tests_attr_name)
        type(cls).dispatch_model(cls, model_tests)
        # create field tests
        field_tests = getattr(cls, metacls._field_tests_attr_name)
        for field_name, tests in field_tests.items():
            type(cls).dispatch_field(cls, tests, field_name)


class TestFactoryMeta(type):
    """TestFactory metaclass to hold all created test methods.

    Set `abstract = True` on a test factory class to prevent from
    registering it in METHODS.
    """

    METHODS = []

    def __init__(cls, name, bases, namespace):
        super().__init__(name, bases, namespace)
        abstract = namespace.get('abstract', False)
        cls.abstract = abstract
        if not abstract:
            type(cls).METHODS.append(cls)


class BaseTestFactory(metaclass=TestFactoryMeta):
    """Base test method factory.

    Use .create(attr, value, **kwargs) to create a test method for a specific
    (attr, value) pair. The **kwargs dict is determined by concrete subclasses.

    Parameters
    ----------
    model_cls : subclass of django.db.models.Model

    Attributes
    ----------
    name_formatter : str
    abstract : bool
    kind : 'field' or 'model'
    """

    name_formatter = None
    abstract = True
    kind = None

    def __init__(self, model):
        self.model = model

    def create(self, attr, value, **kwargs):
        if not self.name_formatter:
            raise ValueError(
                'Name formatter not defined for {}'
                .format(self.__class____name__))
        test_method = self._get_test_method(attr, value, **kwargs)
        test_method.__name__ = self.format_name(
            attr, value, **kwargs).lower()

        if PRINT_FIELD_TEST_CALLS:
            test_method = print_called(test_method)

        return test_method

    def format_name(self, attr, value, **kwargs):
        """Format the test method name using self.name_formatter."""
        return self.name_formatter.format(attr=attr, value=value)

    def accepts(self, attr, value):
        """Say if the method perform the test for this (attr, value) pair."""
        raise NotImplementedError

    @staticmethod
    def perform_test(attr, value, **kwargs):
        """Perform the test: make use of asserts here."""
        raise NotImplementedError

    def get_test_kwargs(self, **kwargs):
        """Return kwargs to pass to the perform_test() function.

        Parameters
        ----------
        **kwargs : dict
            As passed in .create().
        """
        return {}

    def _get_test_method(self, attr, value, **kwargs):
        perform_test = self.perform_test
        test_kwargs = self.get_test_kwargs(**kwargs)

        def test_method(self):
            perform_test(self, attr, value, **test_kwargs)

        return test_method

    @classmethod
    def all(cls, model_cls):
        """Return the list of available field test methods.

        Parameters
        ---------
        model_cls : django.db.models.Model subclass
        """
        return [method_cls(model_cls)
                for method_cls in TestFactoryMeta.METHODS]


class FieldTestFactory(BaseTestFactory):
    """Field test method factory.

    Use .create(attr, value, field_name) to create a test method for a specific
    (attr, value) pair on a given field.
    """

    name_formatter = None
    abstract = True
    kind = 'field'

    def create(self, attr, value, field_name):
        return super().create(attr, value, field_name=field_name)

    def format_name(self, attr, value, field_name):
        return self.name_formatter.format(
            field=field_name, attr=attr, value=value)

    def get_test_kwargs(self, field_name):
        try:
            field = self.model._meta.get_field(field_name)
            return {'field': field}
        except FieldDoesNotExist:
            # look for a property instead
            try:
                prop = getattr(self.model, field_name).fget
                return {'field': prop}
            except AttributeError:
                raise AttributeError(
                    "'{}' object has no field or property '{}'"
                    .format(self.model._meta.object_name, field_name))

    @staticmethod
    def perform_test(attr, value, field):
        raise NotImplementedError


class ModelTestFactory(BaseTestFactory):
    """Model test method factory.

    Use .create(attr, value) to create a test method for a specific
    (attr, value) pair.
    """

    name_formatter = None
    abstract = True
    kind = 'model'

    def create(self, attr, value):
        return super().create(attr, value)

    def format_name(self, attr, value):
        return self.name_formatter.format(attr=attr, value=value)

    def get_test_kwargs(self, **kwargs):
        meta = self.model._meta
        return {'meta': meta}

    @staticmethod
    def perform_test(attr, value, meta):
        raise NotImplementedError


# Register field test methods here

class FieldBoolAttrTestFactory(FieldTestFactory):
    """Test that a field attribute is True or False according to value."""

    name_formatter = 'test_{field}_{attr}_is_{value}'

    def accepts(self, attr, value):
        return isinstance(value, bool)

    @staticmethod
    def perform_test(self, attr, value, field):
        if value is True:
            self.assertTrue(getattr(field, attr))
        else:
            self.assertFalse(getattr(field, attr))


class FieldAttrEqualsTestFactory(FieldTestFactory):
    """Test a field attribute value for equality."""

    name_formatter = 'test_{field}_{attr}_value'

    def accepts(self, attr, value):
        return attr not in ('verbose_name', 'choices')

    @staticmethod
    def perform_test(self, attr, value, field):
        self.assertEqual(getattr(field, attr), value)


class FieldVerboseNameTestFactory(FieldAttrEqualsTestFactory):
    """Test a field verbose name."""

    name_formatter = 'test_{field}_verbose_name'

    def accepts(self, attr, value):
        return attr == 'verbose_name'


class FieldChoicesTestFactory(FieldAttrEqualsTestFactory):
    """Test the choices of a field."""

    name_formatter = 'test_{field}_{attr}_value'

    def accepts(self, attr, value):
        return attr == 'choices'


# Register model test methods here

class ModelBoolAttrTestFactory(ModelTestFactory):
    """Test that a model attribute is True or False according to value."""

    name_formatter = 'test_{attr}_is_{value}'

    def accepts(self, attr, value):
        return isinstance(value, bool)

    @staticmethod
    def perform_test(self, attr, value, meta):
        if value is True:
            self.assertTrue(getattr(meta, attr))
        else:
            self.assertFalse(getattr(meta, attr))


class ModelAttrEqualsTestFactory(ModelTestFactory):
    """Test a model attribute value for equality."""

    name_formatter = 'test_{attr}_value'

    def accepts(self, attr, value):
        return attr not in ('verbose_name',)

    @staticmethod
    def perform_test(self, attr, value, meta):
        self.assertEqual(getattr(meta, attr), value)


class ModelVerboseNameTestFactory(ModelAttrEqualsTestFactory):
    """Test a model verbose name."""

    name_formatter = 'test_verbose_name'

    def accepts(self, attr, value):
        return attr == 'verbose_name'
