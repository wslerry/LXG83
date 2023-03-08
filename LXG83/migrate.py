import os
import sys
import re
from .utils import progressbar, is_valid_ip


if os.path.isdir(r"C:\Program Files (x86)\ArcGIS\Bin"):
    sys.path.append(r"C:\Program Files (x86)\ArcGIS\Bin")
else:
    sys.exit("LXG83 requires ArcMAP 9.3 to be installed")

import arcgisscripting
gp = arcgisscripting.create()
gp93 = arcgisscripting.create(9.3)

ROOT = os.path.dirname(os.path.realpath(__file__))

_prj = os.path.join(ROOT, "assets", "projection", "BRSO_4.prj")


def new_name(target_string, old_name):
    return old_name.replace(target_string, "", 1)


class SDE2GDB:
    """
    Migrate SDE Geodatabase from 8i Server to local FileGeodatabase.
    Usage:
        SDE2GDB(sde_connection, out_directory, geodatabase_name, projection_file, target_string, suffix)

    Example:
        SDE2GDB()
    """
    def __init__(self, sde_connection, out_directory, gdb_name,
                 projection_file, division, target_string, prefix, check_database=False):
        self.sde = sde_connection
        self.out_dir = out_directory
        self.gdb_name = gdb_name
        self.crs = projection_file
        self.division = division
        self.tgt_str = target_string
        self.prefix = prefix
        self.check = check_database

        _, source_ext = os.path.splitext(self.sde)

        if source_ext == '.mdb' or source_ext == '.MDB':
            src = self.sde
            if not gp.Exists(src):
                print "MDB not exist, system exit..."
                sys.exit('MDB not exist')
            else:
                pass
        else:
            if is_valid_ip(self.sde) is True:
                pass
            else:
                print "Invalid IP, system exit..."
                sys.exit('Invalid IP')

            src = os.path.join(os.environ['USERPROFILE'],
                               'AppData\\Roaming\\ESRI\\ArcCatalog',
                               "Connection to %s.sde" % self.sde)
            if not gp.Exists(src):
                print "SDE not exist, system exit..."
                sys.exit('SDE not exist')
            else:
                pass

        if not self.division or self.division == "":
            targetstring = "%s" % self.tgt_str
        else:
            targetstring = "%s_%s" % (self.division, self.tgt_str)

        if not self.crs or self.crs == "":
            self.crs = _prj

        if os.path.isdir(self.out_dir):
            pass
        else:
            os.mkdir(self.out_dir)

        output_personal_gdb = os.path.join(self.out_dir, self.gdb_name)

        try:
            if gp.Exists(output_personal_gdb):
                gp.Delete_management(output_personal_gdb)
        except Exception:
            gp.AddError(Exception)

        if not gp.Exists(output_personal_gdb):
            _, ext = os.path.splitext(output_personal_gdb)
            if ext == '.mdb':
                gp.CreatePersonalGDB_management(self.out_dir, self.gdb_name)
            if ext == '.gdb':
                gp.CreateFileGDB_management(self.out_dir, self.gdb_name)

        gp.workspace = src

        datasets = gp93.ListDatasets("*%s*" % targetstring, "feature")
        pbar = progressbar(datasets, prefix='SDE2GDB :')

        if source_ext == '.sde' or source_ext == '.SDE':
            for ds in pbar:
                if re.search(targetstring, ds):
                    if re.search('SDE.', ds):
                        if re.search('SDE.', ds):
                            dsname = '%s%s' % (self.prefix, new_name('SDE.', ds))
                        elif re.search('sde.', ds):
                            dsname = '%s%s' % (self.prefix, new_name('sde.', ds))
                        else:
                            dsname = gp.ValidateTableName(ds, output_personal_gdb)
                            dsname = '%s%s' % (self.prefix, dsname)
                        try:
                            gp.Copy_management(ds, os.path.join(output_personal_gdb, dsname), 'dataset')
                            gp.DefineProjection_management(os.path.join(output_personal_gdb, dsname), self.crs)
                        except Exception:
                            gp.GetMessages(2)
                            gp.AddError(Exception)
        else:
            for ds in pbar:
                if re.search(targetstring, ds):
                    dsname = gp.ValidateTableName(ds, output_personal_gdb)
                    dsname = '%s%s' % (self.prefix, dsname)
                    try:
                        gp.Copy_management(ds, os.path.join(output_personal_gdb, dsname), 'dataset')
                        gp.DefineProjection_management(os.path.join(output_personal_gdb, dsname), self.crs)
                    except Exception:
                        gp.GetMessages(2)
                        gp.AddError(Exception)

        if self.check:
            params = {
                "migrated_gdb": output_personal_gdb,
                "prefix": '' if not self.prefix or self.prefix == "" else '%s_' % self.prefix,
                "division": self.division
            }

            CheckGDB(**params)
        else:
            pass


class CheckGDB:
    def __init__(self, migrated_gdb, prefix, division):
        self.gdb = migrated_gdb
        self.prefix = prefix
        self.div = division

        gp.workspace = self.gdb
        datasets = gp93.ListDatasets("", "feature")
        pbar = progressbar(datasets, prefix='Check GDB :')
        for ds in pbar:
            features = gp93.ListFeatureClasses("", "All", ds)
            idx = 0
            for feat in features:
                if re.search('SDE.', feat):
                    featname = '%s%s' % (prefix, new_name('SDE.', feat))
                elif re.search('sde.', feat):
                    featname = '%s%s' % (prefix, new_name('sde.', feat))
                else:
                    featname = gp.ValidateTableName(feat, self.gdb)
                    featname = '%s%s' % (prefix, featname)

                if feat != featname:
                    try:
                        gp.rename(feat, featname)
                    except Exception:
                        gp.GetMessages(2)
                        gp.AddError(Exception)

                # this part will rename 'graticles' to 'graticules' featureClass
                if featname == '%s%s_Map_Graticles_1K' % (self.prefix, division):
                    gp.rename(featname, '%s%s_Map_Graticules_1K' % (self.prefix, self.div))
                    featname = '%s%s_Map_Graticules_1K' % (self.prefix, self.div)
                elif featname == '%s%s_Map_Graticles_5K' % (self.prefix, division):
                    gp.rename(featname, '%s%s_Map_Graticules_5K' % (self.prefix, self.div))
                    featname = '%s%s_Map_Graticules_5K' % (self.prefix, self.div)
                else:
                    pass

                desc = gp93.Describe(featname)
                gp.toolbox = "management"

                if desc.FeatureType == 'Annotation':
                    idx += 1
                    # Create a table view and select records to be deleted
                    gp.maketableview(featname, "%s_temp_tab_%s" % (ds, idx))
                    query = '"SHAPE_Area" = 0'
                    gp.SelectLayerByAttribute("%s_temp_tab_%s" % (ds, idx), "NEW_SELECTION", query)

                    # Delete selected records
                    gp.deleterows("%s_temp_tab_%s" % (ds, idx))

                    try:
                        gp.UpdateAnnotation_management(featname, "POPULATE")
                    except Exception:
                        gp.GetMessages(2)
                        gp.AddError(Exception)


class MDB2GDB:
    def __init__(self, mdb_filename, out_directory, projection_file,
                 division, target_string, prefix, check_database=False):
        self.mdb = mdb_filename
        self.out_dir = out_directory
        self.crs = projection_file
        self.div = division
        self.tgt_str = target_string
        self.prefix = prefix
        self.check = check_database

        filename = os.path.splitext(os.path.basename(self.mdb))[0]
        gdb_name = filename + '.gdb'
        SDE2GDB(self.mdb,
                self.out_dir,
                gdb_name,
                self.crs,
                self.div,
                self.tgt_str,
                self.prefix,
                self.check)

