"""
Hack Assembler (Part B)
Student Name: Abhinav Sarda
Roll No: 2501730089
Personal Constant K: 89 (K mod 3 = 2 -> Duplicate label warning)
"""

import os
import sys

COMP_TABLE = {
    "0": "0101010", "1": "0111111", "-1": "0111010",
    "D": "0001100", "A": "0110000", "M": "1110000",
    "!D": "0001101", "!A": "0110001", "!M": "1110001",
    "-D": "0001111", "-A": "0110011", "-M": "1110011",
    "D+1": "0011111", "A+1": "0110111", "M+1": "1110111",
    "D-1": "0001110", "A-1": "0110010", "M-1": "1110010",
    "D+A": "0000010", "A+D": "0000010",
    "D+M": "1000010", "M+D": "1000010",
    "D-A": "0010011", "D-M": "1010011",
    "A-D": "0000111", "M-D": "1000111",
    "D&A": "0000000", "A&D": "0000000",
    "D&M": "1000000", "M&D": "1000000",
    "D|A": "0010101", "A|D": "0010101",
    "D|M": "1010101", "M|D": "1010101",
}

DEST_TABLE = {
    "": "000", "M": "001", "D": "010", "MD": "011",
    "A": "100", "AM": "101", "AD": "110", "AMD": "111",
}

JUMP_TABLE = {
    "": "000", "JGT": "001", "JEQ": "010", "JGE": "011",
    "JLT": "100", "JNE": "101", "JLE": "110", "JMP": "111",
}


def init_symbol_table() -> dict[str, int]:
    symbols = {
        "SP": 0,
        "LCL": 1,
        "ARG": 2,
        "THIS": 3,
        "THAT": 4,
        "SCREEN": 16384,
        "KBD": 24576,
    }
    for i in range(16):
        symbols[f"R{i}"] = i
    return symbols


def strip_comments_and_whitespace(line: str) -> str:
    if "//" in line:
        line = line.split("//", 1)[0]
    return line.strip()


def assemble_lines(raw_lines: list[str]) -> list[str]:
    symbols = init_symbol_table()
    declared_labels: set[str] = set()
    cleaned_instructions: list[str] = []

    # First Pass: resolve (LABEL) ROM addresses & warn on duplicate labels (K mod 3 == 2)
    rom_address = 0
    for line_num, raw_line in enumerate(raw_lines, start=1):
        line = strip_comments_and_whitespace(raw_line)
        if not line:
            continue

        if line.startswith("(") and line.endswith(")"):
            label = line[1:-1].strip()
            if label in declared_labels:
                print(f"Warning (Line {line_num}): Duplicate label '({label})' written twice.")
            else:
                declared_labels.add(label)
                symbols[label] = rom_address
        else:
            cleaned_instructions.append(line)
            rom_address += 1

    # Second Pass: translate instructions to 16-bit Hack machine code
    next_ram_address = 16
    machine_code: list[str] = []

    for inst in cleaned_instructions:
        if inst.startswith("@"):
            symbol = inst[1:].strip()
            if symbol.isdigit():
                address = int(symbol)
            else:
                if symbol not in symbols:
                    symbols[symbol] = next_ram_address
                    next_ram_address += 1
                address = symbols[symbol]
            machine_code.append(f"0{address:015b}")
        else:
            dest, comp, jump = "", inst, ""
            if "=" in comp:
                dest, comp = comp.split("=", 1)
            if ";" in comp:
                comp, jump = comp.split(";", 1)

            dest = dest.strip()
            comp = comp.strip()
            jump = jump.strip()

            c_bits = COMP_TABLE[comp]
            d_bits = DEST_TABLE[dest]
            j_bits = JUMP_TABLE[jump]
            machine_code.append(f"111{c_bits}{d_bits}{j_bits}")

    return machine_code


def assemble_file(input_path: str) -> str:
    with open(input_path, "r", encoding="utf-8") as f:
        raw_lines = f.readlines()

    machine_code = assemble_lines(raw_lines)
    output_path = os.path.splitext(input_path)[0] + ".hack"
    with open(output_path, "w", encoding="utf-8") as f:
        f.write(chr(10).join(machine_code) + chr(10))

    print(f"Assembled {input_path} -> {output_path} ({len(machine_code)} instructions)")
    return output_path


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python assembler.py <input.asm>")
        sys.exit(1)
    assemble_file(sys.argv[1])
