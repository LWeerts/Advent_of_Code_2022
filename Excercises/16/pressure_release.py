
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
        with open("Excercises/16/input_test.txt") as file:
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

    def find_path(self, target: str) -> int:
        """Finds shortest path in a simple network.

        Uses a dictionary to store each node and its distance.
        All nodes in the 'outer shell' are searched for new connections
        which are then added into the dictionary. 

        Returns:
            int: length of the path to the target
        """
        distance_dict = {self.position: 0}
        distance = 0
        while distance < 1000:
            if target in distance_dict:
                break
            for valve, dist in distance_dict.items():
                if dist != distance:
                    continue
                connections = self.valve_dict[valve].tunnels
                for tunnel in connections:
                    if tunnel in distance_dict:
                        continue
                    distance_dict[tunnel] = distance + 1

            distance += 1
        return distance_dict[target]

    def calc_score(self, target: str) -> int:
        # Calculate what total pressure will be released from target valve
        pass


def main():
    field = PlayingField()
    # print(field.valve_dict)
    # print(field.valve_dict["AA"])
    # print(field.flow_list)



if __name__ == "__main__":
    main()
