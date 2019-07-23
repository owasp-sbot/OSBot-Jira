import requests

def run(event, context):
    #return event.get('url') + 'aaa'
    r = requests.get(event.get('url'))

    return r.text
    #return '...**^^.This is a request test for url: {0}'.format(event.get('url'))