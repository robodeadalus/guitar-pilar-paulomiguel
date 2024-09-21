#!/usr/bin/env python3
import random
from ringbuffer import RingBuffer
import math


class GuitarString:
    def __init__(self, frequency: float):
        """
        Create a guitar string of the given frequency, using a sampling rate of 44100 Hz
        """
        self.tickcount = 0
        sample_rate = 44100
        self.capacity = math.ceil(sample_rate / frequency)
        self.buffer = RingBuffer(self.capacity)  # make ringbuffer object

    @classmethod
    def make_from_array(cls, init: list[int]):
        """
        Create a guitar string whose size and initial values are given by the array init
        """
        stg = cls(1000)  # calculate frequency

        stg.capacity = len(init)
        stg.buffer = RingBuffer(stg.capacity)
        for x in init:
            stg.buffer.enqueue(x)
        return stg

    def pluck(self):
        """
        Set the buffer to white noise
        """
        for i in range(self.capacity):
            if self.buffer.is_full():
                self.buffer.dequeue()
            else:
                random_value = random.uniform(-0.5, 0.5)
                self.buffer.enqueue(random_value)

    def tick(self):
        """
        Advance the simulation one time step by applying the Karplus--Strong update
        """
        # do not tick if buffer is empty
        if self.buffer.is_empty() == True:
            pass
        else:
            # self.buffer.dequeue()
            front = self.buffer.dequeue()
            next_sample = 0.996 * ((front + self.buffer.peek()) / 2)
            self.buffer.enqueue(next_sample)
            self.tickcount += 1

    def sample(self) -> float:
        """
        Return the current sample
        """
        # do not sample if buffer is empty
        if self.buffer.is_empty() == True:
            return 0
        else:
            return self.buffer.peek() # return value at front of circular queue

    def time(self) -> int:
        """
        Return the number of ticks so far
        """
        return self.tickcount  # return number of ticks that occurred
