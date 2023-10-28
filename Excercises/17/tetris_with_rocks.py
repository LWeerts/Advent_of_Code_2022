import numpy as np


class PlayingField():
    # rocks = (
    #     np.array(tuple("####")).reshape(1, 4),
    #     np.array(tuple(".#.###.#.")).reshape((3, 3)),
    #     np.array(tuple("..#..####")).reshape((3, 3)),
    #     np.array(tuple("####")).reshape((4, 1)),
    #     np.array(tuple("####")).reshape((2, 2))
    # )
    rocks = (
        np.array(tuple("1111"), dtype=np.int32).reshape(1, 4),
        np.array(tuple("010111010"), dtype=np.int32).reshape((3, 3)),
        np.array(tuple("111001001"), dtype=np.int32).reshape((3, 3)),
        np.array(tuple("1111"), dtype=np.int32).reshape((4, 1)),
        np.array(tuple("1111"), dtype=np.int32).reshape((2, 2))
    )

    def __init__(self, filename) -> None:
        # self.rock_chart = np.full((10000, 7), fill_value=".", dtype="U1")
        # self.rock_chart[500, 6] = "#
        self.rock_chart = np.zeros((10000, 7), dtype=np.uint8)
        # self.rock_chart[500, 6] = 1  # Test
        self.rock_counter: int = 0
        self.falling_rock = np.zeros((10000, 7), dtype=np.uint8)
        with open(filename) as file:
            self.wind_chart = file.readline().strip()
        self.wind_counter = 0

    def highest_rock(self) -> int:
        all_rock_locations = np.where(self.rock_chart == 1)
        if len(all_rock_locations[0]) == 0:
            return 0
        return all_rock_locations[0][-1] + 1  # for counting from 0

    def get_rock(self) -> np.ndarray:
        rock = self.rocks[self.rock_counter]
        self.rock_counter = (self.rock_counter + 1) % 5
        return rock

    def spawn_rock(self) -> None:
        # NOTE to self, spawning too low!



        # Spawn new rock 3 spaces above highest rock
        altitude = self.highest_rock() + 3
        rock = self.get_rock()
        self.falling_rock = np.zeros((10000, 7), dtype=np.uint8)
        self.falling_rock[
            altitude: altitude + rock.shape[0],
            2: 2 + rock.shape[1]
        ] = rock
        # print(f"new rock: \n{self.falling_rock[:10, :]}")

    def move_down(self) -> bool:
        """Moves the falling rock down and checks for collisions

        Rolls falling_rock down and checks for overlap with rock_chart.
        If collision occurred, returns False (did not move the rock).
        If no collision occurred, overwrites falling_rock with the rolled
        array and returns True.
        """
        rock_down = np.roll(self.falling_rock, -1, axis=0)
        if (
            np.any(rock_down * self.rock_chart == 1)
            or np.any(rock_down[-1, :] == 1)
        ):
            # Roll causes collision, thus roll back
            # Or rolled over to other side, thus rock reached bottom
            # Can also be done with a np.sum

            self.rock_chart[self.falling_rock == 1] = 1
            # self.rock_chart = self.rock_chart + self.falling_rock
            return False
        self.falling_rock = rock_down
        return True

    def get_wind(self) -> str:
        wind = self.wind_chart[self.wind_counter]
        self.wind_counter = (self.wind_counter + 1) % len(self.wind_chart)
        return wind

    def move_left_right(self) -> bool:
        """Moves the falling rock side to side and checks for rollover.

        Rolls falling_rock and checks if the result has any part of the
        rock rolled over to the other side of the array.
        If rollover occurred or part of the shifted rock overlaps with
        rock_chart, roll is not applied to falling_rock and
        returns False
        If no rollover occurred, roll is applied and returns True.
        """
        wind_dir = 1 if self.get_wind() == '>' else -1
        rock_shifted = np.roll(self.falling_rock, wind_dir, axis=1)
        rollover_side = 0 if wind_dir == 1 else -1
        if (
            np.sum(rock_shifted[:, rollover_side]) > 0
            or np.any(rock_shifted * self.rock_chart == 1)
        ):
            return False
        self.falling_rock = rock_shifted
        return True

    def play_turn(self, amount: int = 1) -> None:
        with np.printoptions(threshold=np.inf):
            for _ in range(amount):
                move_success = True
                self.spawn_rock()
                while move_success:
                    self.move_left_right()
                    # print(f"falling rock: \n{self.falling_rock[:25, :]}")
                    move_success = self.move_down()
                    # print(f"falling rock: \n{self.falling_rock[:25, :]}")

    def write_field(self):
        with open("output_field.txt", 'w') as file:
            np.savetxt(file, self.rock_chart[self.highest_rock()::-1, :],
                       "%1i")


def main():
    pf = PlayingField("Excercises/17/input.txt")
    # print(pf.highest_rock())
    # for _ in range(6):
    #     print(pf.get_rock())
    pf.play_turn(2022)
    print(f"highest rock = {pf.highest_rock()}")
    pf.write_field()


if __name__ == "__main__":
    main()
