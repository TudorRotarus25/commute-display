

def write_to_serial(connection, string_value):
    connection.write(f"{string_value}\n".encode())


def print_screen(connection, clock_value, lines):
    write_to_serial(connection, "CLEAR")
    write_to_serial(connection, f"CLOCK{clock_value}")
    for line in lines:
        write_to_serial(connection, line)
