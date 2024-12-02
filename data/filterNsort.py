def filter_assets(assets, filters):
    """
    根据给定的筛选条件筛选资产。
    输入参数：
    - assets: 资产列表。
    - filters: 筛选条件字典。
    输出结果：筛选后的资产列表。
    """
    filtered = []
    for asset in assets:
        if all(asset.get(key) == value for key, value in filters.items()):
            filtered.append(asset)
    return filtered


def sort_assets(assets, sort_key, reverse=False):
    """
    根据指定的键对资产列表进行排序。
    输入参数：
    - assets: 资产列表。
    - sort_key: 排序键。
    - reverse: 是否反向排序，默认为False。
    输出结果：排序后的资产列表。
    """
    return sorted(assets, key=lambda x: x[sort_key], reverse=reverse)


# 更新idle_asset_display以支持筛选和排序
def idle_asset_display(asset_category, filters=None, sort_by=None, reverse=False):
    # 原始闲置资产数据
    idle_assets = {
        '电子设备': [{'id': 'E001', 'name': '电脑', 'details': '...', 'traceability': '...'}],
        '办公家具': [{'id': 'F001', 'name': '办公桌', 'details': '...', 'traceability': '...'}]
    }

    if asset_category in idle_assets:
        assets = idle_assets[asset_category]
        if filters:
            assets = filter_assets(assets, filters)
        if sort_by:
            assets = sort_assets(assets, sort_by, reverse)

        for asset in assets:
            print(f"资产ID：{asset['id']}, 名称：{asset['name']}, 详情：{asset['details']}, 溯源：{asset['traceability']}")
    else:
        print("未找到指定分类的资产。")
    return f"分类 '{asset_category}' 的闲置资产信息展示完成。"


# 测试新增功能
if __name__ == "__main__":
    # 使用筛选和排序功能
    idle_asset_display('电子设备', {'name': '电脑'}, 'id', True)