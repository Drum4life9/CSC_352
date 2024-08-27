
from environments import XYEnvironment, Wall, Obstacle, Toy, Agent, Box
import random
from dataclasses import dataclass
import os
from time import sleep


@dataclass(frozen=True, order=True)
class ToyVacuumState:
    width: int
    height: int
    agent: tuple[int, int]
    obstacles: tuple[tuple[int, int], ...]
    toys: tuple[tuple[int, int], ...]
    box: tuple[int, int]
    agent_toys: int
    max_toys: int

    def display(self):
        for y in range(self.height):
            for x in range(self.width):
                if (x, y) == self.agent:
                    print('V', end=" ")
                elif (x, y) in self.obstacles:
                    print('#', end=" ")
                elif (x, y) in self.toys:
                    print('T', end=" ")
                elif (x, y) == self.box:
                    print('B', end=" ")
                elif x == 0 or x == self.width - 1:
                    print('|', end=" ")
                elif y == 0 or y == self.height - 1:
                    print('-', end=" ")
                else:
                    print('.', end=" ")
            print()
        print('toys in inv: ' + str(self.agent_toys))


class ToyVacuumGrid(XYEnvironment):

    def __init__(self, width, height, toy_chance, max_toys=None):
        super().__init__(width, height)

        self.agent_toys = 0


        # walls around the exterior
        self.add_walls()


        while (len(self.things) == 2 * width + 2 * (height - 2)):
            # add the box to the room first
            bx = random.randrange(1, width - 1)
            by = random.randrange(1, height - 1)
            self.add_thing(Box(), (bx, by))
        if width >= 8:
            # arrange some obstacles.
            for i in range(1, int(width) // 2):
                self.add_thing(Obstacle(), (i, 3))
                self.add_thing(Obstacle(), (width - i - 1, height - 4))

        # toss in some toys, according to the chance of a square getting a toy
        for _ in range(int(width * height * toy_chance)):
            self.add_thing(Toy(), (random.randrange(1, width - 1), random.randrange(1, height - 1)), empty_only=True)

        if max_toys is None:
            self.max_toys = sum(1 for d in self.things if isinstance(d, Toy))
        else:
            self.max_toys = max_toys

    def thing_classes(self):
        return [Wall, Toy, Obstacle, Agent, Box]

    def percept(self, agent):
        # the agent can see the entire environment. How does this work:
        return ToyVacuumState(width=self.width, height=self.height,
                       agent=self.agents[0].location,
                       obstacles=tuple([o.location for o in self.things if isinstance(o, Obstacle)]),
                       toys=tuple([d.location for d in self.things if isinstance(d, Toy)]),
                       box=[b.location for b in self.things if isinstance(b, Box)][0],
                       agent_toys=self.agent_toys,
                       max_toys=self.max_toys)

    def execute_action(self, agent, action):
        if action == 'PickUp':
            # get any toys at the current location
            toy_list = self.list_things_at(agent.location, Toy)
            if toy_list:
                # gets the toy from the environment
                toy = toy_list[0]
                # remove the toy from the environment
                self.delete_thing(toy)
                self.agent_toys += 1
        if action == 'Drop':
            # gets any items at the current square (like another toy)
            cur_square = self.list_things_at(agent.location)

            # if we have toys in our inventory
            if cur_square and isinstance(cur_square[0], Box) and self.agent_toys > 0:
                agent.performance += 100
                self.agent_toys = 0
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
        return len([d for d in self.things if isinstance(d, Toy)]) == 0 and self.agent_toys == 0

    def display(self, s, action):
        sleep(0.5)
        os.system('clear')
        print(f'step {s}: action {action}')
        self.agents[0].program.show_state()
