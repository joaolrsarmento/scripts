import sys, os

class PrinterLinux:
    """
    Represents a printer.
    """
    def __init__(self):
        # Get printer name (used as default)

        self.printerName = 'Bematech MP 2100'

    def __print(self, filename: str) -> None:
        """
        Private method that prints the file.
        """
        print('Printing...')
        os.system(f'lpr -P {self.printerName} {filename}')
        print('Completed.')

    def run(self, filename: str) -> None:
        """
        Method called to run the printer.
        """
        try:
            self.__print(filename)
        except:
            raise '''Unable to print'''

