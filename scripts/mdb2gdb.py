from LXG83 import MDB2GDB
import sys
sys.path.append(r"C:\Program Files (x86)\ArcGIS\Bin")
import arcgisscripting

gp = arcgisscripting.create()

if __name__ == "__main__":
    mdb_filename = gp.GetParameterAsText(0)
    out_directory = gp.GetParameterAsText(1)
    division = gp.GetParameterAsText(2)
    target_string = gp.GetParameterAsText(3)

    MDB2GDB(mdb_filename=mdb_filename,
            out_directory=out_directory,
            projection_file="",
            division=division,
            target_string=target_string,
            prefix="",
            check_database=False)
