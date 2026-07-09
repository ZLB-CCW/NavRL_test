from dataclasses import dataclass


@dataclass
class VisualTarget:
    visible: bool
    cx_norm: float
    cy_norm: float
    area_norm: float
    confidence: float
    lost_time: float

    @classmethod
    def from_sequence(cls, values):
        if len(values) < 6:
            raise ValueError("Visual target sequence must contain 6 values")
        return cls(
            visible=float(values[0]) >= 0.5,
            cx_norm=float(values[1]),
            cy_norm=float(values[2]),
            area_norm=float(values[3]),
            confidence=float(values[4]),
            lost_time=float(values[5]),
        )


@dataclass
class VisualFollowConfig:
    target_area: float = 0.12
    center_deadband: float = 0.05
    area_deadband: float = 0.01
    yaw_gain: float = 1.0
    forward_gain: float = 2.0
    vertical_gain: float = 0.5
    max_forward_speed: float = 0.8
    max_vertical_speed: float = 0.4
    max_yaw_rate: float = 1.2
    short_lost_timeout: float = 0.8
    lost_command_decay: float = 0.25
    min_confidence: float = 0.4


@dataclass
class VisualFollowCommand:
    forward_speed: float
    vertical_speed: float
    yaw_rate: float
    active: bool
    state: str


class VisualFollowController:
    def __init__(self, config=None):
        self.config = config or VisualFollowConfig()
        self._last_command = self._zero("LOST_LONG", active=False)

    def update(self, target):
        if not self._is_tracking(target):
            command = self._lost_command(target)
            self._last_command = command
            return command

        cfg = self.config
        yaw_rate = self._deadband(-cfg.yaw_gain * target.cx_norm, cfg.center_deadband)
        vertical_speed = self._deadband(-cfg.vertical_gain * target.cy_norm, cfg.center_deadband)
        forward_speed = self._deadband(
            cfg.forward_gain * (cfg.target_area - target.area_norm),
            cfg.area_deadband,
        )

        command = VisualFollowCommand(
            forward_speed=self._clamp(forward_speed, -cfg.max_forward_speed, cfg.max_forward_speed),
            vertical_speed=self._clamp(vertical_speed, -cfg.max_vertical_speed, cfg.max_vertical_speed),
            yaw_rate=self._clamp(yaw_rate, -cfg.max_yaw_rate, cfg.max_yaw_rate),
            active=True,
            state="TRACKING",
        )
        self._last_command = command
        return command

    def _is_tracking(self, target):
        return target.visible and target.confidence >= self.config.min_confidence

    def _lost_command(self, target):
        if target.lost_time <= self.config.short_lost_timeout:
            decay = self.config.lost_command_decay
            return VisualFollowCommand(
                forward_speed=self._last_command.forward_speed * decay,
                vertical_speed=self._last_command.vertical_speed * decay,
                yaw_rate=self._last_command.yaw_rate * decay,
                active=True,
                state="LOST_SHORT",
            )
        return self._zero("LOST_LONG", active=False)

    @staticmethod
    def _deadband(value, deadband):
        if abs(value) <= deadband:
            return 0.0
        return value

    @staticmethod
    def _clamp(value, lower, upper):
        return max(lower, min(upper, value))

    @staticmethod
    def _zero(state, active):
        return VisualFollowCommand(
            forward_speed=0.0,
            vertical_speed=0.0,
            yaw_rate=0.0,
            active=active,
            state=state,
        )
