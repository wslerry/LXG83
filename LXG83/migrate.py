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
        sde_connection - sde @ mdb @ gdb file
        out_directory - migrated geodatabase output directory
        geodatabase_name - name of geodatabase
        projection_file - Borneo RSO projection directory. Default
        target_string - LASIS application type string name
        prefix - prefix file name
        check - Geodatabase will be check for sanity
        reference - data migrated will be use to assess replication data

        SDE2GDB(sde_connection, out_directory, geodatabase_name, projection_file, target_string, prefix, reference=False/True)

    Example:
        SDE2GDB()
    """
    def __init__(self, sde_connection, out_directory, gdb_name,
                 projection_file, division, target_string, prefix, reference=False):
        self.sde = sde_connection
        self.out_dir = out_directory
        self.gdb_name = gdb_name
        self.crs = projection_file
        self.division = division
        self.tgt_str = target_string
        self.prefix = prefix
        self.replication = reference

        _, source_ext = os.path.splitext(self.sde)

        if source_ext == '.mdb' or source_ext == '.MDB':
            src_type = "MDB"
        elif source_ext == '.gdb' or source_ext == '.GDB':
            src_type = "GDB"
        else:
            pass

        if src_type == "MDB":
            src = self.sde
            if not gp.Exists(src):
                sys.exit('MDB not exist, system exit...')
        elif src_type == "GDB":
            src = self.sde
            if not gp.Exists(src):
                sys.exit('GDB not exist, system exit...')
        else:
            src = os.path.join(os.environ['USERPROFILE'],
                               'AppData\\Roaming\\ESRI\\ArcCatalog',
                               "Connection to %s.sde" % self.sde)
            if not gp.Exists(src):
                sys.exit('SDE not exist, system exit...')

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

            _, ext = os.path.splitext(output_personal_gdb)

            if ext == '.mdb':
                gp.CreatePersonalGDB_management(self.out_dir, self.gdb_name)
            if ext == '.gdb':
                gp.CreateFileGDB_management(self.out_dir, self.gdb_name)
        except Exception:
            gp.AddError(Exception)

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

        if self.tgt_str == "CMS" and self.replication is False:
            # rename grid layer and upgrade annotation if not use for replication(False) but only for migration
            params = {
                "migrated_gdb": output_personal_gdb,
                "prefix": '',
                "division": self.division,
                "lasis_application": self.tgt_str
            }

            RenameGrids(**params)

            params01 = {
                "migrated_gdb": output_personal_gdb,
                "prefix": '',
                "division": self.division
            }

            UpgradeAnnotation(**params01)
        elif self.tgt_str != "CMS":
            gp.workspace = output_personal_gdb
            datasets = gp93.ListDatasets("", "feature")
            idx = 0
            for ds in datasets:
                for _ in gp93.ListFeatureClasses("", "Annotation", ds):
                    idx += 1
            if idx > 0:
                pbar = progressbar(datasets, prefix='Upgrade Annotation :')
                for ds in pbar:
                    features = gp93.ListFeatureClasses("", "Annotation", ds)
                    for feat in features:
                        gp.UpdateAnnotation_management(feat, "POPULATE")
        else:
            pass

        if self.tgt_str == "CMS" and self.replication is True:
            # Delete annotation if the geodatabase means to use for replication
            params02 = {
                "migrated_gdb": output_personal_gdb,
                "prefix": '',
                "division": self.division
            }

            DeleteAnnotation(**params02)
        else:
            pass


class RenameGrids:
    def __init__(self, migrated_gdb, prefix, division, lasis_application):
        self.gdb = migrated_gdb
        self.prefix = prefix
        self.div = division
        self.app = lasis_application

        prefix = '' if not self.prefix or self.prefix == "" else '%s_' % self.prefix

        gp.workspace = self.gdb
        datasets = gp93.ListDatasets("", "feature")
        pbar = progressbar(datasets, prefix='Rename :')
        for ds in pbar:
            features = gp93.ListFeatureClasses("", "All", ds)
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
                elif featname == '%s%s_Map_Graticles_5K' % (self.prefix, division):
                    gp.rename(featname, '%s%s_Map_Graticules_5K' % (self.prefix, self.div))
                else:
                    pass


class UpgradeAnnotation:
    def __init__(self, migrated_gdb, prefix_string, division):
        self.gdb = migrated_gdb
        self.prefix = prefix_string
        self.div = division

        prefix = '' if not self.prefix or self.prefix == "" else '%s_' % self.prefix

        gp.workspace = self.gdb
        datasets = gp93.ListDatasets("", "feature")
        pbar = progressbar(datasets, prefix='Upgrade Annotation :')
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


class DeleteAnnotation:
    def __init__(self, migrated_gdb, prefix, division):
        self.gdb = migrated_gdb
        self.prefix = prefix
        self.div = division

        gp.workspace = self.gdb
        datasets = gp93.ListDatasets("", "feature")
        pbar = progressbar(datasets, prefix='Upgrade Annotation :')
        for ds in pbar:
            features = gp93.ListFeatureClasses("", "All", ds)
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

                desc = gp93.Describe(featname)
                gp.toolbox = "management"

                if desc.FeatureType == 'Annotation':
                    try:
                        gp.Delete_management(featname)
                    except Exception:
                        gp.GetMessages(2)
                        gp.AddError(Exception)


class MDB2GDB:
    def __init__(self, mdb_filename, out_directory, projection_file,
                 division, target_string, prefix, reference=False):
        self.mdb = mdb_filename
        self.out_dir = out_directory
        self.crs = projection_file
        self.div = division
        self.tgt_str = target_string
        self.prefix = prefix
        self.replication = reference

        filename = os.path.splitext(os.path.basename(self.mdb))[0]
        gdb_name = filename + '.gdb'
        SDE2GDB(self.mdb,
                self.out_dir,
                gdb_name,
                self.crs,
                self.div,
                self.tgt_str,
                self.prefix,
                self.replication)


class GDB2GDB:
    def __init__(self, gdb_filename, out_directory, projection_file,
                 division, target_string, prefix, reference=False):
        self.gdb = gdb_filename
        self.out_dir = out_directory
        self.crs = projection_file
        self.div = division
        self.tgt_str = target_string
        self.prefix = prefix
        self.replication = reference

        filename = os.path.splitext(os.path.basename(self.gdb))[0]
        gdb_name = filename + '.gdb'
        SDE2GDB(self.gdb,
                self.out_dir,
                gdb_name,
                self.crs,
                self.div,
                self.tgt_str,
                self.prefix,
                self.replication)

