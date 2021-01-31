
import csv

def getCommand(name: str, database: str) -> str:
    """ Get command name and data from csv file
        Parameters
        ----------
        name :
            Name of command to get
        Returns 
        -------
        List with command name and data bytes 
    """
    with open(database, newline='') as file:
            reader = csv.reader(file)
            for row in reader:
                if row[0] == name:
                    return row
