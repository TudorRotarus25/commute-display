import time


class Context:
    TIMETABLE_REFRESH_INTERVAL_SECONDS = 60

    def __init__(self):
        self._is_state_dirty = False

        self._clock = ""
        self._lines = []
        self._timetable_last_time_updated = 0

    def get_is_state_dirty(self):
        return self._is_state_dirty

    def reset_state(self):
        self._is_state_dirty = False

    def get_clock_value(self):
        return self._clock

    def set_clock_value(self, value: str):
        if value != self._clock:
            self._clock = value
            self._is_state_dirty = True

    def get_lines(self):
        return self._lines

    def set_lines(self, lines):
        if lines != self._lines:
            self._lines = lines
            self._is_state_dirty = True

    def should_update_timetable(self):
        return time.time() - self._timetable_last_time_updated > self.TIMETABLE_REFRESH_INTERVAL_SECONDS

    def mark_timetable_updated(self):
        self._timetable_last_time_updated = time.time()
