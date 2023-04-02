from dummy_api_plugin import DummyApiPlugin


def main():
    plugin = DummyApiPlugin("configurationFile.json")
    plugin.run()


if __name__ == '__main__':
    main()
    