"""
create_simple_table -
制作简单图表
Author:仗剑天涯
Date:2026/4/13
"""
# 导入 openpyxl 库，用于操作 Excel 文件
import openpyxl
# 从 openpyxl 中导入 Workbook 类（用于创建工作簿）
from openpyxl import Workbook
# 再次导入 Workbook（冗余，因为上一行已经导入），但语法正确
from openpyxl.workbook import Workbook
# 导入 BarChart（柱状图）和 Reference（数据区域引用）类
from openpyxl.chart import BarChart, Reference
# 导入 Worksheet 类（用于类型注解）
from openpyxl.worksheet.worksheet import Worksheet

# 创建一个新的工作簿对象（Excel 文件）
# 使用类型注解提示 wb 是 Workbook 类型（方便 IDE 自动补全）
wb = openpyxl.Workbook()  # type:Workbook

# 在工作簿中创建一个名为“数据分析柱状图”的新工作表
# 注意：create_sheet 默认插入到末尾，返回的是 Worksheet 对象
ws = wb.create_sheet('数据分析柱状图')  # type:Worksheet

# 打印 ws 的类型，确认它是 <class 'openpyxl.worksheet.worksheet.Worksheet'>
print(type(ws))

# 定义要写入表格的数据（二维元组）
# 第一行是表头：类别、销售A组、销售B组
# 后面每行是具体类别和两组销量数据
rows = [
    ('类别', '销售A组', '销售B组'),
    ('手机', 40, 30),
    ('平板', 50, 60),
    ('笔记本', 70, 80),
    ('外围设备', 90, 48)
]

# 遍历 rows 中的每一行，使用工作表对象的 append 方法将行数据追加到工作表中
# append 方法会自动将数据放在当前已有数据的下一行
for row in rows:
    ws.append(row)

# 创建柱状图对象
chart1 = BarChart()

# 设置图表的预定义样式编号（openpyxl 内置多种样式，范围 1~48）
chart1.style = 10

# 设置图表类型：'col' 表示垂直柱状图（column）；也可用 'bar' 表示水平条形图
chart1.type = 'col' # 去耦合化，改变1个值就可以改变表格方向

# 设置图表的标题
chart1.title = '销售统计图'

# 设置 Y 轴（纵轴）标题
chart1.y_axis.title = '销量'

# 设置 X 轴（横轴）标题
chart1.x_axis.title = '商品类别'

# 定义图表的数据来源区域
# Reference(工作表, min_row, max_row, min_col, max_col)
# 这里选择第1行到第5行，第2列到第3列（即销售A组和销售B组的数据，包括表头）
# 行列从1开始数，而且最大行可以取到！！！
# 这是openpyxl库严格遵循Excel的标准而完成的！！！
data = Reference(ws, min_row=1, max_row=5, min_col=2, max_col=3)

# 定义图表的类别轴（X轴标签）来源区域
# 选择第2行到第5行，第1列（即“手机”、“平板”、“笔记本”、“外围设备”）
cats = Reference(ws, min_col=1, min_row=2, max_row=5)

# 将数据添加到图表中
# titles_from_data=True 表示使用数据区域的第一行（即表头“销售A组”“销售B组”）作为图例标题
# 图例标题：小方块-销售A组，小方块-销售B组
chart1.add_data(data, titles_from_data=True)

# 设置图表的类别轴标签（即 X 轴显示的文字）
chart1.set_categories(cats)

# 设置柱状图的形状（shape=4 表示矩形柱，其他值可能产生不同的视觉效果，取决于 openpyxl 版本）
chart1.shape = 4

# 将图表添加到工作表中，放置在单元格 A10 的位置（图表的左上角对齐 A10）
ws.add_chart(chart1, 'A10')

# 保存工作簿到指定路径
# 注意：需要确保 resources 文件夹已存在，否则会报错
wb.save('resources/销售柱状统计表.xlsx')

