import trio

from selenium_trio.remote_webdriver import TrioAsyncDriver


async def main():
    page_url = 'https://google.com'
    driver = await TrioAsyncDriver.create_local_driver()

    # for now, all new async methods have a '2' suffix
    await driver.get2(page_url)
    link_elements = await driver.find_elements_by_xpath2('//a')
    link1_href = await link_elements[0].get_attribute2('href')


if __name__ == '__main__':
    trio.run(main)
