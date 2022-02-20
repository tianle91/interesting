import configparser

from praw import Reddit


def get_reddit(path: str = 'praw.ini', site: str = 'chennngiskhan') -> Reddit:
    with open(path) as f:
        config = configparser.ConfigParser()
        config.read_string(f.read())
        return Reddit(**config[site])
