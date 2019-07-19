import yaml
import os

directory = os.path.dirname(os.path.realpath(__file__))
print(directory)
with open(os.path.join(directory, "config.yml"), "r") as yml_config:
    config = yaml.safe_load(yml_config)