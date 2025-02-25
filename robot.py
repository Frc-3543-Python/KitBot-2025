#!/usr/bin/env python3
#
# Copyright (c) FIRST and other WPILib contributors.
# Open Source Software; you can modify and/or share it under the terms of
# the WPILib BSD license file in the root directory of this project.
#

import typing
import wpilib
import commands2
import hal
import phoenix5
import wpilib.drive
import Constants
import keyboard
from cscore import CameraServer
# from wpilib.cameraserver import CameraServer
# from RobotContainer import RobotContainer

class MyRobot(commands2.TimedCommandRobot):
    """
    Our default robot class, pass it to wpilib.run

    Command v2 robots are encouraged to inherit from TimedCommandRobot, which
    has an implementation of robotPeriodic which runs the scheduler for you
    """

    autonomousCommand: typing.Optional[commands2.Command] = None

    def robotInit(self) -> None:
        """
        This function is run when the robot is first started up and should be used for any
        initialization code.
        """
        if Constants.ROTATED:
            self.frontleft = phoenix5._ctre.TalonSRX(Constants.RIGHT_FOLLOWER_ID)
            self.backleft = phoenix5._ctre.TalonSRX(Constants.RIGHT_LEADER_ID)
            self.frontright = phoenix5._ctre.TalonSRX(Constants.LEFT_FOLLOWER_ID)
            self.backright = phoenix5._ctre.TalonSRX(Constants.LEFT_LEADER_ID)
        else:
            self.frontleft = phoenix5._ctre.TalonSRX(Constants.LEFT_LEADER_ID)
            self.backleft = phoenix5._ctre.TalonSRX(Constants.LEFT_FOLLOWER_ID)
            self.frontright = phoenix5._ctre.TalonSRX(Constants.RIGHT_LEADER_ID)
            self.backright = phoenix5._ctre.TalonSRX(Constants.RIGHT_FOLLOWER_ID)
        
        self.top = phoenix5._ctre.VictorSPX(Constants.ROLLER_MOTOR_ID)
        self.backleft.follow(self.frontleft)
        self.backright.follow(self.frontright)
        self.joy = wpilib.XboxController(Constants.DRIVER_CONTROLLER_PORT)
        self.servo = wpilib.Servo(Constants.SERVO_CHANNEL)
        self.listInputsX = []
        self.listInputsY = []
        CameraServer.enableLogging()
        self.camera1 = CameraServer.startAutomaticCapture(0)
        self.camera2 = CameraServer.startAutomaticCapture(1)
        self.camera1.setResolution(640, 480)
        self.camera2.setResolution(640, 480)
        self.camera1.setFPS(30)
        self.camera2.setFPS(30)
        self.sink = CameraServer.getVideo()
        
        # Instantiate our RobotContainer.  This will perform all our button bindings, and put our
        # autonomous chooser on the dashboard.
        #self.container = RobotContainer()

        # This line is used to track usage of the KitBot Templates. Please do not remove
        hal.report(hal.tResourceType.kResourceType_Framework, 10)

    def disabledInit(self) -> None:
        """This function is called once each time the robot enters Disabled mode."""
        # if len(self.listInputsX) > 0 and len(self.listInputsY) > 0:
        #     print(sum(self.listInputsX) / len(self.listInputsX))
        #     print(sum(self.listInputsY) / len(self.listInputsY))
    def disabledPeriodic(self) -> None:
        """This function is called periodically when disabled"""
        # self.top.set(phoenix5.ControlMode.PercentOutput, 1.0)
    def autonomousInit(self) -> None:
        """This autonomous runs the autonomous command selected by your RobotContainer class."""
            # self.autonomousCommand = self.container.getAutonomousCommand()
        if self.autonomousCommand:
            self.autonomousCommand.schedule()

    def autonomousPeriodic(self) -> None:
        """This function is called periodically during autonomous"""
        # self.frontleft.set(1)
        # self.frontleft.set(-1)
    def teleopInit(self) -> None:
        # This makes sure that the autonomous stops running when
        # teleop starts running. If you want the autonomous to
        # continue until interrupted by another command, remove
        # this line or comment it out.
        if self.autonomousCommand:
            self.autonomousCommand.cancel()
        # self.frontleft.set(phoenix5.ControlMode.PercentOutput, 1)
        # self.frontleft.set(phoenix5.ControlMode.PercentOutput, -1)
        
    def teleopPeriodic(self) -> None:
        """This function is called periodically during operator control"""
        # Rot = Constants.ROTATED
        # if self.joy.getRawButton(2):
        #     if Rot:
        #         Rot = False
        #     else:
        #         Rot = True
        #     if Rot:
        #         self.frontleft = phoenix5._ctre.TalonSRX(Constants.RIGHT_FOLLOWER_ID)
        #         self.backleft = phoenix5._ctre.TalonSRX(Constants.RIGHT_LEADER_ID)
        #         self.frontright = phoenix5._ctre.TalonSRX(Constants.LEFT_FOLLOWER_ID)
        #         self.backright = phoenix5._ctre.TalonSRX(Constants.LEFT_LEADER_ID)
        #     else:
        #         self.frontleft = phoenix5._ctre.TalonSRX(Constants.LEFT_LEADER_ID)
        #         self.backleft = phoenix5._ctre.TalonSRX(Constants.LEFT_FOLLOWER_ID)
        #         self.frontright = phoenix5._ctre.TalonSRX(Constants.RIGHT_LEADER_ID)
        #         self.backright = phoenix5._ctre.TalonSRX(Constants.RIGHT_FOLLOWER_ID)
        #     self.backleft.follow(self.frontleft)
        #     self.backright.follow(self.frontright)
        if Constants.MODE == "Joystick":
            self.lx = self.joy.getRawAxis(Constants.LEFT_JOYSTICK_X_AXIS)
            self.ly = self.joy.getRawAxis(Constants.LEFT_JOYSTICK_Y_AXIS)
            # if self.lx >= 0.1 and self.ly >= 0.1:
            #     self.listInputsX[len(self.listInputsX)] = self.lx
            #     self.listInputsY[len(self.listInputsY)] = self.ly
            if self.ly == abs(self.ly):
                self.rls = -(self.ly + self.lx)
                self.rrs = (self.ly - self.lx)
            else:
                self.rls = self.lx - self.ly
                self.rrs = self.lx + self.ly
            self.servo.set(self.joy.getRawAxis(Constants.RIGHT_TRIGGER_AXIS))
        elif Constants.MODE == "Buttons":
            self.lt = self.joy.getRawAxis(Constants.LEFT_TRIGGER_AXIS)
            self.lb = self.joy.getRawButton(Constants.LB)
            self.rt = self.joy.getRawAxis(Constants.RIGHT_TRIGGER_AXIS)
            self.rb = self.joy.getRawButton(Constants.RB)
            if Constants.DIFFERENTIAL:
                if self.lb == 1:
                    self.rls = -self.lt
                else:
                    self.rls = self.lt
                if self.rb == 1:
                    self.rrs = -self.rt
                else:
                    self.rrs = self.rt
            else:
                self.rls = self.lt - self.lb
                self.rrs = self.rt - self.rb
            self.rrs = -self.rrs
            self.servo.set(self.joy.getRawAxis(Constants.LEFT_JOYSTICK_Y_AXIS) / 2 + 0.5)
        elif Constants.MODE == "Keyboard":
            self.w = keyboard.is_pressed(Constants.W)
            self.a = keyboard.is_pressed(Constants.A)
            self.s = keyboard.is_pressed(Constants.S)
            self.d = keyboard.is_pressed(Constants.D)
            if self.w and self.s:
                self.w = False
                self.s = False
            if self.a and self.d:
                self.a = False
                self.d = False
            if self.w and self.d:
                self.rls = -1
                self.rrs = 0
            elif self.s and self.d:
                self.rls = 1
                self.rrs = 0
            elif self.s and self.a:
                self.rls = 0
                self.rrs = -1
            elif self.w and self.a:
                self.rls = 0
                self.rrs = 1
            elif self.w:
                self.rls = -1
                self.rrs = 1
            elif self.a:
                self.rls = 1
                self.rrs = 1
            elif self.s:
                self.rls = 1
                self.rrs = -1
            elif self.d:
                self.rls = -1
                self.rrs = -1
            else:
                self.rls = 0
                self.rrs = 0
        if Constants.INVERT:
            self.frontleft.set(phoenix5.ControlMode.PercentOutput, Constants.MOVE_SPEED * -self.rls)
            self.frontright.set(phoenix5.ControlMode.PercentOutput, Constants.MOVE_SPEED * -self.rrs)
        else:
            self.frontleft.set(phoenix5.ControlMode.PercentOutput, Constants.MOVE_SPEED * self.rls)
            self.frontright.set(phoenix5.ControlMode.PercentOutput, Constants.MOVE_SPEED * self.rrs)
        self.ry = self.joy.getRawAxis(Constants.RIGHT_JOYSTICK_Y_AXIS)
        if Constants.INVERT_EJECT:
            self.top.set(phoenix5.ControlMode.PercentOutput, -Constants.ROLLER_MOTOR_EJECT_SPEED * self.ry)
        else:
            self.top.set(phoenix5.ControlMode.PercentOutput, Constants.ROLLER_MOTOR_EJECT_SPEED * self.ry)
        #time, self.input_img = self.sink.grabFrame()
        if self.joy.getRawButton(Constants.START):
            self.endCompetition()
    def testInit(self) -> None:
        # Cancels all running commands at the start of test mode
        commands2.CommandScheduler.getInstance().cancelAll()


if __name__ == "__main__":
    wpilib.run(MyRobot)
