#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''
This file is part of seminar-notifier.
seminar-notifier is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.
seminar-notifier is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.    See the
GNU General Public License for more details.
You should have received a copy of the GNU General Public License
along with seminar-notifier.    If not, see <http://www.gnu.org/licenses/>.
'''

# (c) Simon Reich 2018

######################################################
## No Configuration after this
######################################################



from yaml import load
from bin import seminarnotifier



def main():
    ''' This is the main function of seminar-notifier.

        It creates one class for each seminar, which does all the handling.
    '''
    # read globalconfig.yaml
    with open('./globalconfig.yaml', 'r') as stream:
        config = load(stream)
 
    if not 'sendmail' in config:
        raise ValueError('Could not find sendmail in config file.')
    if not 'seminars' in config:
        raise ValueError('Could not find seminars in config file.')
    configSendmail = config['sendmail']
    configSeminars = config['seminars']

    for seminar in configSeminars:
        seminarnotifier.SeminarNotifier(str(seminar)+'/config', str(seminar)+'/templates', configSendmail)



if __name__ == '__main__':
    # execute only if run as a script
    main()
