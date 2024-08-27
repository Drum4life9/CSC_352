from search import Problem, SimpleProblemSolvingAgentProgram, astar_search
from vacuum_toy_grid import ToyVacuumState


class ToyVacuumGridProblem(Problem):
    def __init__(self, initial: ToyVacuumState, goal=None):
        super().__init__(initial, goal)
        self.width = initial.width
        self.height = initial.height
        print('initial problem state')
        initial.display()

    def actions(self, state: ToyVacuumState):
        cur_loc = state.agent
        acts = []
        left = (cur_loc[0] - 1, cur_loc[1])
        right = (cur_loc[0] + 1, cur_loc[1])
        up = (cur_loc[0], cur_loc[1] - 1)
        down = (cur_loc[0], cur_loc[1] + 1)

        if cur_loc in state.toys and state.agent_toys < state.max_toys:
            acts.append('PickUp')
        if cur_loc == state.box and (state.agent_toys == state.max_toys or len(state.toys) == 0):
            acts.append('Drop')
        if left not in state.obstacles and self.is_inbounds(left):
            acts.append('Left')
        if right not in state.obstacles and self.is_inbounds(right):
            acts.append('Right')
        if up not in state.obstacles and self.is_inbounds(up):
            acts.append('Up')
        if down not in state.obstacles and self.is_inbounds(down):
            acts.append('Down')
        return acts

    def result(self, state: ToyVacuumState, action: str):
        """Return the state that results from executing the given
        action in the given state. The action must be one of
        self.actions(state)."""

        loc = state.agent

        if action == 'PickUp':
            toys = list(state.toys)
            toys.remove(state.agent)
            return ToyVacuumState(width=state.width, height=state.height, agent=loc,
                                  obstacles=state.obstacles, toys=tuple(toys),
                                  box=state.box, agent_toys=state.agent_toys + 1,
                                  max_toys=state.max_toys)
        if action == 'Drop':
            return ToyVacuumState(width=state.width, height=state.height, agent=loc,
                                  obstacles=state.obstacles, toys=state.toys, box=state.box,
                                  agent_toys=0, max_toys=state.max_toys)
        new_loc = None
        if action == 'Left':
            new_loc = (loc[0] - 1, loc[1])
        elif action == 'Right':
            new_loc = (loc[0] + 1, loc[1])
        elif action == 'Up':
            new_loc = (loc[0], loc[1] - 1)
        elif action == 'Down':
            new_loc = (loc[0], loc[1] + 1)
        else:
            new_loc = (loc[0], loc[1])

        if not self.is_inbounds(new_loc) or new_loc in state.obstacles:
            new_loc = loc

        return ToyVacuumState(width=state.width, height=state.height, agent=new_loc,
                              obstacles=state.obstacles, toys=state.toys, box=state.box, agent_toys=state.agent_toys,
                              max_toys=state.max_toys)

    def goal_test(self, state):
        return len(state.toys) == 0 and state.agent_toys == 0

    def is_inbounds(self, loc: tuple[int, int]) -> bool:
        """Check if loc is inside the walls"""
        x, y = loc
        return 0 < x < self.height - 1 and 0 < y < self.width - 1


def get_heuristic(state):
    if (state.agent_toys == state.max_toys) or len(state.toys) == 0:
        return 5 * (abs(state.agent[0] - state.box[0]) +
                abs(state.agent[1] - state.box[1]))
    return 10 * len(state.toys)


class ToyVacuumPlanningAgentProgram(SimpleProblemSolvingAgentProgram):
    def __init__(self):
        super().__init__()

    def update_state(self, percept: ToyVacuumState):
        # Replace our stored state with the new one. We are assuming that the percept
        # is a full description of the environment
        self.state = percept

    def formulate_problem(self):
        return ToyVacuumGridProblem(self.state)

    def search(self, problem):
        return astar_search(problem, lambda n: get_heuristic(n.state)).solution()

    def show_state(self):
        self.state.display()


'''
+ distance_to_box(n.state) if (n.state.agent_toys == n.state.max_toys or len(n.state.toys) == 0)
                                                    else 0

'''
