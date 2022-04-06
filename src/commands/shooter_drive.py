from commands1 import Command
from hal import JoystickButtons
from wpilib import IterativeRobotBase

from oi import JoystickAxis, UserController


class ShooterDrive(Command):
    _dpad_scaling: float
    _stick_scaling: float

    def __init__(
        self,
        robot: IterativeRobotBase,
        name: str = "ShooterDrive",
        modifier_scaling: float = 0.5,
        dpad_scaling: float = 0.4,
        timeout: int = 15,
    ):
        super().__init__(name, timeout)
        self.robot = robot
        self.requires(robot.shooter)
        self._dpad_scaling = dpad_scaling
        self._stick_scaling = modifier_scaling

    def initialize(self):
        """Called before the Command is run for the first time."""
        return Command.initialize(self)

    def execute(self):
        """Called repeatedly when this Command is scheduled to run"""
        shooting: bool = self.robot.oi.get_button_state(
            UserController.SCORING, JoystickButtons.RIGHTTRIGGER
        )
        unshooting: bool = self.robot.oi.get_button_state(
            UserController.SCORING, JoystickButtons.LEFTTRIGGER
        )
        isDrivable: bool = not(shooting or unshooting)

        if isDrivable:
            shooter: float = self.robot.oi.get_axis(
                UserController.SCORING, JoystickAxis.RIGHTY
            )
            self.robot.shooter.move(shooter * self._stick_scaling)

        return Command.execute(self)

    def isFinished(self):
        """Returns true when the Command no longer needs to be run"""
        return False

    def end(self):
        """Called once after isFinished returns true"""
        pass

    def interrupted(self):
        """Called when another command which requires one or more of the same subsystems is scheduled to run"""
        self.end()
