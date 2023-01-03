class CPU():
    """Emulates the cpu from the elven communication device"""

    def __init__(self) -> None:
        self.current_cycle = 0
        self.register = 1
        self.signals = []
        self.pixel_rows = ""

    def cycle(self):
        """A clock cycle of the CPU"""
        self.current_cycle += 1
        # Send signals at the right time
        if self.current_cycle % 40 == 20:
            self.signals.append(self.register * self.current_cycle)
        # Draw a pixel (#) if register is at the pixel position +- 1
        self.pixel_pos = self.current_cycle % 40 - 1
        if abs(self.pixel_pos - self.register) <= 1:
            self.pixel_rows += "#"
        else:
            self.pixel_rows += " "

    def execute(self, instruction: str):
        """Execute an instruction which may take multiple cycles"""
        if instruction.startswith("addx"):
            self.cycle()
            self.cycle()
            self.register += int(instruction.split()[-1])
        elif instruction.startswith("noop"):
            self.cycle()


def main():
    emulator = CPU()
    with open("Excercises/10/input.txt") as file:
        for line in file:
            emulator.execute(line)
    print(sum(emulator.signals))
    print(emulator.current_cycle)
    for ix in range(0, 240, 40):
        print(emulator.pixel_rows[ix: ix + 40])


if __name__ == "__main__":
    main()
