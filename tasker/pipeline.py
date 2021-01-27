from .tasks import Task


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
        # TODO: this breaks if a task fails; add more runtypes
        if not self._host_instance:
            raise PipelineSetupError('No pipeline setup.')
        if not len(self._task_queue):
            raise PipelineSetupError('No tasks to run.')

        results = []
        failed_results = []
        previous_result = None
        for task in self._task_queue:
            result = task.run(previous_result)
            if result:
                results.append(result)
            else:
                failed_results.append(result)
                break
            previous_result = result
        return PipelineResult(results, failed_results)


class PipelineResult:
    def __init__(self, results, failed_results):
        self._results = results
        self._failed_results = failed_results

    def __bool__(self):
        return len(self._failed_results) == 0

    def __getitem__(self, index):
        return self._results[index]

    def __len__(self):
        return len(self._results)

    def values(self):
        return [result.value for result in self._results]

    def failed(self):
        return [result.value for result in self._failed_results]


class PipelineSetupError(Exception):
    pass