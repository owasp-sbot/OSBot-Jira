from osbot_aws.apis.Lambda import Lambda
from gw_bot.helpers.Lambda_Helpers import slack_message


def run(event, context):
    channel = event.get('channel')
    try:
        dot_to_svg = Lambda('gw_bot.lambdas.dot_to_svg').invoke
        svg_to_png = Lambda('gw_bot.lambdas.svg_to_png').invoke
        svg        = dot_to_svg(event)
        result     = svg_to_png({"svg": svg , "width": event.get("width")})
        if result.get('image'):
            return  result['image']
        return { 'error' : result}
    except Exception as error:
        slack_message(":red_circle: Error in dot_to_png: {0}".format(error), [], channel)
        return { 'error': error }