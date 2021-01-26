
class Task:
    def __init__(self, name, function):
        self.name = name
        self.function = function

    def run(self):
        print(f'Ran {self.name}')

    def __str__(self):
        return f'task="{self.name}"'


class Tasker:
    def __init__(self):
        self._tasks = []

    def task(self, name='anonym', base=Task):
        def wrapped(original_method):
            def decorated_task(method_self):
                return original_method(method_self)
            _task = base(name, decorated_task)
            self._tasks.append(_task)
            return decorated_task
        return wrapped

    def run(self):
        for task in self._tasks:
            result = task.run()
            # if not result.valid:
            #     return result


