import argparse


def get_args():
    """Get the command-line arguments"""
    parser = argparse.ArgumentParser(
        description='An app for recursively crawling the links of the domains of a url',
        formatter_class=argparse.ArgumentDefaultsHelpFormatter,
        epilog='******* Developed by Elvis O. Amoako *******')
    parser.add_argument('-u',
                        '--url',
                        help='The domain url to be crawled',
                        metavar='str',
                        type=str,
                        default='https://turntabl.io')
    return parser.parse_args()
