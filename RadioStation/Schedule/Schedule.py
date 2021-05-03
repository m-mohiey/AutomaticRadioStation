from datetime import datetime, timedelta
from . import ProgramNotFoundException, ProgramScheduleConflictException
from .Program import Program

class Schedule:
    def __init__(self):
        self._lst = list()
        self._position = None
        self.MAX_SILENCE = timedelta(seconds=1)

    def find_soon(self, program_time:datetime=None) -> int:
        if not self._lst:
            return 0
        if self._lst[-1].start <= program_time:
            return len(self._lst)
        for pos, item in enumerate(self._lst):
            if item.start >= program_time:
                return pos
        raise ProgramNotFoundException('No program shcedued at that time')
        
    def _insert_pos(self, program:Program, program_time:datetime) -> int:
        if not (program.start and program_time):
            raise ValueError('Program.start and program_time cannot be both None')
        if program_time:
            program.start = program_time
        return self.find_soon(program.start)
        
    
    def insert_at(self, program:Program, program_time:datetime=None) -> int:
        pos = self._insert_pos(program, program_time)
        current_program = self._lst[pos]
        if (current_program.start == program.start) or (program.start > current_program.start) \
            or (program.start <= current_program.end) or (program.end >= current_program.start) \
                or (program.end <= current_program.end):
            raise ProgramScheduleConflictException('Conflict with current program')
        self._lst.insert(pos, program)
        return pos

    def insert_before(self, program:Program, program_time:datetime=None) -> int:
        pos = self._insert_pos(program, program_time)
        prev_program = self._lst[pos - 1]
        if program.start <= prev_program.end:
            raise ProgramScheduleConflictException('Conflict with previuos program')
        self._lst.insert(pos - 1, program)
        return pos -1

    def insert_after(self, program:Program, program_time:datetime=None) -> int:
        pos = self._insert_pos(program, program_time)
        next_program = self._lst[pos + 1]
        if program.end >= next_program.start:
            raise ProgramScheduleConflictException('Conflict with next program')
        self._lst.insert(pos + 1, program)
        return pos + 1

    def find_next_gap(self) -> (datetime, datetime):
        for current_program, next_program in zip(self._lst, self._lst[1:]):
            if (next_program.start - current_program.end) > self.MAX_SILENCE:
                return (current_program.end, next_program.start)

    def sync(self):
        self._position = self.find_soon(datetime.now())

    def play_next(self) -> Program:
        while True:
            yield self._lst[self._position]
            self._position += 1