#!/usr/bin/env python -u

import logging
import my_module

def main():
    logging.basicConfig(filename='example.log',
                        filemode='w',
                        format='%(asctime)s %(levelname)s %(message)s',
                        datefmt='%Y-%m-%d %H:%M:%S',
                        level=logging.INFO)

    logging.info('Started')
    logging.debug('This is a log of level DEBUG.')
    logging.info('This is a log of level INFO.')
    logging.warning('This is a log of level WARNING.')
    logging.warn('This is a log of level WARN.')
    logging.info('%s before %s!', 'Look', 'leap')

    my_module.do_something()
    logging.info('Finished')

if __name__ == '__main__':
    main()
