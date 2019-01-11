# GeL2MDT_add_pru v1.0

This script is used to add GeneWorks PRU numbers to cases in GeL2MDT.

It should be run following the import of cases to GeL2MDT, by including it in the GeL2MDT `DAILY_UPDATE.sh` script.

It will add or update PRUs for all probands, using the `local_id` field in the `Proband` table.

## Usage

Requirements:

* Python 3.6
* ODBC driver for MS-SQL server
* Access to GeneWorks and GeL2MDT databases
* Python packages:
    * pyodbc
    * mysqlclient
    * pandas

The above requirements will be met if running on our linux server `SV-TE-GENAPP01` within the `gel2mdt` environment

```
source activate gel2mdt
```

Additionally, credentials for GeL2MDT and GeneWorks databases must be stored in environment variables:
* gel2mdt_db_username
* gel2mdt_db_password
* geneworks_db_username
* geneworks_db_password

Run the script:

```
python GeL2MDT_add_pru.py
```