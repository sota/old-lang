
class SotaException(Exception):
    pass

class UnboundVariable(SotaException):
    def __str__(self):
        return 'unbound variable %s' % self.args[0]

class NotCallable(SotaException):
    def __str__(self):
        return '%s is not callable' % self.args[0].to_string()

class WrongArgsNumber(SotaException):
    def __str__(self):
        if len(self.args) == 2:
            return 'wrong number of args:  received %d, expected %s' % (self.args[0], self.args[1])
        else:
            return 'wrong number of args'

class WrongArgType(SotaException):
    def __str__(self):
        return 'wrong arg type: %s is not %s' % (self.args[0].to_string(), self.args[1])

class SyntaxError(SotaException):
    def __str__(self):
        return 'syntax error'

class SotaQuit(SotaException):
    pass
