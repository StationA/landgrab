from objectpath import Tree

from landgrab.transform import BaseTask


def _maybe_insert_nested(d, k, v):
    if '.' in k:
        sub_dict_k, k = k.split('.', 1)
        if sub_dict_k not in d:
            d[sub_dict_k] = {}
        sub_d = d[sub_dict_k]
        _maybe_insert_nested(sub_d, k, v)
    else:
        d[k] = v


class ProjectTask(BaseTask):
    def __init__(self, schema):
        self.schema = schema

    def __call__(self, item):
        output = {}
        t = Tree(item)
        for k, expression in self.schema.items():
            _maybe_insert_nested(output, k, t.execute(expression))
        return output


class ExtractTask(BaseTask):
    def __init__(self, expression):
        self.expression = expression

    def __call__(self, item):
        t = Tree(item)
        return t.execute(self.expression)


class RenameKeyTask(BaseTask):
    def __init__(self, key, new_key):
        self.key = key
        self.new_key = new_key

    def __call__(self, item):
        item[self.new_key] = item[self.key]
        del item[self.key]
        return item
