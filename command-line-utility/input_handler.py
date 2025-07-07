import argparse
import shlex
from converter import *
from state import *
from hash_cracking import *

def create_hex_parser():
    parser = argparse.ArgumentParser(prog="hex_to_decimal", add_help = False)
    group = parser.add_mutually_exclusive_group(required = True)
    group.add_argument("--hex", nargs = "+", help = "Convert hex values")

    parser.add_argument("--reverse-endian", action="store_true", help="Byte order in final product will be reversed")
    return parser

def create_binary_parser():
    parser = argparse.ArgumentParser(prog="byte_to_decimal", add_help = False)
    group = parser.add_mutually_exclusive_group(required = True)
    group.add_argument("--byte", nargs = "+", help = "Convert binary values")

    parser.add_argument("--reverse-endian", action="store_true", help="Byte order in final product will be reversed")
    return parser

def create_decimal_to_binary_parser():
    parser = argparse.ArgumentParser(prog="decimal_to_byte", add_help = False)
    group = parser.add_mutually_exclusive_group(required = True)
    group.add_argument("--decimal", nargs = "+", help = "Convert decimal values")

    parser.add_argument("--reverse-endian", action="store_true", help="Byte order in final product will be reversed")
    return parser

def create_decimal_to_hex_parser():
    parser = argparse.ArgumentParser(prog="decimal_to_hex", add_help = False)
    group = parser.add_mutually_exclusive_group(required = True)
    group.add_argument("--decimal", nargs = "+", help = "Convert decimal values")

    parser.add_argument("--reverse-endian", action="store_true", help="Byte order in final product will be reversed")
    return parser

def create_ascii_decoder_parser():
    parser = argparse.ArgumentParser(prog="decimal_to_ascii", add_help = False)
    group = parser.add_mutually_exclusive_group(required = True)
    group.add_argument("--decimal", nargs = "+", help = "Convert decimal values to ASCII")

    return parser

def create_hash_cracking_parser():
    parser = argparse.ArgumentParser(prog="hash_cracking", add_help = False)
    group = parser.add_mutually_exclusive_group(required = True)
    group.add_argument("--hash", nargs = "+", help = "Crack hashes using wordlist (dictionary attack)")

    return parser



def handle_input(user_input):
    try:
        parts = shlex.split(user_input)
    except ValueError as e:
        print(f"Input error: {e}")
        return

    if not parts:
        print("Type 'help' for usage.")
        return

    command = parts[0]

    if command == "exit":
        exit(0)
    elif command == "help":
        handle_help()
    elif command == "hex_to_decimal":
        handle_hex_to_decimal(parts[1:])
    elif command == "byte_to_decimal":
        handle_binary_to_decimal(parts[1:])
    elif command == "decimal_to_byte":
        handle_decimal_to_binary(parts[1:])
    elif command == "decimal_to_hex":
        handle_decimal_to_hex(parts[1:])
    elif command == "decimal_to_ascii":
        handle_ascii_decode(parts[1:])
    elif command == "hash_cracking":
        handle_hash_cracking(parts[1:])
    else:
        print(f"Unknown command: {command}. Type 'help' for usage.")



def handle_help():
    help_menu = """
Command structure: 
    [command] [options]
Commands:
    help
        Shows usage of every function
    exit                           
        Exit the tool
    hex_to_decimal 
        --hex <hex/hexes>             Convert hex or hexes to decimal
        --reverse-endian              Byte order in finall product will be reversed
    byte_to_decimal
        --byte <byte/bytes>           Convert byte or bytes to decimal
        --reverse-endian              Byte order in finall product will be reversed
    decimal_to_hex
        --decimal <decimal/decimals>  Convert decimal or decimals to hex
        --reverse-endian              Byte order in finall product will be reversed
    decimal_to_byte
        --decimal <decimal/decimals>  Convert decimal or decimals to byte
        --reverse-endian              Byte order in finall product will be reversed
    decimal_to_ascii
        --decimal <decimal/decimals>  Convert decimal or decimals to ASCII
    hash_cracking 
        --hash <hash/hashes>          Crack hash or hashes via dictionary attack (wordlist is a file called wordlist.txt), also only works if hashing algorithm was SHA1, 
                                      hashes that are going to be broken must be made from passwords of 8 characters
"""
    print(help_menu)

def handle_hex_to_decimal(args):
    parser = create_hex_parser()
    try:
        parsed_args = parser.parse_args(args)
    except SystemExit:
        print("Invalid usage. Type 'help' for command structure.")
        return
    
    state["reverse_endian"] = parsed_args.reverse_endian

    if parsed_args.hex:
        try:
            if (len(parsed_args.hex) == 1):
                result = convert_single_hex(parsed_args.hex[0])
                print(f"{parsed_args.hex[0]} -> {result}")
                print(result)
            else:
                result = convert_multiple_hexes(parsed_args.hex)
                for i in range(len(result)):
                    print(f"{parsed_args.hex[i]} -> {result[i]}")
                sum = ""
                for i in range(len(result)):
                    sum += str(result[i]) + ' '
                print(sum)
        except ValueError:
            print(f"Invalid hex value: {parsed_args.hex}")

def handle_binary_to_decimal(args):
    parser = create_binary_parser()
    try:
        parsed_args = parser.parse_args(args)
    except SystemExit:
        print("Invalid usage. Type 'help' for command structure.")
        return
    
    state["reverse_endian"] = parsed_args.reverse_endian

    if parsed_args.byte:
        try:
            if (len(parsed_args.byte) == 1):
                result = convert_single_byte(parsed_args.byte[0])
                print(f"{parsed_args.byte[0]} -> {result[0]}")
            else:
                result = convert_multiple_bytes(parsed_args.byte)
                for i in range(len(result)):
                    print(f"{parsed_args.byte[i]} -> {result[i][0]}")
                sum = ""
                for i in range(len(result)):
                    sum += str(result[i][0]) + ' '
                print(sum)
        except ValueError:
            print(f"Invalid binary value: {parsed_args.byte}")

def handle_decimal_to_binary(args):
    parser = create_decimal_to_binary_parser()
    try:
        parsed_args = parser.parse_args(args)
    except SystemExit:
        print("Invalid usage. Type 'help' for command structure.")
        return
    
    state["reverse_endian"] = parsed_args.reverse_endian

    if parsed_args.decimal:
        try:
            if (len(parsed_args.decimal) == 1):
                result = convert_single_decimal_to_byte(parsed_args.decimal[0])
                print(f"{parsed_args.decimal[0]} -> {result}")
                print(result)
            else:
                result = convert_multiple_decimal_to_byte(parsed_args.decimal)
                for i in range(len(result)):
                    print(f"{parsed_args.decimal[i]} -> {result[i]}")
                sum = ""
                for i in range(len(result)):
                    sum += str(result[i]) + ' '
                print(sum)
        except ValueError:
            print(f"Invalid decimal value: {parsed_args.decimal}")

def handle_decimal_to_hex(args):
    parser = create_decimal_to_hex_parser()
    try:
        parsed_args = parser.parse_args(args)
    except SystemExit:
        print("Invalid usage. Type 'help' for command structure.")
        return
    
    state["reverse_endian"] = parsed_args.reverse_endian

    if parsed_args.decimal:
        try:
            if (len(parsed_args.decimal) == 1):
                result = convert_single_decimal_to_hex(parsed_args.decimal[0])
                print(f"{parsed_args.decimal[0]} -> {result}")
                print(result)
            else:
                result = convert_multiple_decimal_to_hex(parsed_args.decimal)
                for i in range(len(result)):
                    print(f"{parsed_args.decimal[i]} -> {result[i]}")
                sum = ""
                for i in range(len(result)):
                    sum += str(result[i]) + ' '
                print(sum)
        except ValueError:
            print(f"Invalid decimal value: {parsed_args.decimal}")

def handle_ascii_decode(args):
    parser = create_ascii_decoder_parser()
    try:
        parsed_args = parser.parse_args(args)
    except SystemExit:
        print("Invalid usage. Type 'help' for command structure.")
        return

    if parsed_args.decimal:
        try:
            if (len(parsed_args.decimal) == 1):
                result = single_ascii_decode(parsed_args.decimal[0])
                print(f"{parsed_args.decimal[0]} -> {result}")
                print(result)
            else:
                result = multiple_ascii_decode(parsed_args.decimal)
                for i in range(len(result)):
                    print(f"{parsed_args.decimal[i]} -> {result[i]}")
                sum = ""
                for i in range(len(result)):
                    sum += str(result[i])
                print(sum)
        except ValueError:
            print(f"Invalid decimal value: {parsed_args.decimal}")

def handle_hash_cracking(args):
    parser = create_hash_cracking_parser()
    try:
        parsed_args = parser.parse_args(args)
    except SystemExit:
        print("Invalid usage. Type 'help' for command structure.")
        return

    if parsed_args.hash:
        try:
            if (len(parsed_args.hash) == 1):
                crack_hash(parsed_args.hash[0])
            else:
                for i in range(len(parsed_args.hash)):
                    crack_hash(parsed_args.hash[i])
        except ValueError:
            print(f"Invalid hash value: {parsed_args.hash}")