import json
import struct
import sys

COMMANDS = {
    "LOAD_CONST": (0x2A, '>BHHH'),    # 3 параметра: A (1 байт), B (2 байта), C (2 байта)
    "READ_MEM":   (0xB9, '>HH'),   # 2 параметра: B (2 байта), C (2 байта)
    "WRITE_MEM":  (0x65, '>HH'),   # 2 параметра: B (2 байта), C (2 байта)
    "COMPARE_LT": (0x13, '>HHH'),  # 3 параметра: B (2 байта), C (2 байта), R (2 байта)
}

def validate_params(params, fmt):
    expected_count = fmt.count('H') + fmt.count('B') - 1  # Учитываем опкод
    if len(params) != expected_count:
        raise ValueError(f"Неверное количество параметров для команды. Ожидается {expected_count}, передано {len(params)}")
    return params

def convert_to_binary(command, params):
    opcode, fmt = COMMANDS[command]
    print(f"Команда: {command}, Операнд: {params}, Формат: {fmt}")  # Отладочный вывод
    validate_params(params, fmt)
    return struct.pack(fmt, opcode, *params)

def assembler(input_file, output_file, log_file):
    # Указание кодировки UTF-8 при открытии файла
    with open(input_file, 'r', encoding='utf-8') as infile:
        commands = infile.readlines()

    binary_data = b''
    log = {}
    address = 0

    for command_line in commands:
        command_line = command_line.strip()
        if command_line:
            parts = command_line.split()
            command = parts[0]
            params = list(map(int, parts[1:]))
            binary = convert_to_binary(command, params)
            binary_data += binary
            log[hex(address)] = {command: params}
            address += len(binary)

    with open(output_file, 'wb') as binfile:
        binfile.write(binary_data)

    with open(log_file, 'w', encoding='utf-8') as logfile:
        json.dump(log, logfile, indent=4)

if __name__ == "__main__":
    assembler(sys.argv[1], sys.argv[2], sys.argv[3])
