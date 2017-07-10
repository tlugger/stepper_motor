from nio.block.base import Block
from nio.properties import VersionProperty, IntProperty, SelectProperty

from Adafruit_MotorHAT import Adafruit_MotorHAT, Adafruit_DCMotor, Adafruit_StepperMotor

import time
import atexit
from enum import Enum

class Directions(Enum):
    FORWARD = Adafruit_MotorHAT.FORWARD
    BACKWARD = Adafruit_MotorHAT.BACKWARD

class CoilSteps(Enum):
    SINGLE = Adafruit_MotorHAT.SINGLE
    DOUBLE = Adafruit_MotorHAT.DOUBLE
    INTERLEAVE = Adafruit_MotorHAT.INTERLEAVE
    MICROSTEP = Adafruit_MotorHAT.MICROSTEP

class StepMotor(Block):

    version = VersionProperty('0.1.0')
    motor = IntProperty(title='Motor number', default=1)
    steprate = IntProperty(title='Step Rate', default=200)
    speed = IntProperty(title='Speed', default=30)
    steps = IntProperty(title='Number of Steps', default=100)
    direction = SelectProperty(Directions, title="Direction", default="FORWARD")
    coil_steps = SelectProperty(CoilSteps, title="Coil Steps", default="SINGLE")

    def __init__(self):
        super().__init__()
        self.mh = None
        self.stepper = None

    def turnOffMotors(self):
        self.mh.getMotor(1).run(Adafruit_MotorHAT.RELEASE)
        self.mh.getMotor(2).run(Adafruit_MotorHAT.RELEASE)
        self.mh.getMotor(3).run(Adafruit_MotorHAT.RELEASE)
        self.mh.getMotor(4).run(Adafruit_MotorHAT.RELEASE)

    def start(self):
        self.mh = Adafruit_MotorHAT()
        atexit.register(self.turnOffMotors)
        self.stepper = self.mh.getStepper(self.steprate(), self.motor())
        self.stepper.setSpeed(self.speed())

    def process_signals(self, signals):
        for signal in signals:
            self.stepper.step(self.steps(), self.direction().value,  self.coil_steps().value)
        self.notify_signals(signals)
