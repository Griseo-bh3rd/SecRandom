# ==================================================
# 权重计算公式说明弹窗
# ==================================================
from PySide6.QtWidgets import QVBoxLayout
from qfluentwidgets import Dialog, TextEdit


class FormulaDialog(Dialog):
    """权重计算规则说明弹窗

    显示权重计算公式的详细文字说明，帮助用户理解公平抽取算法。
    """

    FORMULA_TEXT = (
        "**权重计算规则**\n\n"
        "**总权重 = 基础权重 + 频率因子 + 小组平衡 + 性别平衡 + 时间因子**\n\n"
        "---\n\n"
        "**基础权重**: 每个学生的初始权重值，可在设置中调整。（默认 1.0）\n\n"
        "**频率因子**: 基于学生被抽取次数计算。\n"
        "  • 被抽中次数越少 → 频率因子越高，越容易被抽到\n"
        "  • 支持三种函数：线性、平方根、指数（可在设置中选择）\n"
        "  • 冷启动阶段，系统自动保护新同学（前10轮）\n\n"
        "**小组平衡**: 基于学生所在小组的被抽取次数。\n"
        "  • 小组被抽中次数越少 → 该小组成员获得更高权重\n"
        "  • 鼓励不同小组之间机会均等\n\n"
        "**性别平衡**: 基于学生性别的被抽取次数。\n"
        "  • 该性别被抽中次数越少 → 该性别的成员获得权重加成\n"
        "  • 鼓励男女机会均等\n\n"
        "**时间因子**: 被抽中时间越久远 → 权重逐渐恢复。\n"
        "  • 超过30天未抽取 → 时间因子加满（1.0）\n\n"
        "---\n\n"
        "**特殊规则**:\n"
        "  • **屏蔽保护**: 刚被抽过的人，在设定时间内几乎不被抽中\n"
        "    （权重降至最低的 1/10）\n"
        "  • **冷启动**: 系统使用初期，自动保护抽取次数较低的成员\n"
        "  • **权重裁剪**: 最低 ≥ 0.05，最高 ≤ 5.0\n\n"
        "**平均值差值保护**（独立机制）:\n"
        "  只允许抽取次数 ≤ 平均值的成员进入候选池，\n"
        "  当最大与最小次数差距过大时排除极值，\n"
        "  有效避免过度抽取少数人。"
    )

    def __init__(self, parent=None):
        super().__init__("权重计算规则", parent)
        self.setMinimumWidth(520)

        layout = QVBoxLayout(self)
        layout.setContentsMargins(16, 12, 16, 12)

        text_edit = TextEdit(self)
        text_edit.setReadOnly(True)
        text_edit.setMarkdown(self.FORMULA_TEXT)
        text_edit.setMinimumHeight(400)
        layout.addWidget(text_edit)

        # Dialog 已有自带的取消按钮，点击关闭即可
        self.setContentCopyable(False)
