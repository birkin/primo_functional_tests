import asyncio, datetime, logging, os
from playwright.async_api import async_playwright


LOG_PATH: str = os.environ['PRIMO_F_TESTS__LOG_PATH']

logging.basicConfig(
    filename=LOG_PATH,
    level=logging.DEBUG,
    format='[%(asctime)s] %(levelname)s [%(module)s-%(funcName)s()::%(lineno)d] %(message)s',
    datefmt='%d/%b/%Y %H:%M:%S' )
log = logging.getLogger(__name__)
log.debug( 'logging ready' )


# async def main():
#     async with async_playwright() as p:
#         browser = await p.chromium.launch()
#         page = await browser.new_page()
#         await page.goto("http://playwright.dev")
#         print(await page.title())
#         await browser.close()


async def main():
    start_time_all = datetime.datetime.now()
    elements: list = list( range(3) )
    async with async_playwright() as p:
        rslt = []
        for el in elements:
            title = await process_element( p )
            rslt.append( title )
        log.debug( f'rslt, ``{rslt}``' )
    end_time_all = datetime.datetime.now()
    elapsed_all = str( end_time_all - start_time_all )
    log.debug( f'elapsed for set, ``{elapsed_all}``')


async def process_element( p ):
    start = datetime.datetime.now()
    browser = await p.chromium.launch()
    page = await browser.new_page()
    await page.goto("http://playwright.dev")
    # print(await page.title())
    title = await page.title()
    await browser.close()
    end = datetime.datetime.now()
    elapsed = str( end - start )
    log.debug( f'elapsed for element, ``{elapsed}``' )
    return title


asyncio.run( main() )

