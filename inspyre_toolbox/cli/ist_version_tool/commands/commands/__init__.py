import importlib
import pkgutil

# Get the current package
package_name = __name__

# Dynamically import all modules in the package
for _, module_name, _ in pkgutil.iter_modules(__path__, package_name + "."):
    module = importlib.import_module(module_name)
