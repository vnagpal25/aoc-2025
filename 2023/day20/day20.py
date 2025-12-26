import sys
from collections import deque
import math

def find_inputs(switches, key):
  inputs = []
  for i, (_, _, o_s) in switches.items():
    if key in o_s:
      inputs.append(i)
  return inputs


def main():
  with open(sys.argv[1], 'r') as file:
    lines = file.read().strip().splitlines()

  # will hold keys which represent module
  # there values are a 3 tuple (type of module (& or %), state (on or off or ''), [outputs])
  io_switches = {}

  # Parse input
  for line in lines:
    if line.startswith("broadcaster"):
      _, switches = line.split(' -> ')
      start_switches = [(el.strip(), 'broadcaster', 'lo')
                        for el in switches.split(',')]
    elif line.startswith("%"):
      input, outputs = line[1:].split(' -> ')
      outputs = [el.strip() for el in outputs.split(',')]
      io_switches[input] = ('%', 'off', outputs)
    elif line.startswith('&'):
      input, outputs = line[1:].split(' -> ')
      outputs = [el.strip() for el in outputs.split(',')]
      io_switches[input] = ('&', '', outputs)
  
  # keys are conjunction module names, and values are inputs to those modules
  conjunction_map = {}
  for i, (type, _, _) in io_switches.items():
    if type == '&':
      'Find the switches that have i in their outputs'
      inputs = find_inputs(io_switches, i)
      conjunction_map[i] = {input: 'lo' for input in inputs}

  cycle_tracker = []
  total_hi = total_lo = 0
  presses = 0
  state_map = {'on': ('off', 'lo'), 'off': ('on', 'hi')}
  (feed, ) = [name for name, (_, _, out) in io_switches.items() if 'rx' in out]
  # feed is a conjunction module, to send a low pulse, it needs to remember high pulses from all of its feeders
  feeders = [name for name, (_, _, out) in io_switches.items() if feed in out]
  # feeders need to send high pulses
  # assumption here is that they do this on a regular periodic basis
  # take the least common multiple of when they send high pulses

  lengths = {name:None for name in feeders}
  while True:
    # starting swithces recieve low pulses from broadcaster
    q = deque(start_switches)

    # hi pulses start as 0 lo pulses start as 1 because of broadcaster
    hi_pulses = 0
    lo_pulses = 1

    # answer to part 1
    if presses == 1000:
      print(f'Answer to part 1: {total_hi * total_lo}')
    
    # increment presses
    presses += 1

    # while there are still pulses to be sent
    while q:
      # key is the switch that the pulse is being sent to 
      # source is the source switch
      # pulse type is hi or lo
      key, source, pulse_type = q.popleft()

      if pulse_type == 'hi':
        hi_pulses += 1
      else:
        lo_pulses += 1

      # part 2 stuff
      if key == feed and pulse_type == 'hi':
        # record lengths
        if not lengths[source]:
          lengths[source] = presses
        
        # if we have seen all the inputs to the feed
        # lets take the lcm of thse lengths
        if all(lengths.values()):
          print(f'Answer to part 2: {math.lcm(*lengths.values())}')
          exit(0)

      # switch doesn't have any outputs
      if key not in io_switches:
        continue
      
      # type of switch, state of switch (on or off), and list of outputs
      type, state, outputs = io_switches[key]

      # flip flop
      if type == '%' and pulse_type == 'lo':
        # get updated state and pulse
        state, pulse_to_send = state_map[state]

        # update the state
        io_switches[key] = (type, state, outputs)

        # add output pulses to queue
        for output in outputs:
          q.append((output, key, pulse_to_send))

      # conjunction module
      elif type == '&':
        # update pulse type in cache
        conjunction_map[key][source] = pulse_type

        # if all of them are remembered to be hi pulses send a lo pulse
        if list(conjunction_map[key].values()) == ['hi'] * len(conjunction_map[key].values()):
          pulse_to_send = 'lo'
        else:
        # else send a hi pulse
          pulse_to_send = 'hi'

        # add output pulses to queue
        for output in outputs:
          q.append((output, key, pulse_to_send))

    # update total pulse counts
    total_lo += lo_pulses
    total_hi += hi_pulses


if __name__ == '__main__':
  main()
