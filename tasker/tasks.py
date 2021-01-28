
class Task:
    def __init__(self, name, function):
        self.name = name
        self.function = function

    def run(self, host_self, prev_result=None):
        base_value = prev_result.value if prev_result else None
        # self.function is an unbound method so it needs a `self`
        value = self.function(host_self, self.before(base_value))
        status = self.validate(value)
        if status:
            value = self.after(value)
        return TaskResult(self.name, value, status)

    def validate(self, value):
        # overwrite this to add custom validation
        return value is not None or bool(value)

    def after(self, value):
        # overwrite this to process the value returned by task
        return value

    def before(self, value):
        # overwrite this to pre-process the task value
        return value

    def __str__(self):
        return f'Task name="{self.name}"'


class TaskResult:
    def __init__(self, name, value, status):
        self.name = name
        self.value = value
        self.status = status

    def __bool__(self):
        return bool(self.status)

    def __str__(self):
        status = 'OK' if self else 'FAILED'
        return f'[{status}] task="{self.name}", value="{self.value}"'
