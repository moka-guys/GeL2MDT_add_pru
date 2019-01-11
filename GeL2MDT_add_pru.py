"""
v1.0 - AB 2019/01/11
Requirements:
    Credentials for Geneworks and gel2mdt database must be set as following environment variables:
        gel2mdt_db_username
        gel2mdt_db_password
        geneworks_db_username
        geneworks_db_password

usage: python GeL2MDT_add_pru.py

Adds PRU from GeneWorks into the local_id field for probands in GeL2MDT.
Should be run following GeL2MDT case imports. 
"""

import MySQLdb
import pyodbc
import pandas
import os

class GeL2MDT_PRU_Adder(object):
    """
    Manages the insertion of PRU identifiers from Geneworks into GeL2MDT
    """
    def __init__(self):
        self.prus_probands = None
            
    def get_prus(self):
        """
        Get PRUs from GeneWorks
        """
        print("Retrieving PRUs from GeneWorks")
        gw_cnxn = pyodbc.connect(f'DRIVER={{ODBC Driver 13 for SQL Server}}; SERVER=10.188.194.121; DATABASE=geneworks; UID={os.environ["geneworks_db_username"]}; PWD={os.environ["geneworks_db_password"]}')
        # Pull out 'PatientTrustID' (aka PRU) and 'Participant Id' for all GeL participants from Geneworks
        gw_query_results = pandas.read_sql('EXEC SelectRegister_GMCParticipants_RegisterEntryDetails', gw_cnxn)[['PatientTrustID', 'Participant Id']]
        # Convert dataframe to a list of tuples [(pru1, participant_id1), ...(pruN, participant_idN)]
        self.prus_probands = list(gw_query_results.itertuples(index=False, name=None))

    def update_db(self):
        """
        Adds PRUs into GeL2MDT
        """
        print("Updating PRUs in GeL2MDT")
        # Connect to gel2mdt
        gel2mdt_cnxn = MySQLdb.connect(user=os.environ["gel2mdt_db_username"], passwd=os.environ["gel2mdt_db_password"], db="gel2mdt_db")
        cursor = gel2mdt_cnxn.cursor()
        # Create update queries for the transaction (executemany() will substitute in the data from the list of tuples supplied)
        sql = "UPDATE Proband SET local_id = %s WHERE gel_id = %s"      
        cursor.executemany(sql, self.prus_probands)
        # Commit the transaction
        gel2mdt_cnxn.commit()

def main():
    pru_adder = GeL2MDT_PRU_Adder()
    pru_adder.get_prus()
    pru_adder.update_db()

if __name__ == '__main__':
    main()

