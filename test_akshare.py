#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Akshare 框架测试脚本 by liziang
用于测试akshare库的基本功能
"""

import akshare as ak
import pandas as pd
from datetime import datetime, timedelta


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
    print("\n" + "=" * 50)
    print("测试3: 获取股票实时行情")
    print("=" * 50)

    try:
        # 获取实时行情（单只股票）
        stock_zh_a_spot_em = ak.stock_zh_a_spot_em()
        print(f"获取到 {len(stock_zh_a_spot_em)} 只股票实时行情")
        print(stock_zh_a_spot_em.head(10)[['代码', '名称', '最新价', '涨跌幅']])
    except Exception as e:
        print(f"获取实时行情失败: {e}")


def test_stock_fund_flow():
    """测试资金流向"""
    print("\n" + "=" * 50)
    print("测试4: 获取资金流向")
    print("=" * 50)

    try:
        # 获取今日资金流向
        stock_fund_flow_statistics_df = ak.stock_fund_flow_statistics(symbol="今日")
        print(f"获取到 {len(stock_fund_flow_statistics_df)} 条记录")
        print(stock_fund_flow_statistics_df.head(10)[['代码', '名称', '主力净流入-净额']])
    except Exception as e:
        print(f"获取资金流向失败: {e}")


def test_stock_zt_pool():
    """测试涨停板数据"""
    print("\n" + "=" * 50)
    print("测试5: 获取涨停板数据")
    print("=" * 50)

    try:
        # 获取今日涨停板
        stock_zt_pool_em_df = ak.stock_zt_pool_em(date=datetime.now().strftime("%Y%m%d"))
        print(f"获取到 {len(stock_zt_pool_em_df)} 只涨停股票")
        if len(stock_zt_pool_em_df) > 0:
            print(stock_zt_pool_em_df[['代码', '名称', '涨跌幅', '涨停原因']].head(10))
    except Exception as e:
        print(f"获取涨停板数据失败: {e}")


def test_index_info():
    """测试指数信息"""
    print("\n" + "=" * 50)
    print("测试6: 获取指数列表")
    print("=" * 50)

    try:
        # 获取主要指数列表
        index_stock_cons_sina_df = ak.index_stock_cons_sina(symbol="上证指数")
        print(f"获取到 {len(index_stock_cons_sina_df)} 只成分股")
        print(index_stock_cons_sina_df.head(10))
    except Exception as e:
        print(f"获取指数信息失败: {e}")


def test_stock_industry():
    """测试行业板块"""
    print("\n" + "=" * 50)
    print("测试7: 获取行业板块")
    print("=" * 50)

    try:
        # 获取行业板块行情
        stock_board_industry_name_em_df = ak.stock_board_industry_name_em()
        print(f"获取到 {len(stock_board_industry_name_em_df)} 个行业板块")
        print(stock_board_industry_name_em_df.head(10))
    except Exception as e:
        print(f"获取行业板块失败: {e}")


def test_version():
    """测试akshare版本"""
    print("=" * 50)
    print("Akshare 版本信息")
    print("=" * 50)
    print(f"Akshare 版本: {ak.__version__}")
    print(f"Pandas 版本: {pd.__version__}")


def main():
    """主函数"""
    print("\n" + "=" * 50)
    print("Akshare 框架测试")
    print("=" * 50)

    # 测试版本信息
    test_version()

    # 测试各项功能
    test_stock_info()
    test_stock_daily()
    test_stock_realtime()
    test_stock_fund_flow()
    test_stock_zt_pool()
    test_index_info()
    test_stock_industry()

    print("\n" + "=" * 50)
    print("测试完成!")
    print("=" * 50)


if __name__ == "__main__":
    main()
