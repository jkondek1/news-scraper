import argparse


def init_parser():
    parser = argparse.ArgumentParser()
    parser.add_argument('--app_host', type=str, default='0.0.0.0')
    parser.add_argument('--app_port', type=int, default=8080)
    parser.add_argument('--app_workers', type=int, default=1)
    parser.add_argument('--db_host', type=str, default='localhost')
    parser.add_argument('--db_port', type=int, default=5432)
    parser.add_argument('--db_user', type=str, default='postgres')
    parser.add_argument('--db_password', type=str, default='postgres')
    parser.add_argument('--db_name', type=str, default='news')
    return parser
