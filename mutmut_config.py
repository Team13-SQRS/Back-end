def pre_mutation(context):
    if context.filename.endswith('test_'):
        return False
    if context.filename.endswith('__init__.py'):
        return False
    if context.filename.endswith('conftest.py'):
        return False
    return True


def post_mutation(context):
    if context.filename.endswith('test_'):
        return False
    if context.filename.endswith('__init__.py'):
        return False
    if context.filename.endswith('conftest.py'):
        return False
    return True
