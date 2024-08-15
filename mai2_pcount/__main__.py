from nonebot import on_command, on_endswith, on_regex
from nonebot.adapters.onebot.v11 import Bot, Event, GroupMessageEvent, Message, MessageEvent
from nonebot.typing import T_State
from nonebot.params import CommandArg, Endswith, RegexMatched

import json
import os
from datetime import datetime

# 定义数据目录
DATA_DIR = './data/mai2_pcount/'

# 创建数据目录
if not os.path.exists(DATA_DIR):
    os.makedirs(DATA_DIR)

def load_data(group_id):
    data_file = os.path.join(DATA_DIR, f"{group_id}.json")
    if os.path.exists(data_file):
        with open(data_file, 'r', encoding='utf-8') as f:
            return json.load(f)
    return {"enabled": False}

def save_data(group_id, data):
    data_file = os.path.join(DATA_DIR, f"{group_id}.json")
    with open(data_file, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=4)

def is_plugin_enabled(data):
    return data.get("enabled", False)

# 开启插件功能
pcount_on = on_command(
    "pcount on", 
    aliases={"开启pcount","开启pcount插件"},
    priority=100, 
    block=True
)

@pcount_on.handle()
async def handle_pcount_on(bot: Bot, event: Event, state: T_State):
    group_id = str(event.group_id)
    data = load_data(group_id)
    if not is_plugin_enabled(data):
        data["enabled"] = True
        save_data(group_id, data)
        await pcount_on.finish("插件功能已开启，数据文件已初始化")
    else:
        await pcount_on.finish("插件功能已开启，数据文件已存在")

# 关闭插件功能
pcount_off = on_command(
    "pcount off", 
    aliases={"关闭pcount","关闭pcount插件"},
    priority=100, 
    block=True
)

@pcount_off.handle()
async def handle_pcount_off(bot: Bot, event: Event, state: T_State):
    group_id = str(event.group_id)
    data = load_data(group_id)
    if is_plugin_enabled(data):
        data["enabled"] = False
        save_data(group_id, data)
        await pcount_off.finish("插件功能已关闭")
    else:
        await pcount_off.finish("插件功能已经是关闭状态")

def check_plugin_status(data, event):
    if not is_plugin_enabled(data):
        return f"插件功能未开启，无法执行指令"
    return None

# 帮助
help = on_command(
    "mai2_pcount_help",
    aliases={"舞萌机厅人数帮助","pcounthelp","mphelp","mmphelp"},
    priority=100,
    block=True
)

@help.handle()
async def handle_help(event: Event):
    help_message = (
        "舞萌 DX 线上机厅人数查询、修改帮助\n"
        "① pcount on: 在本群开启这个插件~不开启的话，下面的指令（除了关闭）都用不了唔~\n"
        "② pcount off: 在本群关闭这个插件~\n"
        "③ 添加机厅: 使用 '添加机厅 机厅名 机厅代号' 来添加哦~\n"
        "④ 删除机厅: 使用 '删除机厅 机厅代号' 来删除哦~\n"
        "⑤ [机厅代号]+ - =[数字]: 使用类似于 'mw=6' 的指令来修改机厅人数哦~\n"
        "⑥ [机厅代号]几: 使用类似于 'mw几' 的指令来查询机厅人数哦~\n"
        "⑦ 修改地区名 [地区名]: 使用类似于 '修改地区名 wmc聚集地' 的指令来修改地区名哦~\n"
        "注意注意~！各个群聊的数据都是不一样的，需要自行配置机厅哦~\n"
        "有问题可以致电Miaowing，我会竭尽全力帮助您解决问题哒！"
    )
    await help.finish(help_message)

# 添加机厅
add_hall = on_command(
    "添加机厅", 
    aliases={"addjt"},
    priority=100, 
    block=True
)

@add_hall.handle()
async def handle_add_hall(bot: Bot, event: Event, state: T_State, args: Message = CommandArg()):
    group_id = str(event.group_id)
    data = load_data(group_id)
    status_message = check_plugin_status(data, event)
    if status_message:
        return
        
    try:
        hall_name, hall_id = args.extract_plain_text().split()
        hall_id = hall_id.strip()
        if hall_id not in data:
            data[hall_id] = {"name": hall_name, "count": 0}
            save_data(group_id, data)
            await add_hall.finish(f"机厅 {hall_name} ({hall_id}) 已添加")
        else:
            await add_hall.finish(f"机厅 {hall_id} 已存在")
    except ValueError:
        await add_hall.finish("输入格式错误，请使用 `添加机厅 机厅名 机厅代号`")

# 删除机厅
remove_hall = on_command(
    "删除机厅", 
    aliases={"removejt","移除机厅"},
    priority=100, 
    block=True
)

@remove_hall.handle()
async def handle_remove_hall(bot: Bot, event: Event, state: T_State, args: Message = CommandArg()):
    group_id = str(event.group_id)
    data = load_data(group_id)
    status_message = check_plugin_status(data, event)
    if status_message:
        return
    
    hall_id = args.extract_plain_text().strip()
    
    if hall_id in data:
        del data[hall_id]
        save_data(group_id, data)
        await remove_hall.finish(f"机厅 {hall_id} 已删除")
    else:
        await remove_hall.finish(f"机厅 {hall_id} 不存在")

# 修改人数
edit_count = on_regex(
    r'([a-zA-Z]+)([+-=])(\d+)', 
    priority=100,
    block=True
)

@edit_count.handle()
async def handle_edit_count(event: Event, match = RegexMatched()):
    group_id = str(event.group_id)
    data = load_data(group_id)
    status_message = check_plugin_status(data, event)
    if status_message:
        return
        
    user_name = event.sender.card or event.sender.nickname
    hall_id = match.group(1).strip()
    operation = match.group(2)
    count_delta = int(match.group(3))

    if hall_id not in data:
        return
    
    current_time = datetime.now().strftime("%H:%M")

    if operation == "+":
        data[hall_id]["count"] += count_delta
    elif operation == "-":
        if data[hall_id]["count"] - count_delta < 0:
            await edit_count.finish(f"操作失败，人数不能小于0哦~\n当前 {data[hall_id]['name']} 共有 {data[hall_id]['count']} 人")
            return
        data[hall_id]["count"] -= count_delta
    elif operation == "=":
        if count_delta < 0:
            await edit_count.finish("修改失败，人数不能小于0哦~")
            return
        data[hall_id]["count"] = count_delta
    else:
        await edit_count.finish("无效的操作符，请使用 +, -, 或 =")
        return
    
    data[hall_id]["upload_time"] = current_time
    data[hall_id]["uploader"] = user_name

    save_data(group_id, data)
    await edit_count.finish(f"数据修改成功，当前 {data[hall_id]['name']} ({hall_id}) 共有 {data[hall_id]['count']} 人")

# 查询人数
look_count = on_endswith(
    "几",
    priority=100, 
    block=True
)

@look_count.handle()
async def handle_look_count(event: Event):
    group_id = str(event.group_id)
    data = load_data(group_id)
    status_message = check_plugin_status(data, event)
    if status_message:
        return
    
    hall_id = event.get_plaintext().rstrip("几").strip()

    if hall_id in data:
        hall_name = data[hall_id]['name']
        count = data[hall_id]['count']
        upload_time = data[hall_id].get('upload_time', '未知')
        uploader = data[hall_id].get('uploader', '无')

        response = f"{hall_name} ({hall_id}): {count}人（{uploader} 于 {upload_time}）"
        await look_count.finish(response)
    else:
        return

# 查询所有机厅人数
jt = on_command(
    "jt",
    aliases={"!jt","！jt","/jt"},
    priority=100,
    block=True
)

@jt.handle()
async def handle_jt(bot: Bot, event: Event):
    group_id = str(event.group_id)
    data = load_data(group_id)
    status_message = check_plugin_status(data, event)
    if status_message:
        return
    
    region_name = data.get("region", "北京")  # 默认城市名 北京
    total_count = 0
    message_lines = ["机厅在线人数:"]
    
    for hall_id in data.keys():
        if hall_id in ["region", "enabled"]:  # 跳过 "region" 和 "enabled" 字段
            continue
        hall_name = data[hall_id]['name']
        count = data[hall_id]['count']
        upload_time = data[hall_id].get('upload_time', '未知')
        uploader = data[hall_id].get('uploader', '无')
        
        total_count += count
        message_lines.append(f"{hall_name} ({hall_id}): {count}人（{uploader} 于 {upload_time}）")
    
    message_lines.append(f"{region_name}一共有{total_count}人正在出勤")
    
    await jt.finish("\n".join(message_lines))

# 修改地区名
edit_region_name = on_command(
    "修改地区名",
    aliases={"edit_region_name","bind region","edit region name","修改地区"},
    priority=100,
    block=True
)

@edit_region_name.handle()
async def handle_edit_region_name(bot: Bot, event: Event, args: Message = CommandArg()):
    group_id = str(event.group_id)
    data = load_data(group_id)
    status_message = check_plugin_status(data, event)
    if status_message:
        return
    
    region_name = args.extract_plain_text().strip()

    if not region_name:
        await edit_region_name.finish("使用方式：修改地区名 wmc聚集地（自定义地区名）")

    data["region"] = region_name
    save_data(group_id, data)

    await edit_region_name.finish(f"地区名已成功修改为：{region_name}")
