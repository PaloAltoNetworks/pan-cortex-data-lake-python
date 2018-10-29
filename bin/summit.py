#!/usr/bin/env python

#
# Copyright (c) 2018 Palo Alto Networks, Inc. <techbizdev@paloaltonetworks.com>
#
# Permission to use, copy, modify, and distribute this software for any
# purpose with or without fee is hereby granted, provided that the above
# copyright notice and this permission notice appear in all copies.
#
# THE SOFTWARE IS PROVIDED "AS IS" AND THE AUTHOR DISCLAIMS ALL WARRANTIES
# WITH REGARD TO THIS SOFTWARE INCLUDING ALL IMPLIED WARRANTIES OF
# MERCHANTABILITY AND FITNESS. IN NO EVENT SHALL THE AUTHOR BE LIABLE FOR
# ANY SPECIAL, DIRECT, INDIRECT, OR CONSEQUENTIAL DAMAGES OR ANY DAMAGES
# WHATSOEVER RESULTING FROM LOSS OF USE, DATA OR PROFITS, WHETHER IN AN
# ACTION OF CONTRACT, NEGLIGENCE OR OTHER TORTIOUS ACTION, ARISING OUT OF
# OR IN CONNECTION WITH THE USE OR PERFORMANCE OF THIS SOFTWARE.
#

# This summit is in the cloud.

from __future__ import print_function
from collections import defaultdict
from datetime import datetime
from datetime import timedelta
import getopt
import json
import logging as logging_
import os
import pprint
import requests
import sys
import time
try:
    import jmespath
    from jmespath import exceptions
    from jmespath import functions
    have_jmespath = True
except ImportError:
    have_jmespath = False
try:
    import arrow
    have_arrow = True
except ImportError:
    have_arrow = False

libpath = os.path.dirname(os.path.abspath(__file__))
sys.path[:0] = [os.path.join(libpath, os.pardir)]

from pancloud import Credentials, HTTPClient, LoggingService, \
    EventService, DirectorySyncService, __version__

_None = object()  # sentinel used to not set --end default
INDENT = 2
LOGGING_SERVICE_EPOCH = 1504224000  # 2017-09-01T00:00:00+00:00
DEFAULT_EVENT_CHANNEL_ID = 'EventFilter'
debug = 0


def main():
    options = parse_opts()

    if options['debug']:
        logger = logging_.getLogger()
        logger.setLevel(logging_.DEBUG)
        log_format = '%(message)s'
        handler = logging_.StreamHandler()
        formatter = logging_.Formatter(log_format)
        handler.setFormatter(formatter)
        logger.addHandler(handler)

    if (sum(bool(x) for x in [options['logging_api'],
                              options['event_api'],
                              options['directory_sync_api']]) > 1):
        print('Only a single Service API request allowed',
              file=sys.stderr)
        sys.exit(1)

    if options['credentials']:
        credentials_ = credentials(options)
    else:
        credentials_ = None

    if options['http_client']:
        httpclient_ = httpclient(options, credentials_)
    else:
        httpclient_ = None

    if options['logging_api']:
        logging(options, httpclient_)

    if options['event_api']:
        if options['id'] is None:
            options['id'] = DEFAULT_EVENT_CHANNEL_ID
        event(options, httpclient_)

    if options['directory_sync_api']:
        directory_sync(options, httpclient_)

    sys.exit(0)


def credentials(options):
    def write_credentials(c, options):
        k = 'Credentials.write_credentials'

        R = options['R']
        try:
            x = c.write_credentials(**R['R2_obj'][k])
        except Exception as e:
            print_exception(k, e)
            sys.exit(1)

        print(k, file=sys.stderr)
        if x is not None:
            print_response_json(options, k, x)

    k = 'Credentials'

    R = options['R']
    try:
        x = Credentials(**R['R0_obj'][k])
    except Exception as e:
        print_exception(k, e)
        sys.exit(1)

    setters(options, x)
    methods(options, x)

    # XXX pre-dates -m
    if options['write_credentials']:
        write_credentials(x, options)

    return x


def setters(options, class_):
    name = class_.__class__.__name__
    for method, val in options['s'][name].items():
        k = '%s.%s' % (name, method)
        try:
            method_ = class_.__class__.__dict__[method]
        except KeyError:
            print('no class.method: %s' % k, file=sys.stderr)
            sys.exit(1)

        if not isinstance(method_, property):
            print('not @property decorated: %s' % k, file=sys.stderr)
            sys.exit(1)

        method_ = method_.fset

        if not hasattr(method_, '__call__'):
            print('not setter: %s' % k, file=sys.stderr)
            sys.exit(1)

        try:
            method_(class_, val)
        except Exception as e:
            print_exception(k, e)
            sys.exit(1)

        try:
            x = json.dumps(val, separators=(',', ':'))
        except ValueError as e:
            x = e

        print('%s = %s' % (k, x), file=sys.stderr)


def methods(options, class_):
    name = class_.__class__.__name__
    for method in options['m'][name]:
        k = '%s.%s' % (name, method)
        try:
            method_ = class_.__class__.__dict__[method]
        except KeyError:
            print('no class.method: %s' % k, file=sys.stderr)
            sys.exit(1)

        # if @property decorated call getter
        if isinstance(method_, property):
            method_ = method_.fget

        if not hasattr(method_, '__call__'):
            print('not callable: %s' % k, file=sys.stderr)
            sys.exit(1)

        R = options['R']
        try:
            x = method_(class_, **R['R2_obj'][k])
        except Exception as e:
            print_exception(k, e)
            sys.exit(1)

        if x is not None:
            if isinstance(x, requests.models.Response):
                print_status(k, x, options)
                print_response(x, options, k)
                exit_for_http_status(x)
            else:
                print(k, file=sys.stderr)
                try:
                    json.dumps(x)
                except (TypeError, ValueError):
                    print(pprint.pformat(x, indent=INDENT))
                else:
                    print_response_json(options, k, x)
        else:
            print(k, file=sys.stderr)


def httpclient(options, c):
    k = 'HTTPClient'

    R = options['R']
    try:
        x = HTTPClient(credentials=c,
                       **R['R0_obj'][k])
    except Exception as e:
        print_exception(k, e)
        sys.exit(1)

    setters(options, x)
    methods(options, x)

    return x


def logging(options, session):
    def query(api, options):
        k = 'LoggingService.query'

        R = options['R']
        if R['R1_obj'][k] is None:
            x = {}
        else:
            x = R['R1_obj'][k].copy()
        if ('startTime' not in x and
           options['start_seconds'] is not None):
            x['startTime'] = options['start_seconds']
        if ('endTime' not in x and
           options['end_seconds'] is not None):
            x['endTime'] = options['end_seconds']

        if options['debug'] > 1:
            if 'startTime' in x:
                t = datetime.utcfromtimestamp(x['startTime'])
                print('startTime:', t, file=sys.stderr)
            if 'endTime' in x:
                t = datetime.utcfromtimestamp(x['endTime'])
                print('endTime:', t, file=sys.stderr)

        if options['debug'] > 2:
            print(pprint.pformat(x, indent=INDENT),
                  file=sys.stderr)

        if not x and R['R1_obj'][k] is None:
            x = None  # preserve None if no parameters added

        try:
            r = api.query(json=x,
                          **R['R2_obj'][k])
        except Exception as e:
            print_exception(k, e)
            sys.exit(1)

        print_status(k, r, options)
        json_ = print_response(r, options, k)
        exit_for_http_status(r)

        if json_ is not None and options['id'] is None and 'queryId' in json_:
            options['id'] = json_['queryId']

    def poll(api, options):
        k = 'LoggingService.poll'

        R = options['R']
        try:
            r = api.poll(query_id=options['id'],
                         sequence_no=options['seq'],
                         params=R['R1_obj'][k],
                         **R['R2_obj'][k])
        except Exception as e:
            print_exception(k, e)
            sys.exit(1)

        print_status(k, r, options)
        print_response(r, options, k)
        exit_for_http_status(r)

    def xpoll(api, options):
        k = 'LoggingService.xpoll'

        R = options['R']
        try:
            for x in api.xpoll(query_id=options['id'],
                               sequence_no=options['seq'],
                               delete_query=options['delete'],
                               params=R['R1_obj'][k],
                               **R['R2_obj'][k]):
                print_response_json(options, k, x)

        except Exception as e:
            print_exception(k, e)
            sys.exit(1)

    def delete(api, options):
        k = 'LoggingService.delete'

        R = options['R']
        try:
            r = api.delete(query_id=options['id'],
                           **R['R2_obj'][k])
        except Exception as e:
            print_exception(k, e)
            sys.exit(1)

        print_status(k, r, options)
        print_response(r, options, k)
        exit_for_http_status(r)

    def write(api, options):
        k = 'LoggingService.write'

        R = options['R']
        try:
            # XXX use R2 to specify "log_type"
            r = api.write(vendor_id=options['id'],
                          json=R['R1_obj'][k],
                          **R['R2_obj'][k])
        except Exception as e:
            print_exception(k, e)
            sys.exit(1)

        print_status(k, r, options)
        print_response(r, options, k)
        exit_for_http_status(r)

    k = 'LoggingService'

    R = options['R']
    try:
        api = LoggingService(session=session,
                             **R['R0_obj'][k])
    except Exception as e:
        print_exception(k, e)
        sys.exit(1)

    if options['debug'] > 0:
        print(api, file=sys.stderr)

    if options['query']:
        query(api, options)

    if options['poll']:
        poll(api, options)

    if options['xpoll']:
        try:
            xpoll(api, options)
        except KeyboardInterrupt:
            sys.exit(1)

    if options['delete'] and not options['xpoll']:
        delete(api, options)

    if options['write']:
        write(api, options)

    setters(options, api)
    methods(options, api)


def event(options, session):
    def generic(api, options, func, k):
        R = options['R']
        try:
            r = func(channel_id=options['id'],
                     **R['R2_obj'][k])
        except Exception as e:
            print_exception(k, e)
            sys.exit(1)

        print_status(k, r, options)
        print_response(r, options, k)
        exit_for_http_status(r)

    def set_filters(api, options):
        k = 'EventService.set_filters'

        R = options['R']
        try:
            r = api.set_filters(channel_id=options['id'],
                                json=R['R1_obj'][k],
                                **R['R2_obj'][k])
        except Exception as e:
            print_exception(k, e)
            sys.exit(1)

        print_status(k, r, options)
        print_response(r, options, k)
        exit_for_http_status(r)

    def get_filters(api, options):
        k = 'EventService.get_filters'
        generic(api, options, api.get_filters, k)

    def xpoll(api, options):
        k = 'EventService.xpoll'

        R = options['R']
        try:
            for x in api.xpoll(channel_id=options['id'],
                               json=R['R1_obj'][k],
                               ack=options['ack'],
                               follow=options['follow'],
                               **R['R2_obj'][k]):
                print('%s:' % k, end='', file=sys.stderr)
                event_print_status(options, [x])
                print(file=sys.stderr)
                print_response_json(options, k, x)
        except Exception as e:
            print_exception(k, e)
            sys.exit(1)

    def poll(api, options):
        k = 'EventService.poll'

        R = options['R']
        try:
            r = api.poll(channel_id=options['id'],
                         json=R['R1_obj'][k],
                         **R['R2_obj'][k])
        except Exception as e:
            print_exception(k, e)
            sys.exit(1)

        print_status(k, r, options)
        print_response(r, options, k)
        exit_for_http_status(r)

    def ack(api, options):
        k = 'EventService.ack'
        generic(api, options, api.ack, k)

    def nack(api, options):
        k = 'EventService.nack'
        generic(api, options, api.nack, k)

    def flush(api, options):
        k = 'EventService.flush'
        generic(api, options, api.flush, k)

    k = 'EventService'

    R = options['R']
    try:
        api = EventService(session=session,
                           **R['R0_obj'][k])
    except Exception as e:
        print_exception(k, e)
        sys.exit(1)

    if options['debug'] > 0:
        print(api, file=sys.stderr)

    if options['set']:
        set_filters(api, options)

    if options['get']:
        get_filters(api, options)

    if options['poll']:
        poll(api, options)

    if options['xpoll']:
        try:
            xpoll(api, options)
        except KeyboardInterrupt:
            sys.exit(1)

    if options['ack'] and not options['xpoll']:
        ack(api, options)

    if options['nack']:
        nack(api, options)

    if options['flush']:
        flush(api, options)

    setters(options, api)
    methods(options, api)


def directory_sync(options, session):
    def generic(api, options, func, k):
        R = options['R']
        try:
            r = func(**R['R2_obj'][k])
        except Exception as e:
            print_exception(k, e)
            sys.exit(1)

        print_status(k, r, options)
        print_response(r, options, k)
        exit_for_http_status(r)

    def query(api, options):
        k = 'DirectorySyncService.query'

        R = options['R']
        try:
            r = api.query(object_class=options['id'],
                          json=R['R1_obj'][k],
                          **R['R2_obj'][k])
        except Exception as e:
            print_exception(k, e)
            sys.exit(1)

        print_status(k, r, options)
        print_response(r, options, k)
        exit_for_http_status(r)

    def count(api, options):
        k = 'DirectorySyncService.count'

        R = options['R']
        try:
            r = api.count(object_class=options['id'],
                          params=R['R1_obj'][k],
                          **R['R2_obj'][k])
        except Exception as e:
            print_exception(k, e)
            sys.exit(1)

        print_status(k, r, options)
        print_response(r, options, k)
        exit_for_http_status(r)

    def domains(api, options):
        k = 'DirectorySyncService.domains'
        generic(api, options, api.domains, k)

    def attributes(api, options):
        k = 'DirectorySyncService.attributes'
        generic(api, options, api.attributes, k)

    k = 'DirectorySyncService'

    R = options['R']
    try:
        api = DirectorySyncService(session=session,
                                   **R['R0_obj'][k])
    except Exception as e:
        print_exception(k, e)
        sys.exit(1)

    if options['debug'] > 0:
        print(api, file=sys.stderr)

    if options['query']:
        query(api, options)

    if options['count']:
        count(api, options)

    if options['domains']:
        domains(api, options)

    if options['attributes']:
        attributes(api, options)

    setters(options, api)
    methods(options, api)


def print_exception(action, e):
    print('%s:' % action, end='', file=sys.stderr)
    print(' %s:' % e.__class__.__name__, end='', file=sys.stderr)
    print(' "%s"' % e, file=sys.stderr)


def print_status(action, r, options):
    print('%s:' % action, end='', file=sys.stderr)

    if r.status_code is not None:
        print(' %s' % r.status_code, end='', file=sys.stderr)
    if r.reason is not None:
        print(' %s' % r.reason, end='', file=sys.stderr)
    if r.headers is not None:
        print(' %s' % r.headers.get('content-length'),
              end='', file=sys.stderr)
    try:
        x = r.json()
    except ValueError:
        print(file=sys.stderr)
        return

    if 'errorCode' in x:
        print(": %s" % x['errorCode'], end='', file=sys.stderr)
    if 'errorMessage' in x:
        print(": '%s'" % x['errorMessage'], end='', file=sys.stderr)

    if (options['logging_api']):
        logging_print_status(options, x)
    if (options['event_api']):
        event_print_status(options, x)
    if (options['directory_sync_api']):
        directory_sync_print_status(options, x)

    print(file=sys.stderr)


def logging_print_status(options, x):
    if 'queryStatus' in x:
        print(" queryStatus=%s" % x['queryStatus'], end='',
              file=sys.stderr)
        # XXX validate expected
        if options['query'] or options['poll']:
            if x['queryStatus'] not in ['RUNNING', 'FINISHED',
                                        'JOB_FINISHED', 'JOB_FAILED']:
                print("(INVALID)", end='', file=sys.stderr)
    if 'queryId' in x:
        print(" queryId=%s" % x['queryId'], end='', file=sys.stderr)
    if 'sequenceNo' in x:
        print(" sequenceNo=%s" % x['sequenceNo'], end='', file=sys.stderr)
    try:
        v = x['result']['esResult']['size']
    except (TypeError, KeyError):
        pass
    else:
        print(' size=%d' % v, end='', file=sys.stderr)


def event_print_status(options, x):
    for ev in x:
        if 'logType' in ev:
            print(' %s' % ev['logType'], end='', file=sys.stderr)
        if 'event' in ev:
            print('[size=%d]' % len(ev['event']), end='', file=sys.stderr)
            if options['debug'] > 0:
                k = 'receive_time'
                try:
                    seconds = ev['event'][-1][k]
                    t = datetime.utcfromtimestamp(seconds)
                    print(' %s' % t, end='', file=sys.stderr)
                except (IndexError, KeyError):
                    pass

                t0 = datetime.utcfromtimestamp(0)
                seq0 = 0
                try:
                    for log in ev['event']:
                        t1 = datetime.utcfromtimestamp(log[k])
                        seq1 = log['seqno']
                        if t0 > t1:
                            # XXX logs not in chronological order
                            print('\nWarning: %s: %s %s > %s %s' %
                                  (k, seq0, t0, seq1, t1),
                                  end='', file=sys.stderr)
                        t0 = t1
                        seq0 = seq1
                except KeyError:
                    pass


def directory_sync_print_status(options, x):
    if 'count' in x:
        print(" count=%d" % x['count'], end='', file=sys.stderr)
    if 'pageNumber' in x:
        print(" pageNumber=%d" % x['pageNumber'], end='', file=sys.stderr)
    if 'pageSize' in x:
        print(" pageSize=%d" % x['pageSize'], end='', file=sys.stderr)
    if 'unreadResults' in x:
        print(" unreadResults=%d" % x['unreadResults'], end='',
              file=sys.stderr)


def print_response(r, options, k):
    if options['debug'] > 2:
        # request
        if r.request.headers is not None:
            # XXX ok to leak Authorization header here
            print(pprint.pformat(dict(r.request.headers),
                                 indent=INDENT), file=sys.stderr)
        print(r.request.body, file=sys.stderr)
        # response
        if r.headers is not None:
            print(pprint.pformat(dict(r.headers),
                                 indent=INDENT), file=sys.stderr)
        print(r.text, file=sys.stderr)

    if r.text is None or r.headers is None:
        return

    x = r.headers.get('content-type')
    if x is None:
        return

    if x.startswith('application/json'):
        try:
            obj = r.json()
        except ValueError as e:
            print(e, file=sys.stderr)
            sys.exit(1)

        print_response_json(options, k, obj)
        return obj
    else:
        print('WARNING: Response Content-Type:', x, file=sys.stderr)


def print_response_json(options, k, x):
    if k in options['print']:
        print_ = options['print'][k]
    else:
        k_, _ = k.split('.')
        if k_ in options['print']:
            print_ = options['print'][k_]
        else:
            return

    if print_['jmespath'] is not None:
        x = jmespath_search(print_['jmespath'], x,
                            options['jmespath_options'])

    if print_['print_json']:
        print_json(x)

    if print_['print_python']:
        print_python(x)


def exit_for_http_status(r):
    if r.status_code is not None:
        if not (200 <= r.status_code < 300):
            sys.exit(1)
        else:
            return

    print('status_code:', r.status_code, file=sys.stderr)
    sys.exit(1)


def print_python(obj):
    print(pprint.pformat(obj, indent=INDENT))


def print_json(obj):
    print(json.dumps(obj, sort_keys=True, indent=INDENT,
                     separators=(',', ': ')))


# Configure JMESPath custom function: isotime()
def jmespath_init():
    class CustomFunctions(functions.Functions):
        @functions.signature({'types': ['number']})
        def _func_isotime(self, x):
            d = datetime.fromtimestamp(x)
            return d.isoformat()

    options = jmespath.Options(custom_functions=CustomFunctions())
    return options


def jmespath_search(expression, obj, options):
    try:
        x = jmespath.search(expression, obj, options=options)
    except exceptions.JMESPathError as e:
        print('JMESPath %s: %s' % (e.__class__.__name__, e), file=sys.stderr)
        sys.exit(1)

    return x


def process_arg(x):
    stdin_char = '-'

    if x == stdin_char:
        lines = sys.stdin.readlines()
    else:
        try:
            f = open(x)
            lines = f.readlines()
            f.close()
        except IOError:
            lines = [x]

    if debug > 1:
        print(pprint.pformat(lines, indent=INDENT), file=sys.stderr)

    lines = ''.join(lines)
    return lines


def process_json_args(args, init=None):
    obj = init
    for r in args:
        try:
            x = json.loads(r)
        except ValueError as e:
            print('%s: %s' % (e, r), file=sys.stderr)
            sys.exit(1)

        if obj is None:
            if isinstance(x, list):
                obj = []
            elif isinstance(x, dict):
                obj = {}
            else:
                print('Invalid --R[0-2] type: %s: %s' % (type(x), x),
                      file=sys.stderr)
                sys.exit(1)
        try:
            if isinstance(x, list):
                if x:
                    obj.append(x[0])
            elif isinstance(x, dict):
                obj.update(x)
            else:
                print('Invalid --R[0-2] type: %s: %s' % (type(x), x),
                      file=sys.stderr)
                sys.exit(1)
        except AttributeError:
            print("Can't mix --R[0-2] types", file=sys.stderr)
            sys.exit(1)

    # XXX used for debug only
    try:
        json_arg = json.dumps(obj, indent=INDENT)
    except ValueError as e:
        print(e, file=sys.stderr)
        sys.exit(1)

    if debug > 1 and obj:
        print(pprint.pformat(obj, indent=INDENT), file=sys.stderr)
        print(json_arg, file=sys.stderr)

    return obj


def validate_time(arg, seconds):
    if seconds < LOGGING_SERVICE_EPOCH:
        t0 = datetime.utcfromtimestamp(LOGGING_SERVICE_EPOCH)
        t = datetime.utcfromtimestamp(seconds)
        print('Warning: %s: "%s" < logging service epoch "%s"' %
              (arg, t, t0),
              file=sys.stderr)


def debug_time(func):
    def wrapper(*args, **kwargs):
        seconds = func(*args, **kwargs)
        if debug > 1:
            t = datetime.utcfromtimestamp(seconds)
            print('time', seconds, t, file=sys.stderr)
        return seconds

    return wrapper


@debug_time
def process_time(x):
    def nice_time(time):
        import re

        m = re.match('^-?(\d+)([sSmMhHdDwW]?)$', time)
        if not m:
            raise ValueError('Invalid time: %s' % time)

        kwargs = {}
        x = m.groups()
        modifier = x[1].lower()
        if modifier == '' or modifier == 's':
            kwargs['seconds'] = int(x[0])
        elif modifier == 'm':
            kwargs['minutes'] = int(x[0])
        elif modifier == 'h':
            kwargs['hours'] = int(x[0])
        elif modifier == 'd':
            kwargs['days'] = int(x[0])
        elif modifier == 'w':
            kwargs['weeks'] = int(x[0])
        else:
            assert False, 'unhandled modifier: %s' % modifier

        try:
            t = timedelta(**kwargs)
        except OverflowError as e:
            raise OverflowError('Invalid time: %s: %s' % (time, e))

        return t

    try:
        t = nice_time(x)
    except OverflowError as e:
            print(e, file=sys.stderr)
            sys.exit(1)
    except ValueError:
        pass
    else:
        if x[0] == '-':
            return int(-t.total_seconds())
        else:
            return int(t.total_seconds())

    if not have_arrow:
        print('%s: %s' % (str(x), e), file=sys.stderr)
        print('Install arrow module for non Unix epoch time support: '
              'http://arrow.readthedocs.io/', file=sys.stderr)
        sys.exit(1)

    try:
        t = arrow.get(x)
    except arrow.parser.ParserError as e:
        print('%s: %s' % (str(x), e), file=sys.stderr)
        sys.exit(1)

    seconds = t.timestamp

    return seconds


def parse_opts():
    options_R = {
        # class init **kwargs
        'R0': defaultdict(list),
        # class method data/params
        # XXX can't have data and params
        'R1': defaultdict(list),
        # class method **kwargs
        'R2': defaultdict(list),
    }

    options_m = defaultdict(list)

    options_s = defaultdict(
        lambda: defaultdict()
    )

    options_print = defaultdict(
        lambda: defaultdict(
            dict,
            {
                'jmespath': None,
                'print_python': False,
                'print_json': False,
            }
        )
    )

    options = {
        'R': options_R,
        'm': options_m,
        's': options_s,
        'print': options_print,
        'jmespath_options': None,
        'credentials': False,
        'http_client': False,
        'logging_api': False,
        'directory_sync_api': False,
        'event_api': False,
        'delete': False,
        'poll': False,
        'xpoll': False,
        'query': False,
        'write': False,
        'write_credentials': False,
        'id': None,
        'seq': 0,
        'start': None,
        'start_seconds': None,
        'window': None,
        'window_seconds': None,
        'midpoint': None,
        'midpoint_seconds': None,
        'end': None,
        'end_seconds': None,
        'set': False,
        'get': False,
        'ack': False,
        'nack': False,
        'flush': False,
        'follow': False,
        'count': False,
        'domains': False,
        'attributes': False,
        'debug': 0,
        }

    def _options_R(opt, last_c, last_m, arg):
        if opt == 'R0':
            if last_c is None:
                print('--%s has no class context' % opt, file=sys.stderr)
                sys.exit(1)
            options_R[opt][last_c].append(process_arg(arg))

        elif opt in ['R1', 'R2']:
            x = '%s.%s' % (last_c, last_m)
            if last_c is None or last_m is None:
                print('--%s has no class.method context: %s' % (opt, x),
                      file=sys.stderr)
                sys.exit(1)
            options_R[opt][x].append(process_arg(arg))

    def _options_m(last_c, arg):
        if last_c is None:
            print('-m has no class context', file=sys.stderr)
            sys.exit(1)

        options_m[last_c].append(arg)

    def _options_s(last_c, arg):
        if last_c is None:
            print('-s has no class context', file=sys.stderr)
            sys.exit(1)

        x = arg.split('=', 1)
        if len(x) != 2:
            print('-s argument must be setter=json',  file=sys.stderr)
            sys.exit(1)

        try:
            val = json.loads(x[1])
        except ValueError as e:
            print('-s json argument invalid: %s' % e)
            sys.exit(1)

        options_s[last_c][x[0]] = val

    def _options_print(opt, last_c, last_m, arg):
        x = '%s.%s' % (last_c, last_m)
        if last_c and last_m:
            pass
        elif last_c:
            x = last_c
        else:
            print('-%s has no class.method context: %s' % (opt, x),
                  file=sys.stderr)
            sys.exit(1)

        if opt == 'J':
            if not have_jmespath:
                print('Install JMESPath for -J support: http://jmespath.org/',
                      file=sys.stderr)
                sys.exit(1)
            options_print[x]['jmespath'] = arg
            if options['jmespath_options'] is None:
                options['jmespath_options'] = jmespath_init()
        elif opt == 'p':
            options_print[x]['print_python'] = True
        elif opt == 'j':
            options_print[x]['print_json'] = True

    short_options = 'CHLDEm:s:J:pj'
    long_options = [
        'delete', 'poll', 'xpoll', 'query', 'write',
        'start=', 'midpoint=', 'end=', 'window=',
        'id=', 'seq=',
        'set', 'get', 'ack', 'nack', 'flush',
        'follow', 'count', 'domains', 'attributes',
        'R0=', 'R1=', 'R2=',
        'debug=', 'version', 'help',
    ]

    try:
        opts, args = getopt.getopt(sys.argv[1:],
                                   short_options,
                                   long_options)
    except getopt.GetoptError as error:
        print(error, file=sys.stderr)
        sys.exit(1)

    last_c = None  # class
    last_m = None  # method

    for opt, arg in opts:
        if False:
            pass
        elif opt == '-C':
            options['credentials'] = True
            last_c = 'Credentials'
        elif opt == '-H':
            options['http_client'] = True
            last_c = 'HTTPClient'
        elif opt == '-L':
            options['logging_api'] = True
            last_c = 'LoggingService'
        elif opt == '-D':
            options['directory_sync_api'] = True
            last_c = 'DirectorySyncService'
        elif opt == '-E':
            options['event_api'] = True
            last_c = 'EventService'
        elif opt == '--delete':
            options['delete'] = True
            last_m = 'delete'
        elif opt == '--poll':
            options['poll'] = True
            last_m = 'poll'
        elif opt == '--xpoll':
            options['xpoll'] = True
            last_m = 'xpoll'
        elif opt == '--query':
            options['query'] = True
            last_m = 'query'
        elif opt == '--write':
            if last_c == 'Credentials':
                last_m = 'write_credentials'
                options['write_credentials'] = True
            else:
                last_m = 'write'
                options['write'] = True
        elif opt == '--start':
            options['start'] = arg
            options['start_seconds'] = process_time(arg)
        elif opt == '--window':
            options['window'] = arg
            options['window_seconds'] = process_time(arg)
            if options['window_seconds'] < 0:
                print("--window can't be negative", file=sys.stderr)
                sys.exit(1)
        elif opt == '--midpoint':
            options['midpoint'] = arg
            options['midpoint_seconds'] = process_time(arg)
            if options['midpoint_seconds'] < 0:
                print("--midpoint can't be negative", file=sys.stderr)
                sys.exit(1)
        elif opt == '--end':
            options['end'] = arg
            options['end_seconds'] = process_time(arg)
            if options['end_seconds'] == -1:
                # XXX as a special case allow end -1 to override default
                # which allows test case of empty body
                options['end_seconds'] = _None
            elif options['end_seconds'] < 0:
                print("--end can't be negative", file=sys.stderr)
                sys.exit(1)
        elif opt == '--id':
            options['id'] = arg
        elif opt == '--seq':
            options['seq'] = arg
        elif opt == '--set':
            options['set'] = True
            last_m = 'set_filters'
        elif opt == '--get':
            options['get'] = True
            last_m = 'get_filters'
        elif opt == '--ack':
            options['ack'] = True
            last_m = 'ack'
        elif opt == '--nack':
            options['nack'] = True
            last_m = 'nack'
        elif opt == '--flush':
            options['flush'] = True
            last_m = 'flush'
        elif opt == '--follow':
            options['follow'] = True
        elif opt == '--count':
            options['count'] = True
            last_m = 'count'
        elif opt == '--domains':
            options['domains'] = True
            last_m = 'domains'
        elif opt == '--attributes':
            options['attributes'] = True
            last_m = 'attributes'
        elif opt in ['--R0', '--R1', '--R2']:
            _options_R(opt[2:], last_c, last_m, arg)
        elif opt == '-m':
            _options_m(last_c, arg)
            last_m = arg
        elif opt == '-s':
            _options_s(last_c, arg)
            last_m = None
        elif opt in ['-p', '-j', '-J']:
            _options_print(opt[1:], last_c, last_m, arg)
        elif opt == '--debug':  # XXX positional
            try:
                options['debug'] = int(arg)
                if options['debug'] < 0:
                    raise ValueError
            except ValueError:
                print('Invalid debug:', arg, file=sys.stderr)
                sys.exit(1)
            if options['debug'] > 3:
                print('Maximum debug level is 3', file=sys.stderr)
                sys.exit(1)
            global debug
            debug = options['debug']
        elif opt == '--version':
            print('pancloud', __version__)
            sys.exit(0)
        elif opt == '--help':
            usage()
            sys.exit(0)
        else:
            assert False, 'unhandled option %s' % opt

    # --start time
    #   Use negative seconds to specify relative time to end.
    #
    #   Can also use a time modifier preceeding seconds:
    #     s|S: seconds
    #     m|M: minutes
    #     h|H: hours
    #     d|D: days
    #     w|W: weeks
    #
    #   Example: --start -7d --end 2018-06-08
    #   Result: startTime: 2018-06-01 00:00:00 endTime: 2018-06-08 00:00:00
    #
    # --midpoint time
    #   Use seconds in --window to specify start-end duration to
    #   midpoint.
    #
    #   Example: --window 2d --midpoint 2018-06-02
    #   Result: startTime: 2018-06-01 00:00:00 endTime: 2018-06-03 00:00:00
    #
    # --end time
    #   Defaults to current time.

    if options['midpoint_seconds'] is not None:
        if options['window_seconds'] is not None:
            offset = options['window_seconds'] // 2
            options['start_seconds'] = (options['midpoint_seconds'] -
                                        offset)
            options['end_seconds'] = (options['midpoint_seconds'] +
                                      offset)
        else:
            print('--midpoint requires --window for start-end',
                  file=sys.stderr)
            sys.exit(1)

    if options['end_seconds'] is _None:
        options['end_seconds'] = None
    elif options['end_seconds'] is None:
        options['end_seconds'] = int(time.time())

    if (options['start_seconds'] is not None and
       options['start_seconds'] < 0):
        options['start_seconds'] = (options['start_seconds'] +
                                    options['end_seconds'])

    if options['start_seconds'] is not None:
        validate_time('startTime', options['start_seconds'])
    if options['end_seconds'] is not None:
        validate_time('endTime', options['end_seconds'])

    headers = None
    if not options['credentials'] and 'ACCESS_TOKEN' in os.environ:
        headers = {
            'Authorization': 'Bearer %s' % os.environ['ACCESS_TOKEN'],
            'Accept': 'application/json',
        }

    for k in list(options_R.keys()):
        init = None
        if k == 'R0' and headers is not None:
            init = {'headers': headers}
        if k == 'R1':
            # default R1 to None so don't send body unless specified
            options_R[k + '_obj'] = defaultdict(lambda: None)
        else:
            options_R[k + '_obj'] = defaultdict(dict)
        for x in options_R[k].keys():
            r = process_json_args(options_R[k][x], init)
            if k in ['R0', 'R1', 'R2'] and isinstance(r, dict):
                pass
            elif k in ['R1'] and isinstance(r, list):
                pass
            else:
                print('Invalid --%s type: %s' % (k, type(r)),
                      file=sys.stderr)
                sys.exit(1)
            options_R[k + '_obj'][x] = r

    if options['debug'] > 2:
        s = pprint.pformat(options, indent=INDENT)
        print(s, file=sys.stderr)

    return options


def usage():
    usage = '''%s [options]
    -L                    Logging Service API request using
                          LoggingService() class
      --delete            delete logging query
      --poll              poll logging query results
      --xpoll             poll all logging query records
      --query             query logging records
      --write             write logging records
      --start time        startTime (-time for relative to end)
      --window time       time duration for midpoint
      --midpoint time     midpoint in window for start-end
      --end time          endTime (default: current time)
      --id id             queryId
      --seq no            sequenceNo
    -E                    Event Service API request using
                          EventService() class
      --set               set event channel filters
      --get               get event channel filters
      --ack               acknowledgement for events read
                          (sets ack point = read point)
      --nack              negative acknowledgement for events read
                          (sets read point = ack point)
      --flush             discard unread events 
                          (set read and ack point to end of channel)
      --poll              read events
      --xpoll             poll all events until drained
                          (use --ack to ack after each poll)
      --follow            follow xpoll after drained: xpoll(follow=True)
      --id id             channelId (default: "%s")
    -D                    Directory Sync Service API request using
                          DirectorySyncService() class
      --query             query directory entries
      --count             get count of directory entries
      --domains           get directory domains
      --attributes        get directory attributes
      --id class          objectClass
    -H                    use HTTPClient() session
    -C                    use Credentials() class
      --write             write_credentials() method
    -m method             invoke class method
    -s setter=json        invoke class setter
                          multiple -[ms]'s allowed
    --R0 json             class constructor args (**kwargs)
    --R1 json             class method body or QUERY_STRING using
                          json= or params= arguments
    --R2 json             class method args (**kwargs)
                          multiple --R[012]'s allowed, will be merged
    -J expression         JMESPath expression for JSON response data
    -p                    print response in Python to stdout
    -j                    print response in JSON to stdout
                          multiple -[Jpj]'s allowed
    --debug level         enable debug level up to 3
    --version             display version
    --help                display usage
''' % (os.path.basename(sys.argv[0]), DEFAULT_EVENT_CHANNEL_ID)
    print(usage, end='')


if __name__ == '__main__':
    main()
