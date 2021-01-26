
class Task:
    def __init__(self, name='anonym', func=lambda:None):
        self.name = name
        self.func = func

    def run(self):
        pass

    def __str__(self):
        return f'task="{self.name}"'


class Tasker:
    def __init__(self):
        self._tasks = []

    def task(self, name='', base=Task):
        def wrapped(original_method):
            def decorated_task(method_self, *args, **kwargs):
                return original_method(method_self, *args, **kwargs)
            _task = base(name, decorated_task)
            self._tasks.append(_task)
            return decorated_task
        return wrapped

    def run(self):
        for task in self._tasks:
            print(task)
            # result = task.run()
            # if not result.valid:
            #     return result


