import yaml


def make_resolver_helpers():
    global MyLoader, MyDumper

    class MyLoader(yaml.Loader):
        pass
    class MyDumper(yaml.Dumper):
        pass

    yaml.add_path_resolver('!root', [],
            Loader=MyLoader, Dumper=MyDumper)
    yaml.add_path_resolver('!root/scalar', [], str,
            Loader=MyLoader, Dumper=MyDumper)
    yaml.add_path_resolver('!root/key11/key12/*', ['key11', 'key12'],
            Loader=MyLoader, Dumper=MyDumper)
    yaml.add_path_resolver('!root/key21/1/*', ['key21', 1],
            Loader=MyLoader, Dumper=MyDumper)
    yaml.add_path_resolver('!root/key31/*/*/key14/map', ['key31', None, None, 'key14'], dict,
            Loader=MyLoader, Dumper=MyDumper)
