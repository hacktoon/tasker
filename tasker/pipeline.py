import inspect
from .tasks import Task


def task(name='Unknown', model=None):
    def decorator(original_method):
        original_method.task_name = name
        original_method.task_model = model
        return original_method
    return decorator


def pipeline(model=Task):
    TaskModel = model

    def decorator(UserPipelineClass):
        # UserPipelineClass : Actual pipeline class which implements
        # the `run` method and inherits from user defined class
        class Pipeline(UserPipelineClass):
            def run(self):
                passed = []
                failed = []
                previous_result = None
                for task in _build_tasks(UserPipelineClass, TaskModel):
                    result = task.run(self, previous_result)
                    if result:
                        passed.append(result)
                    else:
                        failed.append(result)
                        break
                    previous_result = result
                return PipelineResult(passed, failed)
        return Pipeline

    return decorator


def _build_tasks(UserPipelineClass, TaskModel):
    methods = _get_methods(UserPipelineClass)
    for name, function in methods:
        if not hasattr(function, 'task_name'): continue
        _TaskModel = getattr(function, 'task_model') or TaskModel
        yield _TaskModel(name, function)


def _get_methods(cls) -> list:
    return inspect.getmembers(cls, predicate=inspect.isfunction)


class PipelineResult:
    def __init__(self, passed, failed):
        self._passed = passed
        self._failed = failed

    def __bool__(self):
        one_or_more_valid = len(self._passed) > 0
        zero_failed = len(self._failed) == 0
        return one_or_more_valid and zero_failed

    def __getitem__(self, index):
        return self._passed[index]

    def __len__(self):
        return len(self._passed)

    def values(self):
        return [result.value for result in self._passed]

    def failed(self):
        return self._failed
