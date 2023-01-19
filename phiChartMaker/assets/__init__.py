"""此模块用来对 Phigros 谱面中的元素创建对象。
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


# pylint: disable-next=too-many-instance-attributes
class JudgeLine:
    """该类用来创建一个判定线对象。"""

    # pylint: disable-next=too-many-arguments
    def __init__(
        self,
        num_of_notes: int,
        num_of_notes_above: int,
        num_of_notes_below: int,
        bpm: float,
        speed_events: list[dict[str, float]],
        notes_above: list[dict[str, float]],
        notes_below: list[dict[str, float]],
        judge_line_disappear_events: list[dict[str, float]],
        judge_line_move_events: list[dict[str, float]],
        judge_line_rotate_events: list[dict[str, float]],
    ):
        """该方法用来初始化一个判定线对象。

        Args:
            num_of_notes (int):                                     判定线上的音符总数量。
            num_of_notes_above (int):                               从判定线上方下落的音符总数量。
            num_of_notes_below (int):                               从判定线下方下落的音符总数量。
            bpm (float):                                            该判定线上，所有音符遵从的 BPM。
            speed_events (list[dict[str, float]]):                  该判定线上发生的所有速度事件。
            notes_above (list[dict[str, float]]):                   该判定线上所有从上方下落的音符。
            notes_below (list[dict[str, float]]):                   该判定线上所有从下方下落的音符。
            judge_line_disappear_events (list[dict[str, float]]):   该判定线上发生的所有判定线透明度事件。
            judge_line_move_events (list[dict[str, float]]):        该判定线上发生的所有判定线移动事件。
            judge_line_rotate_events (list[dict[str, float]]):      该判定线上发生的所有判定线旋转事件。
        """
        self.num_of_notes = num_of_notes
        self.num_of_notes_above = num_of_notes_above
        self.num_of_notes_below = num_of_notes_below
        self.bpm = bpm
        self.speed_events = speed_events
        self.notes_above = []
        self.notes_below = []
        self.judge_line_disappear_events = judge_line_disappear_events
        self.judge_line_move_events = judge_line_move_events
        self.judge_line_rotate_events = judge_line_rotate_events
        self.initialize_note(notes_above, notes_below)

    def initialize_note(
        self, notes_above: list[dict[str, float]], notes_below: list[dict[str, float]]
    ):
        """该方法用来初始化判定线上的音符。

        Args:
            notes_above (list[dict[str, float]]): 该判定线上所有从上方下落的音符组成的列表。
            notes_below (list[dict[str, float]]): 该判定线上所有从下方下落的音符组成的列表。
        """
        for note in notes_above:
            # TODO 解决 Pylance 的 reportUnknownMemberType 错误
            if note["type"] == 1:
                self.notes_above.append(
                    Tap(
                        note["time"],
                        note["positionX"],
                        note["speed"],
                        note["floorPosition"],
                    )
                )
            elif note["type"] == 2:
                self.notes_above.append(
                    Drag(
                        note["time"],
                        note["positionX"],
                        note["speed"],
                        note["floorPosition"],
                    )
                )
            elif note["type"] == 3:
                self.notes_above.append(
                    Hold(
                        note["time"],
                        note["positionX"],
                        note["holdTime"],
                        note["speed"],
                        note["floorPosition"],
                    )
                )
            elif note["type"] == 4:
                self.notes_above.append(
                    Flick(
                        note["time"],
                        note["positionX"],
                        note["speed"],
                        note["floorPosition"],
                    )
                )
        for note in notes_below:
            # TODO 解决 Pylance 的 reportUnknownMemberType 错误
            if note["type"] == 1:
                self.notes_below.append(
                    Tap(
                        note["time"],
                        note["positionX"],
                        note["speed"],
                        note["floorPosition"],
                    )
                )
            elif note["type"] == 2:
                self.notes_below.append(
                    Drag(
                        note["time"],
                        note["positionX"],
                        note["speed"],
                        note["floorPosition"],
                    )
                )
            elif note["type"] == 3:
                self.notes_below.append(
                    Hold(
                        note["time"],
                        note["positionX"],
                        note["holdTime"],
                        note["speed"],
                        note["floorPosition"],
                    )
                )
            elif note["type"] == 4:
                self.notes_below.append(
                    Flick(
                        note["time"],
                        note["positionX"],
                        note["speed"],
                        note["floorPosition"],
                    )
                )


class NoteBase:
    """该类是所有 Note 的基类，可在基于此创建其它 Note 类。"""

    # pylint: disable-next=too-many-arguments
    def __init__(
        self,
        type_: int,
        time: float,
        position_x: float,
        hold_time: float,
        speed: float,
        floor_position: float,
    ):
        """该方法用来初始化一个 Note 对象。

        Args:
            type_ (int):            Note 的类型。其中，1 为 Tap，2 为 Drag，3 为 Hold，4 为 Flick。
            time (float):           Note 被打击的初始时间。
            position_x (float):     Note 相对于判定线锚点的位置。
            hold_time (float):      Note 被打击的持续时间。对于一个 Hold Note，该时间为其持续时间；对于一个其它音符，该时间为 0。
            speed (float):          Note 下落的速度。
            floor_position (float): 未知变量。
        """
        self.type = type_
        self.time = time
        self.position_x = position_x
        self.hold_time = hold_time
        self.speed = speed
        self.floor_position = floor_position


class Tap(NoteBase):
    """该类用来创建一个 Tap Note 对象。"""

    def __init__(
        self, time: float, position_x: float, speed: float, floor_position: float
    ):
        """该方法用来初始化一个 Tap Note 对象。

        Args:
            time (float):           Note 被打击的初始时间。
            position_x (float):     Note 相对于判定线锚点的位置。
            speed (float):          Note 下落的速度。
            floor_position (float): 未知变量。
        """
        super().__init__(1, time, position_x, 0, speed, floor_position)


class Drag(NoteBase):
    """该类用来创建一个 Drag Note 对象。"""

    def __init__(
        self, time: float, position_x: float, speed: float, floor_position: float
    ):
        """该方法用来初始化一个 Drag Note 对象。

        Args:
            time (float):           Note 被打击的初始时间。
            position_x (float):     Note 相对于判定线锚点的位置。
            speed (float):          Note 下落的速度。
            floor_position (float): 未知变量。
        """
        super().__init__(2, time, position_x, 0, speed, floor_position)


class Hold(NoteBase):
    """该类用来创建一个 Hold Note 对象。"""

    # pylint: disable-next=too-many-arguments
    def __init__(
        self,
        time: float,
        position_x: float,
        hold_time: float,
        speed: float,
        floor_position: float,
    ):
        """该方法用来初始化一个 Hold Note 对象。

        Args:
            time (float):           Note 被打击的初始时间。
            position_x (float):     Note 相对于判定线锚点的位置。
            hold_time (float):      Note 被打击的持续时间。
            speed (float):          Note 下落的速度。
            floor_position (float): 未知变量。
        """
        super().__init__(3, time, position_x, hold_time, speed, floor_position)
        self.end_time = self.time + self.hold_time


class Flick(NoteBase):
    """该类用来创建一个 Flick Note 对象。"""

    def __init__(
        self, time: float, position_x: float, speed: float, floor_position: float
    ):
        """该方法用来初始化一个 Flick Note 对象。

        Args:
            time (float):           Note 被打击的初始时间。
            position_x (float):     Note 相对于判定线锚点的位置。
            speed (float):          Note 下落的速度。
            floor_position (float): 未知变量。
        """
        super().__init__(4, time, position_x, 0, speed, floor_position)
