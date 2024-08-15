from nonebot.plugin import PluginMetadata

from . import __main__

# 插件信息
__plugin_meta__ = PluginMetadata(
    name="mai2_pcount",
    description="wmc的机厅在线人数信息查询、修改插件~",
    usage="使用 mai2_pcount_help 来查看帮助信息喔~",
    type="application",
    homepage="https://github.com/shengwang52005/mai2_pcount",
    supported_adapters={"~onebot.v11"},
)