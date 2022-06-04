class MemoryFile():
    """
    An abstraction for an file kept in memory.

    Attributes
    ----------
    name : str
        the file name
    content : bytes
        the raw content of the file
    dir_path : str
        the path to this file's parent directory
    """

    def __init__(self, name, content, dir_path=''):
        self.name = name
        self.content = content
        self.dir_path = dir_path
