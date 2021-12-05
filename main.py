import argparse

import result_collector


def get_args():
    """Get command-line arguments"""

    parser = argparse.ArgumentParser(
        description='WRAC running and tri results collector',
        formatter_class=argparse.ArgumentDefaultsHelpFormatter)

    parser.add_argument('weeks',
                        type=int,
                        default=1,
                        help='Number of weeks to collect')

    parser.add_argument('-t',
                        '--test',
                        help="Create the test pages",
                        action='store_true')

    parser.add_argument('-m',
                        '--mail',
                        help="Mail the results out",
                        action='store_true')

    return parser.parse_args()


if __name__ == '__main__':
    args = get_args()
    test = args.test
    mail = args.mail
    weeks = args.weeks
    result_collector.find_results(test, mail, weeks)
