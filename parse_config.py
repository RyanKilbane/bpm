import yaml

with open("config.yml", "r") as yml_config:
    config = yaml.safe_load(yml_config)