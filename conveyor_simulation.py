import random
import argparse

class Worker:
    """
    Represents a worker that can hold components and assemble them into products.
    """

    def __init__(self, time_to_build=4, components=["A", "B"]):
        self.components = {component:0 for component in components} 
        self.time_to_build = time_to_build
        self.time_remaining = time_to_build

    def take_or_place_item(self, slot):
        # Place a finished product if the worker has all components, has finished assembling and the slot is empty
        if slot == " " and self.time_remaining == 0 and sum(self.components.values()) == len(self.components):
            # reset after replacing the finished product
            self.components = {component:0 for component in self.components}
            self.time_remaining = self.time_to_build 
            return "P"
        elif slot in self.components and self.components[slot] == 0:
            # Take a component if there's a free hand
            self.components[slot] += 1
            return " " 

        # No action taken
        return None
    
    # Assemble the product if all components are in hand
    def assemble(self):
        if sum(self.components.values()) == len(self.components) and self.time_remaining > 0:
            self.time_remaining -= 1

class Station:
    """
    A station containing multiple workers that can assemble products.
    """

    def __init__(self, num_workers_per_station=2, time_to_build=4, components=["A", "B"]):
        self.workers = [Worker(time_to_build=time_to_build, components=components) for _ in range(num_workers_per_station)]
        self.slot = " "

    # Process the slot
    def process_slot(self):
        # the action_taken variable is used to allow only one worker to take or place an item
        action_taken = False
        for worker in self.workers:
            # assemblying the product  needs to be done regardless of whether the worker takes or places an item
            worker.assemble()
            if not action_taken:
                result = worker.take_or_place_item(self.slot)
                # if the worker takes or places an item the an action is taken and the item at the slot is updated
                if result is not None: 
                    self.slot = result
                    action_taken = True

class Conveyor:
    """
    Simulates a conveyor belt system composed of multiple stations.
    """

    def __init__(self, num_stations=3, num_workers_per_station=2, time_to_build=4, debug=False, components=["A", "B"]):
        self.stations = [Station(num_workers_per_station=num_workers_per_station,time_to_build=time_to_build, components=components) for _ in range(num_stations)]
        self.finished_products = 0
        self.missed = {component : 0 for component in components}
        self.debug = debug

    def add_new_item(self, item):
        # Shift items down the conveyor belt
        for i in range(len(self.stations) - 1, 0, -1):
            self.stations[i].slot = self.stations[i-1].slot
        self.stations[0].slot = item

        if self.debug:
            with open("debug.txt", "a") as f:
                f.write(f"{self} -----processed-----> ")

        # Process each station
        for station in self.stations:
            station.process_slot()

        if self.debug:
            with open("debug.txt", "a") as f:
                f.write(f"{self}\n")

        # Check what type of item is leaving the conveyor
        leaving_item = self.stations[-1].slot
        if leaving_item == "P":
            self.finished_products += 1

        if leaving_item in self.missed:
            self.missed[leaving_item] += 1

    def __repr__(self):
        return " | ".join(str(station.slot) for station in self.stations)

if __name__ == '__main__':
    
    # Parse arguments
    parser = argparse.ArgumentParser(description='Conveyor Belt Simulation')
    parser.add_argument('--iterations', type=int, default=100, help='Number of iterations to run the simulation')
    parser.add_argument('--components', type=str, nargs='+', default=["A", "B"], help='Components to use in the simulation')
    parser.add_argument('--chance', type=float, nargs='+', default=[1/3], help='Chance of a component being added to the conveyor belt')
    parser.add_argument('--stations', type=int, default=3, help='Number of stations on the conveyor')
    parser.add_argument('--workers', type=int, default=2, help='Number of workers per station')
    parser.add_argument('--time', type=int, default=4, help='Time to build a finished product')
    parser.add_argument('--debug', action='store_true', help='Print the conveyor belt after each iteration')

    args = parser.parse_args()

    # clear debug file
    if args.debug:
        with open("debug.txt", "w") as f:
            f.write("")
    
    # for this simulation the number of different components must be two
    # however, for flexibility, the code is written to allow for more than two components
    args.components = list(set(args.components))
    if len(args.components) != 2:
        raise ValueError("The number of components must be two")
    
    # checks for valid arguments
    if len(args.chance) == 1:
        args.chance = [args.chance[0] for _ in range(len(args.components))]
    elif len(args.chance) != len(args.components):
        raise ValueError("The number of components and the number of chances must be the same")

    # add the chance of no component being added to the conveyor belt
    args.chance.append(1 - sum(args.chance))

    if args.stations < 1:
        raise ValueError("There must be at least one station")
    
    if args.workers < 2:
        raise ValueError("There must be at least two workers per station")

    if args.time < 1:
        raise ValueError("The time to build a finished product must be at least one")
    
    # Simulation
    conveyor = Conveyor(num_stations=args.stations, num_workers_per_station=args.workers, time_to_build=args.time, debug=args.debug, components=args.components)
    for i in range(args.iterations):

        # Add a new item to the conveyor belt
        new_item = random.choices(args.components + [" "], weights=args.chance)[0]

        conveyor.add_new_item(new_item)
        

    print(f"Finished products: {conveyor.finished_products}")
    for component in conveyor.missed:
        print(f"Missed {component}s: {conveyor.missed[component]}")