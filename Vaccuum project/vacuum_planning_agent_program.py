from search import Problem, SimpleProblemSolvingAgentProgram, astar_search
from vacuum_grid import VGState


class VacuumGridProblem(Problem):
    def __init__(self, initial: VGState, goal=None):
        super().__init__(initial, goal)
        self.width = initial.width
        self.height = initial.height
        print('initial problem state')
        initial.display()

    def actions(self, state: VGState):
        cur_loc = state.agent
        acts = ['Suck']
        left = (cur_loc[0]-1, cur_loc[1])
        right = (cur_loc[0]+1, cur_loc[1])
        up = (cur_loc[0], cur_loc[1]-1)
        down = (cur_loc[0], cur_loc[1]+1)
        if left not in state.obstacles and self.is_inbounds(left):
            acts.append('Left')
        if right not in state.obstacles and self.is_inbounds(right):
            acts.append('Right')
        if up not in state.obstacles and self.is_inbounds(up):
            acts.append('Up')
        if down not in state.obstacles and self.is_inbounds(down):
            acts.append('Down')

        return acts

    def result(self, state: VGState, action: str):
        """Return the state that results from executing the given
        action in the given state. The action must be one of
        self.actions(state)."""

        loc = state.agent

        if action == 'Suck' and state.agent in state.dirts:
            dirts = list(state.dirts)
            dirts.remove(state.agent)
            return VGState(width=state.width, height=state.height, agent=loc,
                           obstacles=state.obstacles, dirts=tuple(dirts))

        new_loc = None
        if action == 'Left':
            new_loc = (loc[0]-1, loc[1])
        elif action == 'Right':
            new_loc = (loc[0]+1, loc[1])
        elif action == 'Up':
            new_loc = (loc[0], loc[1]-1)
        elif action == 'Down':
            new_loc = (loc[0], loc[1]+1)
        else:
            new_loc = (loc[0], loc[1])

        if not self.is_inbounds(new_loc) or new_loc in state.obstacles:
            new_loc = loc

        return VGState(width=state.width, height=state.height, agent=new_loc,
                       obstacles=state.obstacles, dirts=state.dirts)

    def goal_test(self, state):
        return len(state.dirts) == 0

    def is_inbounds(self, loc: tuple[int, int]) -> bool:
        """Check if loc is inside the walls"""
        x, y = loc
        return 0 < x < self.height - 1 and 0 < y < self.width - 1


class VacuumPlanningAgentProgram(SimpleProblemSolvingAgentProgram):
    def __init__(self):
        super().__init__()

    def update_state(self, percept: VGState):
        # Replace our stored state with the new one. We are assuming that the percept
        # is a full description of the environment
        self.state = percept

    def formulate_problem(self):
        return VacuumGridProblem(self.state)

    def search(self, problem):
        return astar_search(problem, lambda n: 10*len(n.state.dirts)).solution()

    def show_state(self):
        self.state.display()
