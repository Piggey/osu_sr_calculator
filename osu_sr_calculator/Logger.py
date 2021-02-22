from warnings import warn

class Logger:
    IsVerbose = False
    File = None

    def __init__(self, isVerbose, _file):
        self.IsVerbose = isVerbose
        self.File = _file

    def log(self, message, log_type):
        """Available log_types:
        "msg", "warn", "error"
        """
        # will log warnings and errors despite of verbosity
        if(log_type.lower() == 'warn'):
            warn(f'[WARN] [{self.File}] {message}', Warning)
        
        if(log_type.lower() == 'error'):
            # dont really know if it should throw an exception but oh well
            raise Exception(f'[ERROR] [{self.File}] {message}')

        if(log_type.lower() == 'msg' and self.IsVerbose):
            print(f'[MSG] [{self.File}] {message}')