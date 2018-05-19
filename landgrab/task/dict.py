from objectpath import Tree

from landgrab.task import BaseTask


def _maybe_insert_nested(d, k, v):
    """
    Tries to insert a value into a dictionary at a nested key using dot notation, e.g. "a.b" would
    refer to the key "b" inside of the dictionary at key "a" inside of a dictionary
    """
    if '.' in k:
        sub_dict_k, k = k.split('.', 1)
        if sub_dict_k not in d:
            d[sub_dict_k] = {}
        sub_d = d[sub_dict_k]
        _maybe_insert_nested(sub_d, k, v)
    else:
        d[k] = v


class JoinTask(BaseTask):
    """
    Joins string components (nested keys or arbitrary strings) using a delimiter,
    creates a new string, then nests the new string in a new key defined by the provided
    ObjectPath expression
    - type: join
      schema:
        newkey:
          delimiter: ', '
          components:
            - $.properties.key1
            - $.properties.key2
            - 'arbitrary string'
    """
    def __init__(self, schema):
        self.schema = schema

    def __call__(self, item):
        t = Tree(item)
        for new_key, params in self.schema.items():
            values_to_join = []
            for component in params['components']:
                if component.startswith('$'):
                    component = t.execute(component)
                if component:
                    values_to_join.append(str(component))
            new_value = params['delimiter'].join(values_to_join)
            _maybe_insert_nested(item, new_key, new_value)
        return item


class ProjectTask(BaseTask):
    """
    Projects an input dictionary into a new dictionary; similar to a SQL-like SELECT statement. The
    schema should be specified as a dictionary where the key is the output key and the value is an
    ObjectPath expression that refers to the input key, e.g.:

    - type: project
      schema:
        newkey: $.properties.oldkey

    """
    def __init__(self, schema):
        self.schema = schema

    def __call__(self, item):
        output = {}
        t = Tree(item)
        for k, expression in self.schema.items():
            _maybe_insert_nested(output, k, t.execute(expression))
        return output


class ExtractTask(BaseTask):
    """
    Extracts a single value from the input dictionary, as specified by the provided ObjectPath
    expression, e.g.:

    - type: extract
      expression: $.properties.geometry

    Note that the resulting value becomes the output item that is processed by any subsequent tasks
    """
    def __init__(self, expression):
        self.expression = expression

    def __call__(self, item):
        t = Tree(item)
        return t.execute(self.expression)


class RenameKeyTask(BaseTask):
    """
    Renames a set of keys to a set of new keys, as specified by the `map` property, e.g.:

    - type: rename
      map:
        oldkey: newkey
        oldkey2: newkey2
    """
    def __init__(self, map):
        self.map = map

    def __call__(self, item):
        for old_key, new_key in self.map.items():
            item[new_key] = item[old_key]
            del item[old_key]
        return item


class FilterTask(BaseTask):
    """
    Filters the input dictionaries based on the value (or values) of a specific key as specified by
    the provided ObjectPath expression; similar to a SQL-like WHERE statement, e.g.:

    - type: filter
      expression: $.properties.fclass
      value: building
    """

    def __init__(self, expression, value):
        self.expression = expression
        self.value = value

    def __call__(self, item):
        t = Tree(item)
        v = t.execute(self.expression)
        if type(self.value) == list:
            if v in self.value:
                return item
            else:
                return None
        else:
            if v == self.value:
                return item
            else:
                return None
