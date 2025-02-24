# Copyright (c) FIRST and other WPILib contributors.
# Open Source Software; you can modify and/or share it under the terms of
# the WPILib BSD license file in the root directory of this project.

import commands2
import rev

import Constants

# Class to run the roller over CAN
class CANRollerSubsystem(commands2.Subsystem):
    def __init__(self) -> None:
        super().__init__()

        self.rollerMotor = rev.SparkMax(
            Constants.ROLLER_MOTOR_ID, rev.SparkBase.MotorType.kBrushed
        )

        self.rollerMotor.setCANTimeout(250)

        self.sparkConfig = rev.SparkMaxConfig()
        self.sparkConfig.voltageCompensation(Constants.ROLLER_MOTOR_VCOMP)
        self.sparkConfig.smartCurrentLimit(Constants.ROLLER_MOTOR_CURRENT_LIMIT)
        self.rollerMotor.configure(self.sparkConfig, rev.SparkBase.ResetMode.kResetSafeParameters, rev.SparkBase.PersistMode.kPersistParameters)

    # Command to run the roller with joystick inputs
    def runRoller(
        self,
        rollerSubsystem,
        forward: lambda forward: forward,
        reverse: lambda reverse: reverse,
    ) -> commands2.Command:
        return commands2.cmd.run(
            lambda: self.rollerMotor.set(forward() - reverse()),
            rollerSubsystem,
        )
