import os

class FileWriter:
    """
    A file writing utility class.

    Note that this file could benefit from stronger error handling,
    monitoring, and logging before being deployed in practice. Seeing
    as this is an exercise that presumably will only run a few times, I
    assumed that these features could be omitted.

    Attributes
    ----------
    root_dir : str
        the directory to which all files are to be written

    Methods
    -------
    write(file)
        writes an in-memory file to disk

    write_all(file)
        writes a sequence of in-memory files to disk
    """

    def __init__(self, root_dir):
        """
        Parameters
        ----------
        root_dir : str
            the directory to which all files are to be written
        """

        self.root_dir = root_dir

    def write(self, file):
        """
        Writes an in-memory file to disk.

        Parameters
        ----------
        file: MemoryFile
            The in-memory file to be written
        """

        file_path = '/'.join([self.root_dir, file.dir_path, file.name])
        os.makedirs(os.path.dirname(file_path), exist_ok=True)
        with open(file_path, 'wb') as f:
            f.write(file.content)

    def write_all(self, files):
        """
        Writes a sequence of in-memory files to disk.

        Parameters
        ----------
        files: sequence
            The sequence of in-memory files to be written
        """

        for file in files:
            self.write(file)
