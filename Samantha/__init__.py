


# your_project/other_path/__init__.py

from .consolidated_function import filter_stocks  # 導入選股函數

from .consolidated_function import filter_top_10_dividend_stocks

__all__ = ['filter_stocks']  # 定義公共接口
__all__ = ['filter_top_10_dividend_stocks']  # 定義公共接口