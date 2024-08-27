from vacuum_toy_grid import ToyVacuumGrid
from vacuum_toy_planning_program import ToyVacuumPlanningAgentProgram
from environments import Agent

env = ToyVacuumGrid(10, 10, .2, 10)
agent = Agent(ToyVacuumPlanningAgentProgram())
env.add_thing(agent)
env.run()
print('Final State')
agent.program.show_state()

'''
By leaving the environment constructor at just a width, height, and toy chance,
it's max width and height at a toy chance of .2 is: 

Laptop: 22 * 22
Desktop: 25 * 25

By adding in the optional argument of max_toys to specify the number of max toys the
agent can hold, it's max width height with a toy chance of .2 and max of 10 toys is: 

Laptop: 13 * 13
Desktop: 16 * 16

'''
