# ==================================================
# 权重明细面板组件
# ==================================================
from PySide6.QtWidgets import (
    QVBoxLayout,
    QHBoxLayout,
    QHeaderView,
    QWidget,
    QTableWidgetItem,
)
from PySide6.QtGui import QColor
from PySide6.QtCore import Qt
from qfluentwidgets import (
    CardWidget,
    TableWidget,
    ToolButton,
    BodyLabel,
    FluentIcon,
)

from app.common.display.formula_dialog import FormulaDialog


class WeightPanel(CardWidget):
    """可折叠的权重明细展示面板

    用于在抽签/点名结果界面展示每个被抽中学生的权重分解数据。
    默认折叠状态，点击标题栏展开/折叠。
    """

    def __init__(self, parent=None):
        super().__init__(parent)
        self._collapsed = True
        self._dialog = None
        self._init_ui()

    def _init_ui(self):
        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(12, 8, 12, 8)
        main_layout.setSpacing(6)

        # 标题栏
        header = QHBoxLayout()
        header.setContentsMargins(0, 0, 0, 0)

        self._collapse_btn = ToolButton(FluentIcon.CHEVRON_RIGHT, self)
        self._collapse_btn.setToolTip("展开")
        self._collapse_btn.clicked.connect(self.toggle_collapse)
        header.addWidget(self._collapse_btn)

        self._title_label = BodyLabel("权重明细", self)
        header.addWidget(self._title_label)

        header.addStretch()

        self._help_btn = ToolButton(FluentIcon.HELP, self)
        self._help_btn.setToolTip("查看权重计算规则")
        self._help_btn.clicked.connect(self._show_formula_dialog)
        header.addWidget(self._help_btn)

        main_layout.addLayout(header)

        # 权重表格
        self._table = TableWidget(self)
        self._table.setColumnCount(8)
        self._table.setHorizontalHeaderLabels([
            "学生", "基础权重", "频率因子", "小组平衡",
            "性别平衡", "时间因子", "屏蔽", "最终权重",
        ])
        self._table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self._table.setVisible(False)
        main_layout.addWidget(self._table)

    def set_students(self, students_data: list):
        """设置要展示的学生权重数据

        Args:
            students_data: 学生数据列表，每项应包含 name 和 weight_details 字段
        """
        self._table.clearContents()
        self._table.setRowCount(0)

        for student in students_data:
            if not isinstance(student, dict):
                continue

            name = student.get("name", student.get("id", "?"))
            details = student.get("weight_details", {})
            if not details:
                continue

            row = self._table.rowCount()
            self._table.insertRow(row)

            # 列: 学生 | 基础 | 频率 | 小组 | 性别 | 时间 | 屏蔽 | 最终
            self._table.setItem(row, 0, self._make_item(str(name)))

            base = details.get("base_weight", 0)
            self._table.setItem(row, 1, self._make_item(f"{base:.2f}"))

            freq = details.get("frequency_penalty", 0)
            self._table.setItem(row, 2, self._make_item(f"{freq:.2f}"))

            grp = details.get("group_balance", 0)
            self._table.setItem(row, 3, self._make_item(f"{grp:.2f}"))

            gen = details.get("gender_balance", 0)
            self._table.setItem(row, 4, self._make_item(f"{gen:.2f}"))

            time_f = details.get("time_factor", 0)
            self._table.setItem(row, 5, self._make_item(f"{time_f:.2f}"))

            shielded = details.get("is_shielded", False)
            self._table.setItem(
                row, 6, self._make_item("已屏蔽" if shielded else "正常")
            )

            total = details.get("total_weight", student.get("next_weight", 0))
            item = self._make_item(f"{total:.2f}")
            if shielded:
                item.setForeground(QColor("red"))
            self._table.setItem(row, 7, item)

    def toggle_collapse(self):
        """切换折叠/展开"""
        self._collapsed = not self._collapsed
        self._table.setVisible(not self._collapsed)
        if self._collapsed:
            self._collapse_btn.setIcon(FluentIcon.CHEVRON_RIGHT)
            self._collapse_btn.setToolTip("展开")
        else:
            self._collapse_btn.setIcon(FluentIcon.CHEVRON_DOWN)
            self._collapse_btn.setToolTip("折叠")

    def _show_formula_dialog(self):
        if self._dialog is None:
            self._dialog = FormulaDialog(self)
        self._dialog.exec()

    def _make_item(self, text: str):
        item = QTableWidgetItem(text)
        item.setTextAlignment(Qt.AlignCenter)
        item.setFlags(item.flags() & ~Qt.ItemIsEditable)
        return item

    def clear(self):
        """清空表格"""
        self._table.clearContents()
        self._table.setRowCount(0)
        if not self._collapsed:
            self.toggle_collapse()


def create_weight_panel(students_data: list, parent=None) -> WeightPanel:
    """便捷工厂函数，创建并填充权重面板"""
    panel = WeightPanel(parent)
    panel.set_students(students_data)
    return panel
