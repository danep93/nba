
class CSVDataLoadError(Exception):
    def __init__(self, message="Unable to load csv"):
        self.message = message
        super().__init__(self.message)
