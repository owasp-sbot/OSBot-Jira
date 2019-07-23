import base64
import os
import asyncio

from utils.Process import Process
from utils.aws.Lambdas import load_dependency


def run(event, context):


    load_dependency("pyppeteer")                         # (on first run downloads a zip file from S3 to /tmp/lambdas-dependencies/pyppeteer/ which contains
                                                         #   the contents of `pip3 install pyppeteer - t pyppeteer` and the headless_shell file created by
                                                         #   https://github.com/sambaiz/puppeteer-lambda-starter-kit
                                                         #   This command also sets the add the /tmp/lambdas-dependencies/pyppeteer/ to sys.path

    path_headless_shell          = '/tmp/lambdas-dependencies/pyppeteer/headless_shell'     # path to headless_shell AWS Linux executable
    path_page_screenshot         = '/tmp/screenshot.png'                                    # path to store screenshot of url loaded
    os.environ['PYPPETEER_HOME'] = '/tmp'                                                   # tell pyppeteer to use this read-write path in Lambda aws
    target_url                   = event.get('url')                                         # get url to load from lambda params
    doc_type                     = event.get('doc_type')

    async def get_screenshot():                                                             # async method to run request

        from pyppeteer import launch                                                        # import pyppeteer dependency
        Process.run("chmod", ['+x', path_headless_shell])                                   # set the privs of path_headless_shell to execute
        browser = await launch(executablePath = path_headless_shell,                        # lauch chrome (i.e. headless_shell)
                               args = ['--no-sandbox','--single-process'])                  # two key settings or the requests will not work

        page = await browser.newPage()                                                      # typical pyppeteer code, where we create a new Page object
        await page.goto(target_url)                                                         #   - open an url

        await page.waitFor(2 * 1000);  # To Remove
        #await page.waitForNavigation(); not working

        if doc_type and doc_type == 'pdf':
            await page.pdf({'path': path_page_screenshot});
        else:
            await page.screenshot({'path': path_page_screenshot})                           #   - take a screenshot of the page loaded and save it

        await browser.close()                                                               #   - close the browser


    asyncio.get_event_loop().run_until_complete(get_screenshot())                           # event loop to start the run async method which will open the
                                                                                            #   url provided in the lambda params and save it as an png
    with open(path_page_screenshot, "rb") as image_file:                                    # open path_page_screenshot file
        encoded_png =  base64.b64encode(image_file.read()).decode()                         # save it as a png string (base64 encoded to make it easier to return)

    return { "base64_data" : encoded_png}                                                   # return value to Lambda caller


