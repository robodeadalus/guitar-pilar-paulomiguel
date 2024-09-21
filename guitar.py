#!/usr/bin/env python3

"""
Program: Play the guitar supporting 20 notes on the chromatic scale

1. Support 20 notes on the chromatic scale
    - Have a keyboard string of all the possible keys
    - Have a list of the GuitarString objects
    - Pluck the GuitarString object given the key typed
2. Compute for superposition sample
    - Compute the sum of GuitarString objects
3. Play the sample
4. Advance the simulation
"""

from guitarstring import GuitarString
from stdaudio import play_sample
import stdkeys

if __name__ == "__main__":
    # initialize window
    stdkeys.create_window()

    keyboard = "q2we4r5ty7u8i9op-[=]"
    strings = []
    for i in range(20):
        strings.append(GuitarString(440 * (1.059463 ** (i - 12))))

    plucked = set()

    n_iters = 0
    while True:
        # it turns out that the bottleneck is in polling for key events
        # for every iteration, so we'll do it less often, say every
        # 1000 or so iterations
        if n_iters == 1000:
            stdkeys.poll()
            n_iters = 0
        n_iters += 1

        # check if the user has typed a key; if so, process it
        if stdkeys.has_next_key_typed():
            key = stdkeys.next_key_typed()
            try:
                strings[keyboard.index(key)].pluck()
                plucked.add(strings[keyboard.index(key)])
            except:
                print("Invalid input.")

        # compute the superposition of samples
        sample = 0
        for i in plucked.copy():
            if i.time() <= 220500:
                sample += i.sample()
            else:
                i.tickcount = 0
                plucked.remove(i)

        # play the sample on standard audio
        play_sample(sample)

        # advance the simulation of each guitar string by one step
        for i in plucked:
            i.tick()
