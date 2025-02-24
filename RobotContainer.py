# Copyright (c) FIRST and other WPILib contributors.
# Open Source Software; you can modify and/or share it under the terms of
# the WPILib BSD license file in the root directory of this project.

import commands2
import commands2.button

import Constants
from commands.Autos import Autos
from subsystems.CANDriveSubsystem import CANDriveSubsystem
from subsystems.CANRollerSubsystem import CANRollerSubsystem


class RobotContainer:
    """
    This class is where the bulk of the robot should be declared. Since Command-based is a
    "declarative" paradigm, very little robot logic should actually be handled in the :class:`.Robot`
    periodic methods (other than the scheduler calls). Instead, the structure of the robot (including
    subsystems, commands, and button mappings) should be declared here.
    """

    # Constructor for a new instance of the robot container. This is where the subsystems and the controllers should be set up
    def __init__(self) -> None:
        self.driverController = commands2.button.CommandXboxController(
            Constants.DRIVER_CONTROLLER_PORT
        )
        self.operatorController = commands2.button.CommandXboxController(
            Constants.OPERATOR_CONTROLLER_PORT
        )

        self.driveSubsystem = CANDriveSubsystem()
        self.rollerSubsystem = CANRollerSubsystem()

        self.autos = Autos()

        self.configureButtonBindings()

    # Function to bind commands to buttons on the driver and operator controllers.
    def configureButtonBindings(self):
        self.driveSubsystem.setDefaultCommand(
            self.driveSubsystem.arcadeDrive(
                self.driveSubsystem,
                lambda: -self.driverController.getLeftY(),
                lambda: -self.driverController.getRightX(),
            )
        )
        self.rollerSubsystem.setDefaultCommand(
            self.rollerSubsystem.runRoller(
                self.rollerSubsystem,
                lambda: self.operatorController.getRightTriggerAxis(),
                lambda: self.operatorController.getLeftTriggerAxis(),
            )
        )
        self.operatorController.a().whileTrue(
            self.rollerSubsystem.runRoller(
                self.rollerSubsystem,
                lambda: Constants.ROLLER_MOTOR_EJECT_SPEED,
                lambda: 0,
            )
        )

    def getAutonomousCommand(self) -> commands2.Command:
        return self.autos.exampleAuto(self.driveSubsystem)
