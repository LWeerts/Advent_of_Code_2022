
class Valve():
    def __init__(self, name, flow, tunnels) -> None:
        self.name = name
        self.flow = flow
        self.tunnels = tunnels
        self.open = False


class PlayingField():
    def __init__(self) -> None:
        self.valve_dict = self.parse_input()
        self.turn = 0

    def parse_input() -> dict[Valve]:
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


def main():
    pass


if __name__ == "__main__":
    main()
