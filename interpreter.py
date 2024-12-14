import struct
import json
import sys

def interpreter(input_file, output_file, memory_range):
    with open(input_file, 'rb') as infile:
        binary_data = infile.read()

    memory = {}
    index = 0

    while index < len(binary_data):
        command = binary_data[index]
        if command == 0x6E:  # LOAD_CONST
            params = struct.unpack(">BHHH", binary_data[index:index + 7])
            execute_command(command, params[1:], memory)
            index += 7
        elif command == 0xFB:  # READ_MEM
            params = struct.unpack(">BHH", binary_data[index:index + 5])
            execute_command(command, params[1:], memory)
            index += 5
        elif command == 0xEA:  # WRITE_MEM
            params = struct.unpack(">BHHH", binary_data[index:index + 7])
            execute_command(command, params[1:], memory)
            index += 7
        elif command == 0xAB:  # COMPARE_LT
            params = struct.unpack(">BHHH", binary_data[index:index + 7])
            execute_command(command, params[1:], memory)
            index += 7
        else:
            print(f"Неизвестная команда: {hex(command)}")
            break

    memory_range_start, memory_range_end = memory_range
    result = {hex(i): memory.get(i, 0) for i in range(memory_range_start, memory_range_end)}

    with open(output_file, 'w') as outfile:
        json.dump(result, outfile, indent=4)

def execute_command(command, params, memory):
    if command == 0x2A:  # LOAD_CONST
        const, addr = params
        memory[addr] = const
    elif command == 0xB9:  # READ_MEM
        src_addr, dest_addr = params
        memory[dest_addr] = memory.get(src_addr, 0)
    elif command == 0x65:  # WRITE_MEM
        src_addr, dest_addr = params
        memory[dest_addr] = memory.get(src_addr, 0)
    elif command == 0x13:  # COMPARE_LT
        addr1, addr2, result_addr = params
        memory[result_addr] = 1 if memory.get(addr1, 0) < memory.get(addr2, 0) else 0


if __name__ == "__main__":
    if len(sys.argv) < 5:
        print("Ошибка: недостаточно аргументов. Пример использования:")
        print("python interpreter.py <input_file> <output_file> <memory_range_start> <memory_range_end>")
        sys.exit(1)

    memory_range = (int(sys.argv[3], 16), int(sys.argv[4], 16))
    interpreter(sys.argv[1], sys.argv[2], memory_range)
