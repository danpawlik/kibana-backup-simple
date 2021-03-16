#!/usr/bin/env python3

# Kibana documentation:
# https://www.elastic.co/guide/en/kibana/master/spaces-api-post.html

import argparse
import json
import requests
import sys


def manage_space(action, host, space_name, readonly, disable, user, password,
                 description, color, initials, image_url):
    """ Create, update or delete space in Kibana"""

    payload = {
        "id": space_name.lower(),
        "name": space_name,
        "description": description,
    }

    # Taked from
    # https://www.elastic.co/guide/en/kibana/master/features-api-get.html
    # curl localhost:5601/api/features | python3 -m json.tool - | grep '"id":'
    if readonly:
        payload['disabledFeatures'] = ["discover",
                                       "canvas", "ml", "maps",
                                       "infrastructure", "logs", "apm",
                                       "uptime", "siem",
                                       "dev_tools", "advancedSettings",
                                       "indexPatterns",
                                       "savedObjectsManagement",
                                       "monitoring"]
                                      # "visualize", "dashboard"]
    if disable:
        payload['disabledFeatures'] = disable

    if color:
        payload['color'] = color

    if initials:
        payload['initials'] = initials

    if image_url:
        payload['imageUrl'] = image_url

    if action == 'create':
        url = kibana_url + '/api/spaces/space'
        r = requests.post(url, auth=(user, password),
                          headers={'kbn-xsrf': 'reporting'},
                          data=json.dumps(payload))
    elif action == 'update':
        url = kibana_url + '/api/spaces/space/' + space_name.lower()
        r = requests.put(url, auth=(user, password),
                         headers={'kbn-xsrf': 'reporting'},
                         data=json.dumps(payload))
    elif action == 'delete':
        url = kibana_url + '/api/spaces/space/' + space_name.lower()
        r = requests.delete(url, auth=(user, password),
                            headers={'kbn-xsrf': 'reporting'})

    if r.ok:
        print("Space %s %sd" % (space_name, action))
    else:
        print("Some problems occured on %s %s: %s" % (space_name, action,
                                                      r.text))


if __name__ == '__main__':
    args_parser = argparse.ArgumentParser(
        description='Create or manage Kibana spaces')
    args_parser.add_argument('action', choices=['create', 'update', 'delete'])
    args_parser.add_argument('--kibana-url', default='http://127.0.0.1:5601',
                             help='URL to access Kibana API')
    args_parser.add_argument('--space-name', required=True,
                             help='Name of the Kibana space')
    args_parser.add_argument('--readonly', action='store_true',
                             help='Create readonly space. '
                             'Do not use with --disable option')
    args_parser.add_argument('--disable', action='append', nargs='+',
                             help='Disable feautures for the space.'
                             'It can be used multiple times')
    args_parser.add_argument('--user', default='', help='Kibana user')
    args_parser.add_argument('--password', default='', help='Kibana password')
    args_parser.add_argument('--description', default='',
                             help='Space description')
    args_parser.add_argument('--color', help='Specifies the hexadecimal color '
                             'code used in the space avatar')
    args_parser.add_argument('--initials', help='Specifies the initials shown '
                             'in the space avatar')
    args_parser.add_argument('--image-url', help='Specifies the data-url '
                             'encoded image to display in the space avatar')

    args = args_parser.parse_args()

    kibana_url = args.kibana_url
    if (not args.kibana_url.startswith('http') and
            not args.kibana_url.startswith('https')):
        kibana_url = "http://%s" % args.kibana_url

    disable = args.disable
    if args.disable:
        if args.readonly:
            print("Can't use readonly argument with disable. Use one of them")
            sys.exit(1)
        disable = sum(args.disable, [])

    manage_space(args.action, kibana_url, args.space_name, args.readonly,
                 disable, args.user, args.password, args.description,
                 args.color, args.initials, args.image_url)
