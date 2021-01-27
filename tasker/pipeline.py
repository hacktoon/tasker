

class PipelineSetupError(Exception):
    pass




class Task:
    def __init__(self, name, function):
        self.name = name
        self.function = function

    def run(self, previous=None):
        value = self.function(previous)
        status = self.is_valid(value)
        if status:
            value = self.process_value(value)
        return TaskResult(self.name, value, status)

    def is_valid(self, value):
        # overwrite this to add custom validation
        return value is not None or bool(value)

    def process_value(self, value):
        # overwrite this to process the value returned by task
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
        self._host_instance = None
        self._basetask = Task
        self._task_queue = []

    def setup(self, basetask=Task):
        self._basetask = basetask

        def decorator(HostClass):
            # create instance of class with tasks
            self._host_instance = HostClass()
        return decorator

    def task(self, name='Unknown', basetask=None):
        TaskClass = basetask or self._basetask

        def decorator(original_method):
            def decorated_method(previous):
                if not self._host_instance:
                    raise PipelineSetupError('No pipeline configured.')
                return original_method(self._host_instance, previous)
            _task = TaskClass(name, decorated_method)
            self._task_queue.append(_task)
            return decorated_method
        return decorator

    def run(self):
        if not self._host_instance:
            raise PipelineSetupError('No pipeline setup.')
        if not len(self._task_queue):
            raise PipelineSetupError('No tasks to run.')

        summary = []
        previous_result = None
        for task in self._task_queue:
            result = task.run(previous_result)
            if result:
                summary.append(result.value)
            previous_result = result
            print(result)
        return summary


