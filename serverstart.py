from src import application
import argparse
import os
import configparser
import shutil
from src.core.data import DataConfig
from src.data.sqlite import UserDataStrategy, ReplyDataStrategy

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--debug", action="store_true")
    args = parser.parse_args()
    DataConfig.UserDataStrategy = UserDataStrategy
    DataConfig.ReplyDataStrategy = ReplyDataStrategy
    if args.debug:
        application.run(host='0.0.0.0', port=5000, debug=True)
    else:
        application.run(host='0.0.0.0', port=5000, debug=False)

