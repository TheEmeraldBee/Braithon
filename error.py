class Error:
    def __init__(self, code, message):
        self.code = code
        self.message = message

    def __repr__(self):
        return f"Code: {self.code}, Message: {self.message}"


class Result:
    def __init__(self):
        self.ok = True
        self.ok_value = None
        self.break_amount = 0
        self.err: Error = Error(0, "")

    def with_value(self, value):
        self.ok_value = value
        return self

    def with_error(self, err: Error):
        self.err = err
        self.ok = False
        return self

    def with_exit(self):
        self.break_amount = 10000
        return self

    def with_break(self, amount: int):
        self.break_amount = amount
        return self

    def is_ok(self):
        self.break_amount -= 1
        return self.ok or self.break_amount >= 0

    def unwrap(self):
        if not self.is_ok():
            raise Exception("ERROR: Tried to unwrap error value")
        return self.ok_value

    def unwrap_or(self, default):
        if self.is_ok():
            return self.ok_value
        else:
            return default

    def __repr__(self):
        if self.is_ok():
            return f"Ok Value with inner {self.ok_value}"
        elif self.err == None:
            return ""
        else:
            return f"Error {self.err}"
