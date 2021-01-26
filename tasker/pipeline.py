

class NoSetupError(Exception):
    pass


class Task:
    def __init__(self, name, function, params={}):
        self.name = name
        self.function = function

    def run(self):
        result = self.function()
        print(f'OK task={self.name}, result={result}')

    def __str__(self):
        return f'task="{self.name}"'


class NullPipelineSetup:
    def __getattr__(self):
        raise NoSetupError('No setup class given.')


class Pipeline:
    def __init__(self):
        self._setup_cls = NullPipelineSetup
        self._task_type = Task
        self._task_queue = []

    def setup(self, type=Task):
        def decorator(cls):
            self._setup_cls = cls()
        return decorator

    def task(self, name='unknown', type=None):
        TaskType = type or self._task_type

        def decorator(original_method):
            def decorated_method():
                return original_method(self._setup_cls)
            _task = TaskType(name, decorated_method)
            self._task_queue.append(_task)
            return decorated_method
        return decorator

    def run(self):
        for task in self._task_queue:
            result = task.run()
            # if not result.valid:
            #     return result


