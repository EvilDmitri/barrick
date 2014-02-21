#!/usr/bin/python
# -*- coding: utf-8 -*-

import argparse


def main():
    parser = argparse.ArgumentParser()

    parser.add_argument("-u", type=str,
                        help="Url to scrape")

    parser.add_argument("-l", type=str,
                        help="Login for site")

    parser.add_argument("-p", type=str,
                        help="Password for site")

    parser.add_argument("--page", type=int, default=1,
                        help="Number of the pages to be scraped")

    parser.add_argument("--post-params", type=str,
                        help="Post parameters, url encoded")

    parser.add_argument("-f", type=str,
                        help="File to store the parsed data")

    args = parser.parse_args()

    from modules.site_grabber import barrick_grabber

    barrick_grabber(url=args.u, params=args.post_params, file_name=args.f, pages=args.page)


if __name__ == '__main__':
    main()