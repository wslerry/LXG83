import sys
from LXG83 import SDE2GDB
sys.path.append(r"C:\Program Files (x86)\ArcGIS\Bin")
import arcgisscripting

gp = arcgisscripting.create()

if __name__ == "__main__":
    sde_connection = gp.GetParameterAsText(0)
    out_directory = gp.GetParameterAsText(1)
    gdb_name = gp.GetParameterAsText(2)
    division = gp.GetParameterAsText(3)
    lasis_type = gp.GetParameterAsText(4)

    SDE2GDB(sde_connection=sde_connection,
            out_directory=out_directory,
            gdb_name=gdb_name,
            projection_file="",
            division=division,
            target_string=lasis_type,
            prefix="",
            reference=True
            )
