from src import application
import argparse
import os
import configparser
import shutil

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--debug", action="store_true")
    args = parser.parse_args()
    if args.debug:
        application.run(host='0.0.0.0', port=5000, debug=True)
    else:
        application.run(host='0.0.0.0', port=5000, debug=False)

