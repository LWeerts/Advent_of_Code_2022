
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
        self.valve_dict: dict[str, Valve] = self.parse_input()
        self.turn = 0
        self.position = "AA"

    def parse_input(self) -> dict[Valve]:
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

    def find_path(self, target: str) -> None:
        # connections = self.valve_dict[self.position].tunnels
        distance_list = [[self.position]]
        distance = 0
        while distance < 1000:
            if target in distance_list[distance]:
                break
            for valve in distance_list[distance]:
                connections = self.valve_dict[valve].tunnels
                if distance + 1 == len(distance_list):
                    distance_list.append([])
                distance_list[distance + 1].extend(connections)

            distance += 1


def main():
    field = PlayingField()
    print(field.valve_dict)
    print(field.valve_dict["AA"])


if __name__ == "__main__":
    main()
