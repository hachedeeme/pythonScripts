import ConfigParser

def printConfigTree(configTree):
    for section, options in configTree.items():
        print section
        for option, value in options.items():
            print '  ->', option, '=', value

def getConfigTree(configFile):
    """
        {
            'section_1' : {
                'option_1' : 'value_1'
            },
            'section_2' : {
                'option_2' : 'value_2'
                'option_3' : 'value_3'
            }
        }
    """

    configParser = ConfigParser.ConfigParser()
    configParser.read(configFile)

    sections = configParser.sections()

    config = {}
    for section in sections:
        config[section] = {}
        options = configParser.options(section)
        for option in options:
            try:
                config[section][option] = configParser.get(section, option)
                if config[section][option] == -1:
                    print "skip:", option
            except:
                print "exception on", option
                config[section][option] = None

    return config

if __name__ == "__main__":
    config = getConfigTree("ibox_paths.cfg")
    printConfigTree(config)