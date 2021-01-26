

class PipelineSetupError(Exception):
    pass




class Task:
    def __init__(self, name, function, params={}):
        self.name = name
        self.function = function

    def run(self):
        status = True
        try:
            value = self.function()
            status = self.is_valid(value)
        except Exception as err:
            status = False
            value = str(err)
        parsed_value = self.process_value(value)
        return TaskResult(self.name, parsed_value, status)

    def is_valid(self, value):
        return value is not None or bool(value)

    def process_value(self, value):
        return value

    def __str__(self):
        return f'[TASK] "{self.name}"'


class TaskResult:
    def __init__(self, name, value, status):
        self.name = name
        self.value = value
        self.status = status

    def __bool__(self):
        return self.status

    def __str__(self):
        status = 'OK' if self.status else 'FAILED'
        return f'[{status}] task="{self.name}", value="{self.value}"'


class Pipeline:
    def __init__(self):
        self._worker_obj = None
        self._basetask = Task
        self._task_queue = []

    def setup(self, basetask=Task):
        self._basetask = basetask

        def decorator(worker_cls):
            # create instance of class with tasks
            self._worker_obj = worker_cls()
        return decorator

    def task(self, name='Unknown', basetask=None):
        TaskClass = basetask or self._basetask

        def decorator(original_method):
            def decorated_method():
                if not self._worker_obj:
                    raise PipelineSetupError('No pipeline configured.')
                return original_method(self._worker_obj)
            _task = TaskClass(name, decorated_method)
            self._task_queue.append(_task)
            return decorated_method
        return decorator

    def run(self):
        if not self._worker_obj:
            raise PipelineSetupError('No pipeline configured.')
        if not len(self._task_queue):
            raise PipelineSetupError('No tasks to run.')

        for task in self._task_queue:
            result = task.run()
            print(result)
            # if not result:
            #     return result


