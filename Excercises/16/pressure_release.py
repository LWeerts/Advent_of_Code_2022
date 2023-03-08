# Attempted answers: 1777, too low
import time


def memoize(func):
    memo = {}

    def helper(inp1, inp2):
        if (inp1, inp2) not in memo:
            memo[(inp1, inp2)] = func(inp1, inp2)
        return memo[(inp1, inp2)]
    return helper


class Valve():
    def __init__(self, name: str, flow: int, tunnels: list[str]) -> None:
        self.name = name
        self.flow = flow
        self.tunnels = tunnels
        self.open = False

    def __str__(self) -> str:
        return f"{self.name}, {self.flow}, {self.tunnels}, {self.open}"


class PlayingField():
    def __init__(self) -> None:
        self.valve_dict = self.parse_input()
        self.flow_list = self.sort_flow()
        self.turn = 0
        self.position = "AA"

    def parse_input(self) -> dict[str, Valve]:
        valve_dict = {}
        with open("Excercises/16/input.txt") as file:
            for line in file:
                if line == "\n":
                    continue
                split_line = line.split()
                name = split_line[1]
                flow = int(split_line[4].strip("rate=;"))
                tunnels = [tun.strip(",") for tun in split_line[9:]]
                valve_dict[name] = Valve(name, flow, tunnels)
        return valve_dict

    def sort_flow(self) -> list[str, int]:
        """For finding the valves with the largest flow.

        Returns:
            list: tuples of valvename and flow, sorted by flow.
        """
        output = []
        for name, valve in self.valve_dict.items():
            flow = valve.flow
            output.append((name, flow))
        output.sort(key=lambda valve: valve[1], reverse=True)
        return output

    @memoize
    def find_path(self, start: str) -> dict:
        """Finds shortest path in a simple network.

        Uses a dictionary to store each node and its distance.
        All nodes in the 'outer shell' are searched for new connections
        which are then added into the dictionary.

        Returns:
            dict: distance to all other valves
        """
        distance_dict = {start: 0}
        shell = 0
        while len(distance_dict) != len(self.valve_dict) or shell < 1000:
            to_be_added = {}
            for valve, dist in distance_dict.items():
                if dist != shell:
                    continue
                connections = self.valve_dict[valve].tunnels
                for tunnel in connections:
                    if tunnel in distance_dict:
                        continue
                    to_be_added[tunnel] = shell + 1

            shell += 1
            distance_dict.update(to_be_added)
        return distance_dict

    def calc_score(self, target: str) -> tuple[int, int]:
        # Calculate what total pressure will be released from target valve
        distance_dict = self.find_path(self.position)
        distance = distance_dict[target]
        # 30 minutes -1 for opening the valve
        minutes = 29 - distance - self.turn
        if minutes <= 0:  # No time left
            return 0, 0
        flow = self.valve_dict[target].flow
        score = minutes * flow
        return score, distance


def main():
    start = time.perf_counter()
    field = PlayingField()
    # print(field.valve_dict)
    # print(field.valve_dict["AA"])
    # print(field.flow_list)

    total_pressure_released = 0

    while field.turn < 30:
        # Grab 5 promising valves as next targets
        high_flow_valves: list[str] = []
        for name, _ in field.flow_list:
            if len(high_flow_valves) == 5:
                break
            if field.valve_dict[name].open:
                continue
            high_flow_valves.append(name)

        highscore = 0
        target_name = ""
        target_distance = 0
        target_total_pressure = 0
        for target in high_flow_valves:
            total_pressure, distance = field.calc_score(target)
            if distance != 0:
                score = total_pressure / (distance ** 2)
            else:
                score = total_pressure
            if score > highscore:
                highscore = score
                target_name = target
                target_distance = distance
                target_total_pressure = total_pressure
        if highscore == 0:  # No valve can release pressure anymore
            break
        # Move to the target
        field.position = target_name
        field.turn += target_distance + 1  # + 1 for opening the valve
        total_pressure_released += target_total_pressure
        field.valve_dict[target_name].open = True

    print(total_pressure_released)
    end = time.perf_counter()
    print(f"Time taken: {end - start}")


if __name__ == "__main__":
    main()
