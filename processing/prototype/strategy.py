
'''
License: "NASA Open Source Agreement 1.3"

Description:
    Implements classes which can be combined into strategy design patterns.
'''


from cerberus import Validator
from PropertyDictionary.collection import PropertyDict


class Task(object):
    '''Provides a consistent api for executing a task'''

    task_schema = None
    validator = None

    def __init__(self, options):
        super(Task, self).__init__()

        print 'Initializing', self.__class__.__name__

        if not self.task_schema:
            self.task_schema = None

        if not self.validator:
            self.validator = Validator()

        self.options = None

        if options is not None:
            self.options = PropertyDict(options)
            self.validate()

    def validate(self):
        '''Validate the provided options'''
        if self.task_schema is not None:
            self.validator.validate(dict(self.options), self.task_schema)

            print 'Validating', self.__class__.__name__
            if self.validator.errors:
                raise ESPAValidationError(self.validator.errors)

    def execute(self):
        '''Execute or implement the specific task'''
        c_name = self.__class__.__name__
        f_name = 'execute'
        msg = 'You must implement [{0}.{1}] method'.format(c_name, f_name)
        raise NotImplementedError(msg)


class TaskChain(Task):
    '''Provides a consistent api for executing sequential list of tasks'''

    def __init__(self, options):
        super(TaskChain, self).__init__(options)

        self.tasks = list()

    def add(self, task):
        '''Adds a task to the task list'''
        self.tasks.append(task)

    def execute(self):
        '''Execute each task in the order recieved'''
        output = PropertyDict()
        for task in self.tasks:
            output.update(task.execute())

        return output


