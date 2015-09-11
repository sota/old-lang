
class SastException(Exception):
    pass

class SastUnboundVariable(SastException):
    def __str__(self):
        return "Unbound variable %s" % (self.args[0], )

class SastNotCallable(SastException):
    def __str__(self):
        return "%s is not a callable" % (self.args[0].to_format(), )

class SastWrongArgsNumber(SastException):
    def __str__(self):
        if len(self.args) == 2:
            return ("Wrong number of args. Got: %d, expected: %s" %
                (self.args[0], self.args[1]))
        else:
            return "Wrong number of args."

class SastWrongArgType(SastException):
    def __str__(self):
        return "Wrong argument type: %s is not %s" % \
                (self.args[0].to_format(), self.args[1])

class SastSyntaxError(SastException):
    def __str__(self):
        return "Syntax error"

class SastQuit(SastException):
    """raised on (quit) evaluation"""
    pass
