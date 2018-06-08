

class SequenceTooShortException(Exception):
    def __init__(self, series, depth):
        self._series = series
        self._depth = depth

        message = 'Sequence beginning with {} is too short to compute a cumulative runtime to depth {}'.format(series[:7], depth)
        # Call the base class constructor with the parameters it needs
        super().__init__(message)
