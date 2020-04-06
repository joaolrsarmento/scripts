# import plataform

# This code should be useful only if you are using windows
# if plataform.system() == 'Windows':
import win32api
import win32print

class Printer:
    """
    Represents a printer.
    """
    def __init__(self):
        # Get printer name (used as default)

        self.printerName = win32print.GetDefaultPrinter()

    def __print(self, filename: str) -> None:
        """
        Private method that prints the file.
        """
        print('Printing...')
        win32api.ShellExecute (
                                0,
                                "print",
                                filename,
                                #
                                # If this is None, the default printer will
                                # be used anyway.
                                #
                                '/d:"%s"' % self.printerName,
                                ".",
                                0
                                )
        print('Completed.')

    def run(self, filename: str) -> None:
        """
        Method called to run the printer.
        """
        try:
            self.__print(filename)
        except:
            raise '''Unable to print'''

