import yaml
import botocore.session
import boto3


class APIConfig(object):

    def __init__(self, name, region, account_id, role_id):
        self.region = region
        self.account_id = account_id
        self.role_id = role_id
        self.name = name

    @staticmethod
    def parse(config_path):
        with open(config_path, 'r') as stream:
            try:
                cfg = yaml.load(stream)
                return APIConfig(
                    cfg['name'],
                    get_region(cfg),
                    get_account_id(),
                    cfg['role_id']
                )
            except yaml.YAMLError as exc:
                print exc


class WebsiteConfig(object):

    def __init__(self, name, region):
        self.name = name
        self.region = region

    @staticmethod
    def parse(path):
        with open(path, 'r') as stream:
            try:
                cfg = yaml.load(stream)
                region = get_region(cfg)
                return WebsiteConfig(
                    cfg['name'],
                    region
                )
            except yaml.YAMLError as exc:
                print exc


def get_region(cfg):
    if 'region' in cfg:
        return cfg['region']
    else:
        session = botocore.session.get_session()
        return session.get_config_variable('region')


def get_account_id():
    sts = boto3.client('sts')
    response = sts.get_caller_identity()
    return response['Account']
