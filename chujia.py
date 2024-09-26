import asyncio
from pyppeteer import launch, errors
import pandas as pd
from datetime import datetime
import random
import time
import re
import math
import traceback
import logging
import os

# Cookie 字符串
cookie_string1 = """
__jdv=95931165|direct|-|none|-|1727172014758; __jdu=17271720147572010223461; wlfstk_smdl=csqbi3pz51qocg6tv30uo6jsss02he0u; TrackID=1eKZdLWDdjy7O6ar1GnZWnZv_t881OmyMc0RwN3WxrNGYRnhyt2Rg81SqzeNO5E8SPu0RouMx1sUrSWh21CPmiFpl1wLQUZ7WKyNpGxo3Ut8; thor=1A1D846F9448AEBED2C62C1C84D7847C8D01CC69380D2CEDDBA21085C51E62941883119B14D4148CDF614B3D87D1C702022EC20089BB36204B21901D6B0A05DA09E7B77F13AC136B63B4E5FFE77BD3F0DE67E546EEFE8B0D7831C95E68B9145185DCF975AB5EC17E6BE481F5E3563FAE078B51EA9D0189851ACB23D94B64927291108594A80B8EE80B0B9FAFCFC646337C5DACE71236ABC4F533E48A19B873F0; light_key=AASBKE7rOxgWQziEhC_QY6yaz1ka-nzZKgvHCxRlMRzYKizLDOqFOVZ_bBD_OFm8Jc9lJUYH; pinId=WLY0tQZjXWqudnuXPiqGtw; pin=jd_iTKwiyhqSPet; unick=L--%E7%8F%8D; ceshi3.com=000; _tp=IQqP9DOgcsJEFevFZ3Unng%3D%3D; _pst=jd_iTKwiyhqSPet; flash=3_cShAM7mdEkNlhsFrzmqlDG_6IWuy5J1Wfs_vrev3c8prp9uIsO4xY2Ng9_WMxIO3RdtkQhXVBR90z6mtBYgsPpcLhnhf5QvaL1H5xyoEXGiLcqdzEkxRVl1TBdDjMY3xb8Qw7d-D6Cug7tlIHXvTHITrO3279XPhMV1nFYpAitobpDnufKdc; source=PC; platform=pc; areaId=19; ipLoc-djd=19-1690-0-0; _gia_d=1; 3AB9D23F7A4B3CSS=jdd032OAU34ZBPAATYFPT5N6ROOVVQEIOD6WXX37YV2AMFT7RPLS7HWRE3NTVCNR6XUFPEPFU52LJRQTLDX2X2PYIMNVRAIAAAAMSFBVIEUAAAAAAD3F6WQCB4ILTX4X; __jda=150982071.17271720147572010223461.1727172015.1727172015.1727254915.2; __jdb=150982071.2.17271720147572010223461|2.1727254915; __jdc=150982071; 3AB9D23F7A4B3C9B=2OAU34ZBPAATYFPT5N6ROOVVQEIOD6WXX37YV2AMFT7RPLS7HWRE3NTVCNR6XUFPEPFU52LJRQTLDX2X2PYIMNVRAI; RT="z=1&dm=jd.com&si=4fezzs314c2&ss=m1hmze8u&sl=0&tt=0"
"""
cookie_string2 = """
__jdv=95931165|direct|-|none|-|1727172125185; __jdu=17271721251822082445218; wlfstk_smdl=ktogrp5t1m2wuqn3y13qk2oqphwap7va; TrackID=1jySPO4E7a_KKqwxfCGfLZzGNUwne94lN-ummVDrZ7PAOzJ5MsDeV-WDv6_-szzKyhSFsj7lEwyUI3gPcWHu8YyhSX6Avwwb4FNeGczjvg9A; thor=C8A3E939CEBF30DF5245823891C13577BBA383E0FFF50E56AAE468A22240F649B9EBC4717638E561F046E615F4B93AFE1E07D5ADB544ACC84B81D09E4B93B1972EFA0799B757C79081A7E3DAEAAD4C9C6CA97D639B8396751FB04667CA57E781BE244CEA0FC83332A4F96C9A4FC005D751ABA7544EEF0AF455E1F5D6518223287F98F0C2086307674480BB47021D7252; light_key=AASBKE7rOxgWQziEhC_QY6yanVPLz8x0Lv-dDNSeliX-iFQMtj8LGU4tKH_hctG1ksBllIJN; pinId=zIbf9x9WNKrVgNDvyOAxMw; pin=zhanggyn_m; unick=zhanggyn; ceshi3.com=000; _tp=ve5mLsQmXiO6uzmz7VFs9w%3D%3D; _pst=zhanggyn_m; source=PC; platform=pc; areaId=19; ipLoc-djd=19-1690-0-0; __jda=150982071.17271721251822082445218.1727172125.1727175951.1727255298.3; __jdb=150982071.2.17271721251822082445218|3.1727255298; __jdc=150982071; _gia_d=1; 3AB9D23F7A4B3CSS=jdd03DKPPNXZS4T4LHVMBBD4223Q2G4WHB7JE3AJ3KNJQLDXWQVUZPY5XGIAK6XSOHZ3ITGYOZQEVXJAYDMF53Y2KTOGR4EAAAAMSFBYHMWQAAAAACX4MZXVK3O3YXYX; flash=3_3plXdBxDpHVE43wet8SdLWjjlEABlKGdw1BkcpBUk7Li0PWHJviydo_sALSh2p0jQvYzx_2rq4XhVkXqa-Skv426oPmzlUBBRynFwAi1olvQsEohH3ue8FCf-vz3JlP7ZxGuv6Q_HPVzV856KuRSCoHk8VlzHmVhhascSIO6XAK-0e**; 3AB9D23F7A4B3C9B=DKPPNXZS4T4LHVMBBD4223Q2G4WHB7JE3AJ3KNJQLDXWQVUZPY5XGIAK6XSOHZ3ITGYOZQEVXJAYDMF53Y2KTOGR4E; RT="z=1&dm=jd.com&si=uexwlohx038&ss=m1hn7rn8&sl=0&tt=0"
"""

# 电脑谷歌浏览器位置
# google_pos = r'C:\Program Files\Google\Chrome\Application\chrome.exe'


current_directory = os.path.dirname(os.path.abspath(__file__))
# 获取当前时间戳，格式化为字符串，用作日志文件名的后缀
current_time_str = datetime.now().strftime('%Y-%m-%d_%H-%M-%S')
log_file_name = f"/output_{current_time_str}.log"  # 动态生成日志文件名
info_log_file_name = f"/output_{current_time_str}.info.log"  # 动态生成info日志文件名

class InfoFilter(logging.Filter):
    def filter(self, record):
        return record.levelno == logging.INFO

lock = asyncio.Lock()

# 创建日志器
logger = logging.getLogger('test')
logger.setLevel(logging.DEBUG)  # 仅记录 INFO 及以上级别的日志

# 创建控制台处理器
console_handler = logging.StreamHandler()
console_handler.setLevel(logging.INFO)  # 控制台只输出 INFO 级别的日志
console_handler.addFilter(InfoFilter())

# 创建文件处理器
file_handler = logging.FileHandler(current_directory + log_file_name, mode='a', encoding='utf-8')
file_handler.setLevel(logging.DEBUG)  # 记录所有日志

file_handler_info = logging.FileHandler(current_directory + info_log_file_name, mode='a', encoding='utf-8')
file_handler_info.setLevel(logging.INFO)  # 只记录 INFO 级别的日志
file_handler_info.addFilter(InfoFilter())

# 设置日志输出格式
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s', datefmt='%Y-%m-%d %H:%M:%S')
console_handler.setFormatter(formatter)
file_handler.setFormatter(formatter)
file_handler_info.setFormatter(formatter)

# 将处理器添加到日志器
logger.addHandler(console_handler)
logger.addHandler(file_handler)
logger.addHandler(file_handler_info)

# 定义一个自定义的 print 函数
async def info(*args, **kwargs):
    message = ' '.join(map(str, args))
    async with lock:
        logger.info(message)

async def error(*args, **kwargs):
    message = ' '.join(map(str, args))
    async with lock:
        logger.error(message)

async def debug(*args, **kwargs):
    message = ' '.join(map(str, args))
    async with lock:
        logger.debug(message)

# 读取Excel文件
excel_file = "./excel_file.xlsx"
df = pd.read_excel(excel_file)

# 检查并添加“运营竞拍代码”列
if '运营竞拍代码' not in df.columns:
    df['运营竞拍代码'] = ''

# 计算卖价方法
def calculate_selling_price(cost, signup_count):
    # 定义表格规则
    table = {
        (0, 100): [(3.9, 4.1), (4.0, 4.2), (4.1, 4.3), (4.2, 4.4), (4.3, 4.5)],
        (100, 300): [(3.4, 3.6), (3.5, 3.7), (3.6, 3.8), (3.7, 3.9), (3.8, 4.0)],
        (300, 500): [(3.2, 3.4), (3.3, 3.5), (3.4, 3.6), (3.5, 3.7), (3.6, 3.8)],
        (500, 800): [(2.9, 3.1), (3.0, 3.2), (3.1, 3.3), (3.2, 3.4), (3.3, 3.5)],
        (800, 1200): [(2.4, 2.6), (2.5, 2.7), (2.6, 2.8), (2.7, 2.9), (2.8, 3.0)],
        (1200, float('inf')): [(1.9, 2.1), (2.0, 2.2), (2.1, 2.3), (2.2, 2.4), (2.3, 2.5)]
    }
    # 确定成本区间
    cost_range = next(key for key in table if key[0] < cost <= key[1])

    # 确定报名人数区间
    if signup_count > 8:
        signup_index = 0
    elif 7 <= signup_count <= 8:
        signup_index = 1
    elif 5 <= signup_count <= 6:
        signup_index = 2
    elif 3 <= signup_count <= 4:
        signup_index = 3
    else:
        signup_index = 4

    # 获取对应的卖价区间
    price_range = table[cost_range][signup_index]

    # 如果是区间，随机取一个带一位小数的值
    if isinstance(price_range, tuple):
        random_multiplier = round(random.uniform(*price_range), 1)
    else:
        random_multiplier = price_range

    # 最终价格向上取整
    selling_price = math.ceil(cost * random_multiplier)

    return selling_price

# 计算目标价算法
def calculate_target_price(selling_price):
    # 定义目标价的倍数范围表格
    multiplier_table = {
        '>1200': (1.0, 1.0),
        '800~1200': (1.0, 1.0),
        '500~800': (1.0, 1.0),
        '300~500': (1.0, 1.0),
        '100~300': (1.0, 1.0),
        '≤100': (1.0, 1.0)
    }

    # 确定卖价的区间
    if selling_price > 1200:
        multiplier_range = multiplier_table['>1200']
    elif 800 <= selling_price <= 1200:
        multiplier_range = multiplier_table['800~1200']
    elif 500 <= selling_price <= 800:
        multiplier_range = multiplier_table['500~800']
    elif 300 <= selling_price <= 500:
        multiplier_range = multiplier_table['300~500']
    elif 100 <= selling_price <= 300:
        multiplier_range = multiplier_table['100~300']
    else:
        multiplier_range = multiplier_table['≤100']

    # 随机选择倍数并计算目标价
    random_multiplier = round(random.uniform(*multiplier_range), 1)
    target_price = math.ceil(selling_price * random_multiplier)

    return target_price

# 将 cookie 字符串解析为字典列表
def parse_cookie_string(cookie_string):
    cookies = []
    for item in cookie_string.split(';'):
        name, value = item.strip().split('=', 1)
        cookies.append({'name': name, 'value': value, 'domain': '.jd.com'})
    return cookies

# 得到自己商品id列表
def get_items_id_from_excel(file_path):
    df = pd.read_excel(file_path)
    items = []
    for _, row in df.iterrows():
        productId = row['商品ID']
        if '运营竞拍代码' in df.columns:
            if not pd.isna(row['运营竞拍代码']):
                items.append({
                    '商品ID': int(productId),
                    '商品标题': row['商品标题'],
                    '成本': row['成本'],
                    '卖价': row['卖价'],
                    '目标价': row['目标价'],
                    '运营竞拍代码': str(row['运营竞拍代码']).split(','),
                    'url': f"https://paimai.jd.com/{int(productId)}"
                })
            else:
                items.append({
                    '商品ID': int(productId),
                    '商品标题': row['商品标题'],
                    '成本': row['成本'],
                    '卖价': row['卖价'],
                    '目标价': row['目标价'],
                    '运营竞拍代码': [],
                    'url': f"https://paimai.jd.com/{int(productId)}"
                })
        else:
            items.append({
                '商品ID': int(productId),
                '商品标题': row['商品标题'],
                '成本': row['成本'],
                '卖价': row['卖价'],
                '目标价': row['目标价'],
                '运营竞拍代码': [],
                'url': f"https://paimai.jd.com/{int(productId)}"
            })
    return items

# 得到自己商品列表
def get_items_from_excel(file_path):
    df = pd.read_excel(file_path)
    items = []
    for _, row in df.iterrows():
        productId = row['商品ID']
        items.append({
            '商品ID': int(productId),
            '商品标题': row['商品标题'],
            '成本': row['成本'],
            '卖价': row['卖价'],
            '目标价': row['目标价'],
            '运营竞拍代码': str(row['运营竞拍代码']).split(','),  # 分割竞拍代码字符串
            'url': f"https://paimai.jd.com/{int(productId)}"
        })
        # 检查是否存在自定义卖价
        if not pd.isna(row['卖价']):
            stored_sale_ids.add(int(productId))
        # 检查是否存在自定义卖价和目标价
        if not pd.isna(row['目标价']):
            stored_target_ids.add(int(productId))
    return items

async def get_code(browser, item, cookie_string, retries=1):
    page = await browser.newPage()
    await page.setViewport({'width': 1920, 'height': 1080})

    # 设置 cookie
    cookies = parse_cookie_string(cookie_string)
    await page.setCookie(*cookies)

    try:
        try:
            # 设置最多等待 15 秒
            await page.goto(item['url'], timeout=15000)
        except Exception as e:
            await debug(f"打开 {item['url']} 页面超时15秒，继续执行后续操作...")

        # 防止网站检测
        await page.evaluate('''() =>{ Object.defineProperties(navigator,{ webdriver:{ get: () => false } }) }''')

        # 等待1秒等页面加载
        await asyncio.sleep(1)

        # 获取结束状态
        end_time = await page.evaluate('''() => {
            const endElement = document.querySelector('.endtime');
            return endElement ? endElement.innerText : null;
        }''')

        # 如果结束了则跳过此商品
        if end_time is not None:
            await page.close()
            await info(f"跳过商品：{item['商品标题']} - 该商品已结束")
            return False

        # 要先打开隐藏内容
        await page.click('div[class^="index_userDetail__viewAll"]')
        await asyncio.sleep(0.5)

        # 获取我的竞拍代码
        my_bid_code = await page.evaluate(r'''() => {
            const elements = document.querySelectorAll('div[class^="index_userDetail__subtitle"]');
            return elements[0] ? elements[0].textContent.match(/\d+/)[0] : null;
        }''')

        # 如果我的竞拍代码存在，检查全局字典，不存在代表未报名
        if my_bid_code:
            if item['商品ID'] not in bid_codes_dict:
                bid_codes_dict[item['商品ID']] = []  # 如果字典中还没有这个商品ID，初始化一个列表

            # 仅在当前竞拍代码数量少于2且列表中没有当前竞拍代码时添加新的竞拍代码
            if len(bid_codes_dict[item['商品ID']]) < 2:
                await debug('当前竞拍代码:', my_bid_code)
                if my_bid_code not in bid_codes_dict[item['商品ID']]:
                    bid_codes_dict[item['商品ID']].append(my_bid_code)
                # 写入excel
                row_index = df[df['商品ID'] == item['商品ID']].index
                # 将竞拍代码合并为逗号分隔的字符串
                auction_codes = ','.join(bid_codes_dict[item['商品ID']])
                df.loc[row_index, '运营竞拍代码'] = auction_codes
                df.to_excel(excel_file, index=False)
        else:
            await page.close()
            await info(f"跳过商品：{item['商品标题']} - 该商品未报名")
            return False

        await page.close()

    except Exception as e:
        if retries > 0:
            await error(f"获取竞拍代码方法：访问 {item['url']} 异常，正在重试...")
            await error(traceback.format_exc())
            await page.close()  # 关闭当前页面
            return await get_code(browser, item, cookie_string, retries - 1)
        else:
            await error(f"获取竞拍代码方法：访问 {item['url']} 失败，跳过此次访问。")
            await error(traceback.format_exc())
            await page.close()  # 关闭当前页面
            return False  # 页面访问失败，返回 False

async def visit_page(item, page, retries=1):
    try:
        try:
            # 设置最多等待 15 秒
            await page.goto(item['url'], timeout=15000)
        except Exception as e:
            await debug(f"打开 {item['url']} 页面超时15秒，继续执行后续操作...")

        # 防止网站检测
        await page.evaluate('''() =>{ Object.defineProperties(navigator,{ webdriver:{ get: () => false } }) }''')

        # 等待1秒等页面加载
        await asyncio.sleep(1)

        # 获取结束状态
        end_time = await page.evaluate('''() => {
            const endElement = document.querySelector('.endtime');
            return endElement ? endElement.innerText : null;
        }''')

        # 如果结束了则跳过此商品
        if end_time is not None:
            skipped_ids.add(item['商品ID'])
            await info(f"跳过商品：{item['商品标题']} - 该商品已结束")
            return 'False'

        # 获取当前价
        current_price = await page.evaluate('''() => {
            const priceElement = document.querySelector('.price.current .number em');
            return priceElement ? parseFloat(priceElement.innerText.replace(',', '').trim()) : null;
        }''')

        # 如果没有找到当前价格，意味着结束了则跳过此商品
        if current_price is None:
            if retries > 0:
                await error(f"获取当前价格失败，访问 {item['url']} 异常，正在重试...")
                await error(traceback.format_exc())
                return 'Retry'
            else:
                await error(f"获取当前价格失败，访问 {item['url']} 失败，跳过此次访问。")
                await error(traceback.format_exc())
                return 'False'  # 页面访问失败，返回 False

        # 获取当前最高价的竞拍代码
        highest_bid_code_text = await page.evaluate('''() => {
            const codeElement = document.querySelector('.smc ul li:first-child em:first-child')
            return codeElement ? codeElement.innerText.trim() : '';
        }''')

        highest_bid_code = re.sub(r'\D', '', highest_bid_code_text)

        # 如果没有最高价的竞拍代码，意味着无人出价，我们也不出
        if highest_bid_code == '' and need_skip:
            await info(f"跳过商品：{item['商品标题']} - 该商品无人出价")
            return 'False'

        # 获取加价幅度
        increment_text = await page.evaluate('''() => {
            const incrementElement = document.querySelector('.list.description ul li:nth-child(3) em');
            return incrementElement ? incrementElement.innerText.trim() : '';
        }''')
        match = re.search(r'[\d,]+', increment_text)
        increment_amount = int(match.group(0).replace(',', '')) if match else 20

        # 获取报名人数
        signups_text = await page.evaluate('''() => {
            const signupElement = document.querySelector('.times span:first-child em');
            return signupElement ? signupElement.innerText.trim() : '';
        }''')
        signups_count = int(signups_text) if signups_text else 0

        # 判断是否使用存储的卖价
        if item['商品ID'] in stored_sale_ids:
            sale_price = item['卖价']
        else:
            sale_price = calculate_selling_price(item['成本'], signups_count)
        # 判断是否使用存储的目标价
        if item['商品ID'] in stored_target_ids:
            target_price = item['目标价']
        else:
            target_price = calculate_target_price(sale_price)

        # 查找商品ID对应的行
        row_index = df[df['商品ID'] == item['商品ID']].index
        df.loc[row_index, '卖价'] = sale_price
        df.loc[row_index, '目标价'] = target_price

        flag = 'False'
        # 判断出价逻辑
        if current_price + increment_amount < sale_price or (current_price + increment_amount >= sale_price and current_price + increment_amount <= target_price and highest_bid_code in item['运营竞拍代码']):
            # 检查是否已经是由我出价
            my_bid_exists = await page.evaluate('''() => {
                return document.querySelector('.pm-myBidPrice') !== null;
            }''')
            if not my_bid_exists:
                # 获取出价金额
                bid_amount = await page.evaluate('''() => {
                    const valueElement = document.querySelector('.input-value')
                    return valueElement ? parseFloat(valueElement.value.replace(',', '').trim()) : null;
                }''')

                # 有出价金额说明报名了, 没有就要跳过
                if (bid_amount):
                    # 随机点击增价按钮
                    add_clicks = random.randint(min_clicks, max_clicks)
                    can_add_times = (sale_price - current_price - increment_amount) // increment_amount
                    add_clicks = int(min(add_clicks, max(can_add_times, 0)))
                    # 如果当前价格比卖价高，不加价
                    if current_price >= sale_price:
                        add_clicks = 0
                    for _ in range(add_clicks):
                        await info(f'正在加价：{_ + 1}/{add_clicks}次')
                        await page.click('.button-add')
                        await asyncio.sleep(0.5)  # 等待按钮点击生效

                    # 点击确认出价按钮
                    await page.click('.button.bid-button')
                    await asyncio.sleep(1)  # 等待弹窗出现

                    # 如果增加了价格，会有二次确认弹窗
                    if add_clicks > 0:
                        await page.click('.dialog-submit')
                        await asyncio.sleep(0.5)

                    await info(f"出价成功：{item['商品标题']}（{item['商品ID']}）")
                    await info(f"出价时间：{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
                    await info(f"出价金额：{bid_amount + increment_amount * add_clicks}")
                    await info(f"卖价：{sale_price}")
                    await info(f"目标价：{target_price}")

                    flag = 'True'  # 出价成功，返回 True
                else:
                    await info(f"跳过商品：{item['商品标题']} - 该商品未报名")
            else:
                await info(f"跳过商品：{item['商品标题']} - 该商品最新出价是自己")
        else:
            skipped_ids.add(item['商品ID'])
            df.to_excel(excel_file, index=False)
            await info(f"跳过商品：{item['商品标题']} - 该商品已达标，加入完成库")
            await info(f"当前价：{current_price}")
            await info(f"卖价：{sale_price}")
            await info(f"目标价：{target_price}")

        return flag # 未出价，返回False

    except Exception as e:
        if retries > 0:
            await error(f"Warning出价方法：访问 {item['url']} 异常，正在重试...")
            await error(traceback.format_exc())
            return 'Retry'
        else:
            await error(f"Failed出价方法：访问 {item['url']} 失败，跳过此次访问。")
            await error(traceback.format_exc())
            return 'False'  # 页面访问失败，返回 False


async def main_task():
    default_user_agent = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'

    browser = await launch({
        # 'executablePath': google_pos,
        'dumpio': False,
        'args': [
            '--no-sandbox',
            '--lang=zh-CN,zh,en',
            '--disable-gpu',
            '--disable-software-rasterizer',
            '--disable-webrtc',
            '--blink-settings=imagesEnabled=true',
            '--start-maximized',
            '--ignore-certificate-errors',
            '--useragent={}'.format(default_user_agent),
            '--disable-blink-features=AutomationControlled',
            '--excludeSwitches=enable-automation',
            '--disable-logging',
            '--log-level=3',
        ]
    },
        headless=True,
        autoClose=False,
        solMo=500  # 所有浏览器操作延迟500ms
    )

    # 各个id对应的运营竞拍代码数组
    global bid_codes_dict
    bid_codes_dict = {}
    # 需要跳过的id
    global skipped_ids
    skipped_ids = set()
    # 不需要计算卖价的id
    global stored_sale_ids
    stored_sale_ids = set()
    # 不需要计算目标价的id
    global stored_target_ids
    stored_target_ids = set()
    global need_skip
    global min_clicks
    global max_clicks

    # 以下是可以动态设置的全局值 #

    # 是否需要跳过未出价的商品
    need_skip = False
    # 随机加价最小次数
    min_clicks = 0
    # 随机加价最大次数
    max_clicks = 10
    # 期望完成一轮的最小时间
    min_round = 0
    # 期望完成一轮的最大时间
    max_round = 0
    # 遇到异常的重试次数
    retry_times = 2
    # 最大等待执行时间
    timeout = 60

    # 先写入竞拍代码
    id_s = get_items_id_from_excel(excel_file)
    for cookie_string in [cookie_string1, cookie_string2]:
        if not cookie_string.strip():
            continue  # 跳过空的cookie字符串
        for i, item in enumerate(id_s):
            await info('-----------------------------------------------------')
            await info(f'写入竞拍代码{i + 1}/{len(id_s)}')
            # 没有竞拍代码才进去
            if len(item['运营竞拍代码']) == 0:
                await get_code(browser, item, cookie_string, 1)

    items = get_items_from_excel(excel_file)
    # 当所有items中都有竞拍代码时才继续
    is_continue = True
    for i, item in enumerate(items):
        if len(item['运营竞拍代码']) == 0:
            is_continue = False
            break

    if is_continue:
        all_above_target = False
        await info(f'全部满足目标？{all_above_target}')
        while not all_above_target:
            y = len(items) - len(skipped_ids)
            await info('剩余', y)
            # 计算 x 的下限
            lower_bound = (min_round / y) - 2
            # 计算 x 的上限
            upper_bound = (max_round / y) - 2
            # x 的取值范围
            x_min = int(lower_bound) if lower_bound == int(lower_bound) else int(lower_bound) + 1
            x_min = max(x_min, 0)
            x_max = int(upper_bound) - 1
            x_max = max(x_max, 0)

            for cookie_string in [cookie_string1, cookie_string2]:
                if not cookie_string.strip():
                    await info(f"{'cookie1是空的' if cookie_string == cookie_string1 else 'cookie2是空的'}")
                    continue  # 跳过空的cookie字符串

                await info(f"{'当前循环cookie1' if cookie_string == cookie_string1 else '当前循环cookie2'}")
                all_above_target = True
                for i, item in enumerate(items):
                    await info('-----------------------------------------------------')
                    if item['商品ID'] in skipped_ids:
                        await info(f"跳过商品：{item['商品标题']}（{item['商品ID']}）")
                        continue

                    # 下一个item
                    next_index = (i + 1) % len(items)
                    next_item = items[next_index]

                    for cur in range(retry_times + 1):
                        page = await browser.newPage()
                        await page.setViewport({'width': 1920, 'height': 1080})
                        # 设置 cookie
                        cookies = parse_cookie_string(cookie_string)
                        await page.setCookie(*cookies)

                        try:
                            bid_successful = await asyncio.wait_for(visit_page(item, page, retry_times - cur), timeout)
                            if bid_successful == 'True':
                                # 根据剩余数量及期望一轮完成时间动态生成随机等待值
                                countdown = random.randint(min(x_min, x_max), max(x_min, x_max))
                                await info(f"即将进行下一个商品：倒计时：{countdown}秒")
                                await asyncio.sleep(countdown)
                                break
                            if bid_successful == 'False':
                                break
                            if bid_successful == 'Retry' and cur == retry_times:
                                await info(f"{item['商品ID']}执行两次失败")
                        except asyncio.TimeoutError:
                            if cur == retry_times:
                                await error(f"{item['商品ID']}执行失败，操作超时")
                            else:
                                await error(f"{item['商品ID']}操作超时，重试一次")
                        except Exception as e:
                            if cur == retry_times:
                                await error(f"{item['商品ID']}执行失败")
                            await error(f"{item['商品ID']}程序异常:{traceback.format_exc()}")
                        finally:
                            await page.close()

                    if not all_above_target:
                        break
                else:
                    all_above_target = len(items) == len(skipped_ids)
                if all_above_target:
                    break

        await browser.close()
        await info('都已达标')
        df.to_excel(excel_file, index=False)
    else:
        await info('有竞拍代码未获取到，不进行出价环节')
        await browser.close()

if __name__ == '__main__':
    asyncio.run(main_task())
