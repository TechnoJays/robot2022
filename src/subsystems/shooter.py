import configparser
from typing import Optional

from wpilib import IterativeRobotBase, PWMMotorController, PWMVictorSPX, SmartDashboard
from commands1 import Subsystem
from commands.do_nothing_shooter import DoNothingShooter
from commands.shooter_drive import ShooterDrive

class Shooter(Subsystem):
    # Config file section name
    GENERAL_SECTION = "ShooterGeneral"

    # Config keys
    ENABLED_KEY = "ENABLED"
    INVERTED_KEY = "INVERTED"
    MAX_SPEED_KEY = "MAX_SPEED"
    CHANNEL_KEY = "CHANNEL"
    MODIFIER_SCALING_KEY = "MODIFIER_SCALING"

    _robot: IterativeRobotBase = None

    _enabled: bool = False

    _motor: PWMMotorController = None
    _max_speed: float = 0.0
    _modifier_scaling: Optional[float] = None

    def __init__(
        self, 
        robot: IterativeRobotBase, 
        name: str ="Shooter", 
        configfile: str ="/home/lvuser/py/configs/subsystems.ini"
    ):
        self._robot = robot
        self._config = configparser.ConfigParser()
        self._config.read(configfile)
        self._enabled = self._config.getboolean(
            Shooter.GENERAL_SECTION, Shooter.ENABLED_KEY
        )
        self._init_components()
        print("Shooter initialized")
        Shooter._update_smartdashboard(0.0)
        super().__init__(name)

    def _init_components(self):
        # self._max_speed = self._config.getfloat(
        #     Shooter.GENERAL_SECTION, Shooter.MAX_SPEED_KEY
        # )
        self._max_speed = 1.0
        if self._enabled:
            print("Shooter enabled")
            self._motor = PWMVictorSPX(
                self._config.getint(Shooter.GENERAL_SECTION, Shooter.CHANNEL_KEY)
            )
            self._motor.setInverted(
                self._config.getboolean(Shooter.GENERAL_SECTION, Shooter.INVERTED_KEY)
            )


    def initDefaultCommand(self):
        # TODO Shooter needs independent DoNothin
        self.setDefaultCommand(ShooterDrive(self._robot))

    
    def move(self, speed: float):
        adjusted_speed = 0.0
        if self._motor:
            adjusted_speed = speed * self._max_speed
            self._motor.set(adjusted_speed)
            print("Motor Speed")
        Shooter._update_smartdashboard(adjusted_speed)

    @staticmethod
    def _update_smartdashboard(speed: float = 0.0):
        SmartDashboard.putNumber("Shooter Speed", speed)
