import os
import imp
import glob
import sysconfig
import sys

base_module_name = os.path.splitext(os.path.basename(__file__))[0]

base_module_ext = sysconfig.get_config_var("EXT_SUFFIX")
if sysconfig.get_python_version() <= "2.7":
    import distutils.sysconfig
    base_module_ext = distutils.sysconfig.get_config_var("SO")

file_pattern = os.path.abspath(os.path.join(os.environ["PSUTIL_PLATFORM_PATH"], "*{mod}{ext}".format(mod=base_module_name, ext=base_module_ext)))

try:
    file_path = glob.glob(file_pattern)[0]
    module_name = os.path.basename(file_path).split(base_module_ext)[0]
except:
    raise ImportError("Couldn't find psutil platform module in '%s'" % os.environ["PSUTIL_PLATFORM_PATH"])

if sys.version_info.major > 2:
    import importlib.machinery
    import importlib.util

    spec = importlib.util.spec_from_file_location(module_name, file_path)
    mod = importlib.util.module_from_spec(spec)
    locals().update(mod.__dict__)

else:
    import imp
    mod = imp.load_dynamic(module_name, file_path)
    locals().update(mod.__dict__)
