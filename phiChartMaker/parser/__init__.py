"""该模块用来对谱面中的元素进行变换处理。
版权所有 (C) 2023 phiChartMaker

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program.  If not, see <https://www.gnu.org/licenses/>.

本程序是自由软件：你可以根据自由软件基金会 (the Free Software Foundation)
发布的 GNU 通用公共许可证 (GNU General Public License) 的条款，无论是许可证
的第 3 版，还是（由你选择）任何更高的版本，重新发布 和/或 修改本程序。

本程序是基于使用目的而加以发布，然而不负任何担保责任；亦无对适售性或特定目的适用性
所为的默示性担保。详情请参照 GNU 通用公共许可证 (GNU General Public License)。

你应该已经收到了一份与本程序一起的 GNU 通用公共许可证 (GNU General Public License)
的副本。如果没有，请参阅 <https://www.gnu.org/licenses/>。
"""

# pylint: disable=invalid-name

import math


# TODO 解决此模块 Pylance 报错 reportUnknownVariableType, reportOptionalSubscript 的问题
def get_endpoint_position(
    move_events: list[dict[str, float]],
    rotate_events: list[dict[str, float]],
    time: float,
) -> list[tuple[float, float]]:
    """该方法用来计算某一时刻，判定线两个端点的坐标。

    Args:
        move_events (list[dict[str, float]]): 该判定线所有移动事件组成的列表。
        rotate_events (list[dict[str, float]]): 该判定线所有旋转事件组成的列表。
        time (float): 所计算的时刻。

    Returns:
        list[tuple[float, float]]: 一个由以元组形式表示的两端点坐标组成的列表。
    """

    ### 从 move_events 中筛选出符合条件的 move_dict
    # 该 move_dict 满足 move_dict["startTime"] <= time <= move_dict["endTime"]，即需求时间时此刻发生的判定线移动事件
    # TODO 解决由部分工具转换 RPE/PE 谱面时，导致事件发生时间重合或反向的问题
    move_dict = next(
        filter(lambda x: x["startTime"] <= time <= x["endTime"], move_events), None
    )

    ### 从 rotate_events 中筛选出符合条件的 rotate_dict
    # 其原理同 move_events 的筛选逻辑
    rotate_dict = next(
        filter(lambda x: x["startTime"] <= time <= x["endTime"], rotate_events), None
    )

    ### 计算判定线锚点的坐标
    # 首先，获得整个移动事件发生的总耗时
    move_action_total_time = move_dict["endTime"] - move_dict["startTime"]
    # 然后，获得当前事件已经进行的时间
    time_interval_from_start = time - move_dict["startTime"]
    # 其次，获得当前事件已经进行的比例
    percentage_of_time_used = time_interval_from_start / move_action_total_time
    # 以此计算出锚点的即时坐标
    point_x = move_dict["start"] + percentage_of_time_used * (
        move_dict["end"] - move_dict["start"]
    )
    point_y = move_dict["start2"] + percentage_of_time_used * (
        move_dict["end2"] - move_dict["start2"]
    )

    ### 计算判定线的即时旋转角
    # 首先，获得整个移动事件发生的总耗时
    rotate_action_total_time = rotate_dict["endTime"] - rotate_dict["startTime"]
    # 然后，获得当前事件已经进行的时间
    time_interval_from_start = time - rotate_dict["startTime"]
    # 其次，获得当前事件已经进行的比例
    percentage_of_time_used = time_interval_from_start / rotate_action_total_time
    # 以此计算出锚点的即时旋转角
    point_r = rotate_dict["start"] + percentage_of_time_used * (
        rotate_dict["end"] - rotate_dict["start"]
    )

    ### 计算判定线两个端点的坐标 p1 p2
    # p1 p2 的端点坐标使用 p1x, p1y, p2x, p2y 表示
    # 首先假定该判定线为水平于 x 轴，使用锚点坐标计算出两个端点的理论坐标
    length = 3
    p1x = point_x - length / 2
    p1y = point_y + 0
    p2x = point_x + length / 2
    p2y = point_y + 0
    # 根据 RPE 的设计，可得旋转的方向默认为正，故有
    angle = math.radians(point_r)
    p1x_rotated = (
        point_x + (p1x - point_x) * math.cos(angle) - (p1y - point_y) * math.sin(angle)
    )
    p1y_rotated = (
        point_y + (p1x - point_x) * math.sin(angle) + (p1y - point_y) * math.cos(angle)
    )
    p2x_rotated = (
        point_x + (p2x - point_x) * math.cos(angle) - (p2y - point_y) * math.sin(angle)
    )
    p2y_rotated = (
        point_y + (p2x - point_x) * math.sin(angle) + (p2y - point_y) * math.cos(angle)
    )

    ### 最终，以列表内嵌元组形式返回两个端点的坐标
    p1 = (p1x_rotated, p1y_rotated)
    p2 = (p2x_rotated, p2y_rotated)
    return [p1, p2]


def get_edge_intersection(
    move_events: list[dict[str, float]],
    rotate_events: list[dict[str, float]],
    time: float,
) -> list[tuple[float | bool, int]]:
    """该方法用来计算某一时刻，判定线和屏幕边缘的交点。

    Args:
        move_events (list[dict[str, float]]): 该判定线所有移动事件组成的列表。
        rotate_events (list[dict[str, float]]): 该判定线所有旋转事件组成的列表。
        time (float): 所计算的时刻。

    Returns:
        list[tuple[float | bool, int]]: 一个由上下左右四个交点以元组形式组成的列表。
        # TODO 对于不能计算出交点的点，直接返回 False 而不返回元组
    """

    ### 首先，使用函数 get_endpoint_position 获得两个端点坐标，并存储至对应变量
    p1, p2 = (
        get_endpoint_position(move_events, rotate_events, time)[0],
        get_endpoint_position(move_events, rotate_events, time)[1],
    )
    p1x_rotated = p1[0]
    p1y_rotated = p1[1]
    p2x_rotated = p2[0]
    p2y_rotated = p2[1]

    ### 之后，就可以开始计算判定线和屏幕的交点
    # FIXME 修复在锚点高于屏幕上边缘时导致屏幕上边缘交点返回 False 的问题
    # 经过简单的数学证明：当锚点位于屏幕之内时，则 p1 一定是较高的点。故分情况讨论如下
    # 如果线段端点 1 在上边缘之上
    if p1y_rotated > 1:
        up_edge_x = p1x_rotated + (1 - p1y_rotated) * (p2x_rotated - p1x_rotated) / (
            p2y_rotated - p1y_rotated
        )
    else:
        up_edge_x = False
    # 如果线段端点 2 在下边缘之下
    if p2y_rotated < 0:
        down_edge_x = p1x_rotated + (0 - p1y_rotated) * (p2x_rotated - p1x_rotated) / (
            p2y_rotated - p1y_rotated
        )
    else:
        down_edge_x = False
    # TODO 完成左边缘和右边缘的逻辑编写

    # 最后，以列表形式返回四个端点（目前为两个）的坐标
    return [(up_edge_x, 1), (down_edge_x, 0)]
