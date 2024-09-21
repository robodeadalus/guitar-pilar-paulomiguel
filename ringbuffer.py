#!/usr/bin/env python3


class RingBuffer:
    def __init__(self, capacity: int):
        """
        Create an empty ring buffer, with given max capacity
        """
        self.MAX_CAP = capacity
        self._front = 0  # index of the oldest inserted item
        self._rear = 0  # index where next item will be inserted
        self.buffer = [None] * self.MAX_CAP  # code inspiration from https://www.geeksforgeeks.org/python-initialize-empty-array-of-given-length/

    def size(self) -> int:
        """
        Return number of items currently in the buffer
        """
        if self._front < self._rear:
            return self._rear - self._front
        elif self._front > self._rear:
            return self._rear + (self.MAX_CAP - self._front)
        elif self._front == self._rear:
            if self.buffer[self._rear] == None:
                return 0
            else:
                return self.MAX_CAP

    def is_empty(self) -> bool:
        """
        Is the buffer empty (size equals zero)?
        """
        if self.size() == 0:
            return True
        else:
            return False

    def is_full(self) -> bool:
        """
        Is the buffer full (size equals capacity)?
        """
        if self.size() == self.MAX_CAP:
            return True
        else:
            return False

    def enqueue(self, x: float):
        """
        Add item `x` to the end
        """
        try:
            if self.is_full():
                raise RingBufferFull
            else:
                # add the item
                self.buffer[self._rear] = x
                # increase _rear
                if self._rear < (self.MAX_CAP - 1):
                    self._rear += 1
                else:
                    self._rear = 0
        except RingBufferFull:
            print("Ring buffer is full!")
            raise

    def dequeue(self) -> float:
        """
        Return and remove item from the front
        """
        try:
            if self.is_empty():
                raise RingBufferEmpty
            else:
                # remove the item
                removed_item = self.peek()
                self.buffer[self._front] = None
                # increase _front
                if self._front < (self.MAX_CAP - 1):
                    self._front += 1
                else:
                    self._front = 0
                return removed_item
        except RingBufferEmpty:
            print("Ring buffer is empty!")
            raise

    def peek(self) -> float:
        """
        Return (but do not delete) item from the front
        """
        try:
            if self.is_empty():
                raise RingBufferEmpty
            else:
                return self.buffer[self._front]
        except RingBufferEmpty:
            print("Ring buffer is empty!")
            raise


class RingBufferFull(Exception):
    # Raised when buffer is full
    pass


class RingBufferEmpty(Exception):
    # Raised when buffer is empty
    pass
