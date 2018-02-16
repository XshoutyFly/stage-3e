import pip
required = ['docopt', 'ciscosparkapi', 'jinja2', 'requests', 'flask', 'psutil']
for require in required:
    pip.main(['install', require])
pip.main(['install', 'git+https://cto-github.cisco.com/gladhuie/ngork.git'])