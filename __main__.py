from .core.core import Core

if __name__ == '__main__':
    program = []
    with open('py-virpu/programs/fib.cor', 'r') as file:
        program = [line.strip() for line in file.readlines()]
    core = Core(program, execute_n=0, visual=True)