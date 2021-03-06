# -*- coding: utf-8 -*-
import argparse
import logging
import sys
import os
import datetime
import tweepy
sys.path.append(os.path.dirname(os.path.abspath(__file__)) + "utils")
from utils.file_manager import FileManager

log_handler = logging.StreamHandler(sys.stdout)
log_handler.setFormatter(logging.Formatter('[%(asctime)s][%(levelname)s] %(message)s'))
logger = logging.getLogger(__name__)
logger.addHandler(log_handler)

def record(args):
    file_manager = FileManager()
    config_dict = file_manager.get_json_dict_from_json(os.path.join(os.path.dirname(os.path.abspath(__file__)), "config.json"))
    logger.debug(config_dict)

    auth = tweepy.OAuthHandler(config_dict["twitter_api"]["consumer_key"], config_dict["twitter_api"]["consumer_secret"])
    auth.set_access_token(config_dict["twitter_api"]["access_token"], config_dict["twitter_api"]["access_token_secret"])
    twitter_api = tweepy.API(auth)

    for screen_name in args.target_screen_name:
        try:
            logger.info("Processing \"%s\" ..." % screen_name)
            user_dict = twitter_api.get_user(screen_name=screen_name)
            #logger.debug(user_dict._json)
            datetime_str = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            followers_count = str(user_dict._json["followers_count"])
            friends_count = str(user_dict._json["friends_count"])
            directory_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "results")
            file_manager.update_csv_file(directory_path, screen_name, datetime_str, friends_count, followers_count)
        except Exception as e:
            logger.error("screen_name: %s, log: %s" % (screen_name, e))

if __name__ == "__main__":
    arg_parser = argparse.ArgumentParser()
    arg_parser.add_argument("command", help="the command you want to run")
    arg_parser.add_argument("target_screen_name", nargs="*", help="screen name of the target name")
    arg_parser.add_argument("-q", "--quiet", required=False, action="store_true", help="do not output log")
    args = arg_parser.parse_args()

    # set logging configuration
    logging_level = logging.INFO
    if args.quiet == True:
        logging_level = logging.CRITICAL
    logger.setLevel(logging_level)

    if args.command == "record":
        record(args)
    else:
        logger.critical("%s is invalid command!!" % args.command)
        sys.exit(1)

