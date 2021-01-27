from .tasks import Task


class Pipeline:
    def __init__(self, *args, **kwargs):
        self._host_instance = None
        self._host_params = (args, kwargs)
        self._basetask = Task
        self._task_queue = []

    def setup(self, basetask=Task):
        self._basetask = basetask

        def decorator(HostClass):
            # create instance of class with tasks
            args, kwargs = self._host_params
            self._host_instance = HostClass(*args, **kwargs)
        return decorator

    def task(self, name='Unknown', basetask=None):
        TaskClass = basetask or self._basetask

        def decorator(host_method):
            def decorated_method(prev_result):
                if not self._host_instance:
                    raise PipelineSetupError('No pipeline configured.')
                return host_method(self._host_instance, prev_result)
            _task = TaskClass(name, decorated_method)
            self._task_queue.append(_task)
            return decorated_method
        return decorator

    def run(self):
        # TODO: this breaks if a task fails; add more runtypes
        if not self._host_instance:
            raise PipelineSetupError('No pipeline setup.')
        if not len(self._task_queue):
            raise PipelineSetupError('No tasks to run.')

        successful = []
        failed = []
        previous_result = None
        for task in self._task_queue:
            result = task.run(previous_result)
            if result:
                successful.append(result)
            else:
                failed.append(result)
                break
            previous_result = result
        return PipelineResult(successful, failed)


class PipelineResult:
    def __init__(self, successful, failed):
        self._successful = successful
        self._failed = failed

    def __bool__(self):
        one_or_more_valid = len(self._successful) > 0
        zero_failed = len(self._failed) == 0
        return one_or_more_valid and zero_failed

    def __getitem__(self, index):
        return self._successful[index]

    def __len__(self):
        return len(self._successful)

    def values(self):
        return [result.value for result in self._successful]

    def failed(self):
        return self._failed


class PipelineSetupError(Exception):
    pass