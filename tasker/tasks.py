
class Task:
    def __init__(self, name, host_method):
        self.name = name
        self.host_method = host_method

    def run(self, prev_result=None):
        value = self.host_method(prev_result)
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
