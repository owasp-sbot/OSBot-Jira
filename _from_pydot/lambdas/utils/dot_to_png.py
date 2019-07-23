from osbot_aws.apis.Lambda import Lambda
from pbx_gs_python_utils.utils.Lambdas_Helpers import slack_message


def run(event, context):
    channel = event.get('channel')
    try:
        dot_to_svg = Lambda('utils.dot_to_svg').invoke
        svg_to_png = Lambda('utils.svg_to_png').invoke
        svg        = dot_to_svg(event)
        result     = svg_to_png({"svg": svg , "width": event.get("width")})
        if result.get('image'):
            return  result['image']
        return { 'error' : result}
    except Exception as error:
        slack_message(":red_circle: Error in dot_to_png: {0}".format(error), [], channel)
        return { 'error': error }