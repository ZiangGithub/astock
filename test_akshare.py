#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Akshare 框架测试脚本
用于测试akshare库的基本功能
包含防反爬机制：延迟+重试
"""

import akshare as ak
import pandas as pd
import time
import random
from datetime import datetime, timedelta

# 防反爬配置
REQUEST_DELAY_MIN = 3  # 最小请求间隔（秒）
REQUEST_DELAY_MAX = 8  # 最大请求间隔（秒）
MAX_RETRIES = 3        # 最大重试次数
RETRY_DELAY_MIN = 5    # 重试最小间隔（秒）
RETRY_DELAY_MAX = 10   # 重试最大间隔（秒）


def random_delay():
    """随机延迟，防止反爬"""
    delay = random.uniform(REQUEST_DELAY_MIN, REQUEST_DELAY_MAX)
    print(f"  [延迟 {delay:.1f}秒...]")
    time.sleep(delay)


def robust_request(func, *args, max_retries=MAX_RETRIES, **kwargs):
    """
    带重试机制的请求包装器
    用于处理反爬导致的连接中断
    """
    for attempt in range(max_retries):
        try:
            return func(*args, **kwargs)
        except Exception as e:
            error_msg = str(e)
            # 检查是否是反爬相关错误
            is_anti_crawl = any(keyword in error_msg for keyword in [
                "Connection aborted",
                "RemoteDisconnected",
                "Connection reset",
                "timed out"
            ])

            if is_anti_crawl and attempt < max_retries - 1:
                retry_delay = random.uniform(RETRY_DELAY_MIN, RETRY_DELAY_MAX)
                print(f"  [反爬触发，第{attempt + 1}次重试，{retry_delay:.1f}秒后重试...]")
                time.sleep(retry_delay)
                continue
            else:
                raise


def test_stock_info():
    """测试股票基本信息获取"""
    print("=" * 50)
    print("测试1: 获取A股股票列表")
    print("=" * 50)

    try:
        # 获取A股股票列表
        stock_info_a_code_name_df = ak.stock_info_a_code_name()
        print(f"获取到 {len(stock_info_a_code_name_df)} 只股票")
        print(stock_info_a_code_name_df.head(10))
    except Exception as e:
        print(f"获取股票列表失败: {e}")


def test_stock_daily():
    """测试股票日线数据获取"""
    random_delay()  # 防反爬延迟
    print("\n" + "=" * 50)
    print("测试2: 获取股票日线数据")
    print("=" * 50)

    try:
        # 获取上证指数日线数据
        stock_zh_index_daily_df = ak.stock_zh_index_daily(symbol="sh000001")
        print(f"获取到 {len(stock_zh_index_daily_df)} 条记录")
        print(stock_zh_index_daily_df.tail(5))
    except Exception as e:
        print(f"获取日线数据失败: {e}")


def test_stock_realtime():
    """测试股票实时行情"""
    random_delay()
    print("\n" + "=" * 50)
    print("测试3: 获取股票实时行情")
    print("=" * 50)

    try:
        # 使用重试机制获取实时行情
        stock_zh_a_spot_em = robust_request(ak.stock_zh_a_spot_em)
        print(f"获取到 {len(stock_zh_a_spot_em)} 只股票实时行情")
        # 选择存在的列
        cols = [c for c in ['代码', '名称', '最新价', '涨跌幅', '代码-市场'] if c in stock_zh_a_spot_em.columns]
        print(stock_zh_a_spot_em[cols].head(10))
    except Exception as e:
        print(f"获取实时行情失败: {e}")


def test_stock_fund_flow():
    """测试资金流向"""
    random_delay()
    print("\n" + "=" * 50)
    print("测试4: 获取个股资金流向")
    print("=" * 50)

    try:
        # 使用重试机制获取个股资金流向 (平安银行)
        stock_fund_flow = robust_request(ak.stock_individual_fund_flow, stock="000001", market="sz")
        print(f"获取到 {len(stock_fund_flow)} 条记录")
        print(stock_fund_flow.head(10))
    except Exception as e:
        print(f"获取资金流向失败: {e}")


def test_stock_zt_pool():
    """测试涨停板数据"""
    random_delay()
    print("\n" + "=" * 50)
    print("测试5: 获取涨停板数据")
    print("=" * 50)

    try:
        # 获取最近一个交易日的数据
        # 计算上一个交易日（跳过周末）
        today = datetime.now()
        for i in range(1, 8):
            prev_day = today - timedelta(days=i)
            if prev_day.weekday() < 5:  # 0-4 是周一到周五
                trade_date = prev_day.strftime("%Y%m%d")
                break

        stock_zt_pool_em_df = robust_request(ak.stock_zt_pool_em, date=trade_date)
        print(f"获取到 {len(stock_zt_pool_em_df)} 只涨停股票")
        if len(stock_zt_pool_em_df) > 0:
            cols = [c for c in ['代码', '名称', '涨跌幅', '连板数', '首次封板时间'] if c in stock_zt_pool_em_df.columns]
            print(stock_zt_pool_em_df[cols].head(10))
    except Exception as e:
        print(f"获取涨停板数据失败: {e}")


def test_stock_market_fund_flow():
    """测试市场资金流向"""
    random_delay()
    print("\n" + "=" * 50)
    print("测试6: 获取市场资金流向")
    print("=" * 50)

    try:
        # 使用重试机制获取市场资金流向
        stock_market_fund_flow = robust_request(ak.stock_market_fund_flow)
        print(f"获取到 {len(stock_market_fund_flow)} 条记录")
        print(stock_market_fund_flow.head(10))
    except Exception as e:
        print(f"获取市场资金流向失败: {e}")


def test_index_info():
    """测试指数信息"""
    random_delay()
    print("\n" + "=" * 50)
    print("测试7: 获取指数日线数据")
    print("=" * 50)

    try:
        # 获取上证指数日线数据
        stock_zh_index_daily_df = ak.stock_zh_index_daily(symbol="sh000001")
        print(f"上证指数最新数据:")
        print(stock_zh_index_daily_df.tail(3))
    except Exception as e:
        print(f"获取指数信息失败: {e}")


def test_stock_industry():
    """测试行业板块"""
    random_delay()
    print("\n" + "=" * 50)
    print("测试8: 获取行业板块涨跌")
    print("=" * 50)

    try:
        # 使用重试机制获取行业板块行情
        stock_board_industry_name_em_df = robust_request(ak.stock_board_industry_name_em)
        print(f"获取到 {len(stock_board_industry_name_em_df)} 个行业板块")
        print(stock_board_industry_name_em_df.head(10)[['板块名称', '涨跌幅', '总市值']])
    except Exception as e:
        print(f"获取行业板块失败: {e}")


def test_stock_concept():
    """测试概念板块"""
    random_delay()
    print("\n" + "=" * 50)
    print("测试9: 获取概念板块涨跌")
    print("=" * 50)

    try:
        # 使用重试机制获取概念板块行情
        stock_board_concept_name_em_df = robust_request(ak.stock_board_concept_name_em)
        print(f"获取到 {len(stock_board_concept_name_em_df)} 个概念板块")
        print(stock_board_concept_name_em_df.head(10)[['板块名称', '涨跌幅', '总市值']])
    except Exception as e:
        print(f"获取概念板块失败: {e}")


def test_stock_kline():
    """测试个股K线数据"""
    random_delay()
    print("\n" + "=" * 50)
    print("测试10: 获取个股K线数据")
    print("=" * 50)

    try:
        # 使用重试机制获取个股K线数据 (平安银行)
        stock_zh_a_hist_df = robust_request(
            ak.stock_zh_a_hist,
            symbol="000001",
            period="daily",
            start_date="20250201",
            end_date="20250228"
        )
        print(f"获取到 {len(stock_zh_a_hist_df)} 条记录")
        print(stock_zh_a_hist_df.tail(5))
    except Exception as e:
        print(f"获取K线数据失败: {e}")


def test_version():
    """测试akshare版本"""
    print("=" * 50)
    print("Akshare 版本信息")
    print("=" * 50)
    print(f"Akshare 版本: {ak.__version__}")
    print(f"Pandas 版本: {pd.__version__}")


def is_trading_day():
    """检查今天是否是交易日"""
    now = datetime.now()
    # 周一到周五，且不是节假日（简单判断）
    if now.weekday() < 5:
        return True
    return False


def get_latest_trade_date():
    """获取最近的交易日"""
    today = datetime.now()
    for i in range(0, 8):
        check_day = today - timedelta(days=i)
        if check_day.weekday() < 5:
            return check_day.strftime("%Y-%m-%d")
    return None


def main():
    """主函数"""
    print("\n" + "=" * 50)
    print("Akshare 框架测试 (防反爬版)")
    print("=" * 50)

    # 显示交易日信息
    trade_date = get_latest_trade_date()
    is_trade = is_trading_day()
    print(f"最近交易日: {trade_date}")
    print(f"今天是否交易: {'是' if is_trade else '否'}")
    print(f"请求间隔: {REQUEST_DELAY_MIN}-{REQUEST_DELAY_MAX}秒")
    print(f"最大重试次数: {MAX_RETRIES}")

    # 测试版本信息
    test_version()

    # 测试各项功能
    test_stock_info()
    test_stock_daily()
    test_stock_realtime()
    test_stock_fund_flow()
    test_stock_zt_pool()
    test_stock_market_fund_flow()
    test_index_info()
    test_stock_industry()
    test_stock_concept()
    test_stock_kline()

    print("\n" + "=" * 50)
    print("测试完成!")
    print("=" * 50)


if __name__ == "__main__":
    main()
