import unittest
import struct
from assembler import convert_to_binary, COMMANDS
from interpreter import execute_command

class TestAssembler(unittest.TestCase):

    def test_convert_to_binary_load_const(self):
        command = "LOAD_CONST"
        params = [42, 857, 3]
        expected = struct.pack('>BHHH', 0x2A, 42, 857, 3)
        result = convert_to_binary(command, params)
        self.assertEqual(result, expected, "Ошибка в преобразовании команды LOAD_CONST")

class TestInterpreter(unittest.TestCase):

    def test_execute_read_mem(self):
        memory = {97: 123}
        command = 0xB9
        params = [97, 25]
        execute_command(command, params, memory)
        self.assertEqual(memory[25], 123, "Ошибка выполнения команды READ_MEM")

    def test_execute_write_mem(self):
        memory = {24: 789}
        command = 0x65
        params = [24, 37]
        execute_command(command, params, memory)
        self.assertEqual(memory[37], 789, "Ошибка выполнения команды WRITE_MEM")

    def test_execute_compare_lt(self):
        memory = {10: 5, 45: 7}
        command = 0x13
        params = [10, 45, 25]
        execute_command(command, params, memory)
        self.assertEqual(memory[25], 1, "Ошибка выполнения команды COMPARE_LT")

if __name__ == "__main__":
    unittest.main()
