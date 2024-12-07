import pkg_resources


def load_plugins():
    plugins = {}
    for entry_point in pkg_resources.iter_entry_points('inspyre_toolbox.plugins'):
        plugin = entry_point.load()
        plugins[entry_point.name] = plugin
    return plugins


def main():
    plugins = load_plugins()
    print("Available plugins:", plugins)
