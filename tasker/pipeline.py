from .tasks import Task


class PipelineSetupError(Exception):
    pass


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


