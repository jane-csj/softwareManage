def square_dynamics():
    """
    广场动态功能，展示广场通知消息和互联网询价信息。
    输入参数：无
    输出结果：打印广场动态信息。
    """
    print("广场动态：")
    print("1. 广场通知消息：")
    print("   - 通知1：...")
    print("   - 通知2：...")
    print("2. 互联网询价信息：")
    print("   - 询价1：...")
    print("   - 询价2：...")
    return "广场动态信息展示完成。"


def filter_assets(assets, filters):
    """根据给定的筛选条件筛选资产。"""
    filtered = []
    for asset in assets:
        if all(asset.get(key) == value for key, value in filters.items()):
            filtered.append(asset)
    return filtered


def sort_assets(assets, sort_key, reverse=False):
    """根据指定的键对资产列表进行排序。"""
    return sorted(assets, key=lambda x: x[sort_key], reverse=reverse)


def idle_asset_display(asset_category, filters=None, sort_by=None, reverse=False):
    """
    闲置资产展示功能，按照资产分类展示闲置资产信息。
    输入参数：
    - asset_category: 资产分类，用于筛选特定分类的资产。
    - filters: 筛选条件字典。
    - sort_by: 排序字段。
    - reverse: 是否反向排序，默认为False。
    输出结果：打印筛选后的资产信息。
    """
    print(f"展示分类 '{asset_category}' 的闲置资产信息：")
    # 假设的资产数据
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


def asset_search(search_query):
    """
    资产检索功能，根据查询条件检索闲置资产。
    输入参数：
    - search_query: 查询条件，用于检索资产。
    输出结果：打印检索到的资产信息。
    """
    print(f"检索 '{search_query}' 相关的资产：")
    # 假设的资产数据
    idle_assets = [
        {'id': 'E001', 'name': '电脑', 'category': '电子设备'},
        {'id': 'F001', 'name': '办公桌', 'category': '办公家具'}
    ]
    found = False
    for asset in idle_assets:
        if search_query in asset['name']:
            print(f"资产ID：{asset['id']}, 名称：{asset['name']}, 分类：{asset['category']}")
            found = True
    if not found:
        print("未找到相关资产。")
    return f"'{search_query}' 的资产检索结果展示完成。"


def asset_check_out(asset_id, user_unit, time, quantity):
    """
    资产领用功能，领用闲置资产。
    输入参数：
    - asset_id: 资产ID，用于标识具体的资产。
    - user_unit: 领用单位。
    - time: 领用时间。
    - quantity: 领用数量。
    输出结果：返回领用结果。
    """
    result = f"资产ID {asset_id} 被 {user_unit} 于 {time} 领用，数量 {quantity}。"
    print(result)
    return result


def asset_return(asset_id, user_unit, time, quantity):
    """
    资产归还功能，归还闲置资产。
    输入参数：
    - asset_id: 资产ID，用于标识具体的资产。
    - user_unit: 归还单位。
    - time: 归还时间。
    - quantity: 归还数量。
    输出结果：返回归还结果。
    """
    result = f"资产ID {asset_id} 被 {user_unit} 于 {time} 归还，数量 {quantity}。"
    print(result)
    return result


def asset_profile(asset_id):
    """
    资产画像功能，展示闲置资产的详细信息。
    输入参数：
    - asset_id: 资产ID，用于标识具体的资产。
    输出结果：打印资产的详细信息。
    """
    print(f"展示资产ID {asset_id} 的画像信息：")
    # 假设的资产数据
    asset_details = {
        'E001': {'name': '电脑', 'category': '电子设备', 'usage_info': '...', 'life_cycle': '...', 'base_info': '...',
                 'repair_records': '...', 'disposal_status': '...', 'inventory_records': '...'}
    }
    if asset_id in asset_details:
        details = asset_details[asset_id]
        print(
            f"名称：{details['name']}, 分类：{details['category']}, 使用信息：{details['usage_info']}, 生命周期：{details['life_cycle']}, 基础信息：{details['base_info']}, 维修记录：{details['repair_records']}, 处置情况：{details['disposal_status']}, 盘点记录：{details['inventory_records']}")
    else:
        print("未找到指定资产的详细信息。")
    return f"资产ID {asset_id} 的画像信息展示完成。"


# 闲置资产管理功能

def asset_check_in(asset_id, quantity):
    """
    资产入库功能，对单位的闲置资产进行入库登记。
    输入参数：
    - asset_id: 资产ID，用于标识具体的资产。
    - quantity: 入库数量。
    输出结果：返回入库结果。
    """
    result = f"资产ID {asset_id} 入库数量 {quantity}。"
    print(result)
    return result


def use_registration(asset_id, user_unit):
    """
    领用登记功能，执法单位对本单位的闲置资产进行登记备案。
    输入参数：
    - asset_id: 资产ID，用于标识具体的资产。
    - user_unit: 使用单位。
    输出结果：返回登记结果。
    """
    result = f"资产ID {asset_id} 被 {user_unit} 登记备案。"
    print(result)
    return result


def asset_approval(asset_id, action):
    """
    资产审批功能，对闲置资产入库、领用、维修、盘点进行审批。
    输入参数：
    - asset_id: 资产ID，用于标识具体的资产。
    - action: 审批操作，如'check_in', 'check_out', 'repair', 'inventory'。
    输出结果：返回审批结果。
    """
    result = f"资产ID {asset_id} 的 {action} 操作已审批。"
    print(result)
    return result


def asset_rent(asset_id, requesting_unit, quantity, rental_period):
    """
    资产租借功能，租借资产并生成租借单据。
    输入参数：
    - asset_id: 资产ID，用于标识具体的资产。
    - requesting_unit: 申请单位。
    - quantity: 租借数量。
    - rental_period: 租借周期。
    输出结果：返回租借结果。
    """
    result = f"资产ID {asset_id} 被 {requesting_unit} 租借，数量 {quantity}，租借周期 {rental_period}。"
    print(result)
    return result


def asset_inventory(inventory_type, asset_id, inventory_time, description, inventory_staff):
    """
    资产盘点功能，进行定期或临时盘点。
    输入参数：
    - inventory_type: 盘点类型，'regular' 或 'temporary'。
    - asset_id: 资产ID，用于标识具体的资产。
    - inventory_time: 盘点时间。
    - description: 盘点情况说明。
    - inventory_staff: 盘点人员。
    输出结果：返回盘点结果。
    """
    result = f"{inventory_type} 盘点：资产ID {asset_id}，时间 {inventory_time}，说明 {description}，盘点人员 {inventory_staff}。"
    print(result)
    return result


# 测试函数
if __name__ == "__main__":
    try:
        # 公物仓广场功能测试
        square_dynamics()
        idle_asset_display('电子设备')
        asset_search('电脑')
        asset_check_out('E001', '单位A', '2023-12-01', 2)
        asset_return('E001', '单位A', '2023-12-15', 2)
        asset_profile('E001')

        # 闲置资产管理功能测试
        asset_check_in('E001', 10)
        use_registration('E001', '单位B')
        asset_approval('E001', 'check_in')
        asset_rent('E001', '单位C', 5, '1个月')
        asset_inventory('regular', 'E001', '2023-12-01', '定期盘点', '张三')
    except Exception as e:
        print(f"发生错误: {e}")