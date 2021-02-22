class Logger(object):
    IsVerbose = False
    def __init__(self, isVerbose):
        self.IsVerbose = isVerbose

    def log(self, message, log_type):
        """Available log_types:
        "msg", "warn", "error"
        """
        if(self.IsVerbose):
            if(log_type.lower() == 'msg'):
                return f'[MSG] {message}'
            elif(log_type.lower() == 'warn'):
                return f'[WARN] {message}'
            elif(log_type.lower() == 'error'):
                return f'[ERROR!] {message}'
        else:
            return