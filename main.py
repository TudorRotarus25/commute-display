#!/usr/bin/env python3
import os
import serial
import time
from datetime import datetime
from dotenv import load_dotenv
from context import context
from utils import printer, api


context = context.Context()


def write_state_to_screen(connection):
    """
    We'll print the state to the screen only if the state was modified since the last print (state is dirty)

    :param connection: serial.Serial
    :return: void
    """
    if context.get_is_state_dirty():
        print("Printing the screen")
        printer.print_screen(connection, context.get_clock_value(), context.get_lines())
        context.reset_state()


def get_timetable_string(index: int, line: str, due_time: str):
    name = f" {line}" if len(line) == 2 else line
    return f"{index + 1} {name}|{due_time}"


def refresh_time():
    now = datetime.now()
    clock_time = now.strftime("%H:%M")
    context.set_clock_value(clock_time)


def refresh_timetable():
    if context.should_update_timetable():
        print("Updating the timetable")
        busses_data = api.get_bus_info()
        lines = [get_timetable_string(i, x["line"], x["due_time"]) for i, x in enumerate(busses_data)]

        context.set_lines(lines)
        context.mark_timetable_updated()


def refresh_not_operating():
    context.set_lines([
        "Not operating"
    ])


def is_update_period():
    """
    We only want to display bus timetables between 7am and 9am
    :return: void
    """
    now = datetime.now()

    if 7 <= now.hour <= 9:
        return True

    return False


if __name__ == '__main__':
    load_dotenv()

    arduino_address = os.environ.get("ARDUINO_ADDRESS", "")

    with serial.Serial(arduino_address, 9600, timeout=1) as ser:
        ser.flushInput()
        time.sleep(1)

        while True:
            refresh_time()

            if is_update_period():
                refresh_timetable()
            else:
                refresh_not_operating()

            write_state_to_screen(ser)

            time.sleep(5)
