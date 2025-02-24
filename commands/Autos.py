# Copyright (c) FIRST and other WPILib contributors.
# Open Source Software; you can modify and/or share it under the terms of
# the WPILib BSD license file in the root directory of this project.

import commands2

from subsystems.CANDriveSubsystem import CANDriveSubsystem

# Example autonomous commands which drive forwards for 1 second.


class Autos(commands2.Command):
    def __init__(self) -> None:
        pass

    def exampleAuto(driveSubsystem: CANDriveSubsystem) -> commands2.Command:
        return commands2.cmd.run(
            lambda: driveSubsystem.arcadeDrive(0.5, 0.0)
        ).withTimeout(1.0)
