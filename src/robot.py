import commands1
import wpilib
from wpilib import SmartDashboard

from oi import OI
from subsystems.climbing import Climbing
from subsystems.drivetrain import Drivetrain
from subsystems.shooter import Shooter
from subsystems.vacuum import Vacuum


class MyRobot(wpilib.TimedRobot):
    oi = None
    drivetrain = None
    climbing = None
    shooter = None
    vacuum = None
    autonomous_command = None

    def autonomousInit(self):
        # Schedule the autonomous command
        self.drivetrain.reset_gyro_angle()
        self.autonomous_command = self.oi.get_auto_choice()
        self.autonomous_command.start()

    def testInit(self):
        pass

    def teleopInit(self):
        if self.autonomous_command:
            self.autonomous_command.cancel()

    def disabledInit(self):
        pass

    def robotInit(self):
        """
        This function is called upon program startup and
        should be used for any initialization code.
        """
        self.oi = OI(self)
        self.drivetrain = Drivetrain(self)
        self.climbing = Climbing(self)
        # self.oi.setup_button_bindings()

    def autonomousPeriodic(self):
        """This function is called periodically during autonomous."""
        commands1.Scheduler.getInstance().run()
        pass

    def teleopPeriodic(self):
        """This function is called periodically during operator control."""
        SmartDashboard.putString("Color Target", str(self.oi.get_game_message()))
        commands1.Scheduler.getInstance().run()

    def testPeriodic(self):
        """This function is called periodically during test mode."""
        pass


if __name__ == "__main__":
    wpilib.run(MyRobot)
