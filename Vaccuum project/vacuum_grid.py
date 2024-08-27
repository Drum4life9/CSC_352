
from environments import XYEnvironment, Wall, Obstacle, Dirt, Agent
import random
from dataclasses import dataclass
import os
from time import sleep


@dataclass(frozen=True, order=True)
class VGState:
    width: int
    height: int
    agent: tuple[int, int]
    obstacles: tuple[tuple[int, int], ...]
    dirts: tuple[tuple[int, int], ...]

    def display(self):
        for y in range(self.height):
            for x in range(self.width):
                if (x, y) == self.agent:
                    print('V', end=" ")
                elif (x, y) in self.obstacles:
                    print('C', end=" ")
                elif (x, y) in self.dirts:
                    print('#', end=" ")
                elif x == 0 or x == self.width - 1:
                    print('|', end=" ")
                elif y == 0 or y == self.height - 1:
                    print('-', end=" ")
                else:
                    print('.', end=" ")
            print()


class VacuumGrid(XYEnvironment):
    def __init__(self, width, height):
        super().__init__(width, height)

        # walls around the exterior
        self.add_walls()

        # arrange some obstacles.
        for i in range(1, width // 2):
            self.add_thing(Obstacle(), (i, 3))
            self.add_thing(Obstacle(), (width - i - 1, height - 4))

        # toss in some dirt
        for _ in range(width * height // 4):
            self.add_thing(Dirt(), (random.randrange(1, width - 1), random.randrange(1, height - 1)), empty_only=True)

    def thing_classes(self):
        return [Wall, Dirt, Obstacle, Agent]

    def percept(self, agent):
        # the agent can see the entire environment. How does this work:
        return VGState(width=self.width, height=self.height,
                       agent=self.agents[0].location,
                       obstacles=tuple([o.location for o in self.things if isinstance(o, Obstacle)]),
                       dirts=tuple([d.location for d in self.things if isinstance(d, Dirt)]))

    def execute_action(self, agent, action):
        if action == 'Suck':
            dirt_list = self.list_things_at(agent.location, Dirt)
            if dirt_list:
                dirt = dirt_list[0]
                agent.performance += 1
                self.delete_thing(dirt)
        else:
            new_loc = None
            if action == 'Left':
                new_loc = (agent.location[0]-1, agent.location[1])
            elif action == 'Right':
                new_loc = (agent.location[0]+1, agent.location[1])
            elif action == 'Up':
                new_loc = (agent.location[0], agent.location[1]-1)
            elif action == 'Down':
                new_loc = (agent.location[0], agent.location[1]+1)

            if new_loc and (not self.some_things_at(new_loc, Obstacle)
                            and not self.some_things_at(new_loc, Wall)):
                agent.location = new_loc

    def is_done(self):
        return len([d for d in self.things if isinstance(d, Dirt)]) == 0

    def display(self, s, action):
        sleep(0.5)
        os.system('clear')
        print(f'step {s}: action {action}')
        self.agents[0].program.show_state()
