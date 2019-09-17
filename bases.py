from random import randrange
from parameters import prefix_path, keyboard, initial_check
import functools
from copy import deepcopy


@functools.total_ordering
class Time(object):
    """Time object , int = ms, list = [min, second, ms], default is 1s."""
    def __init__(self, time):
        if isinstance(time, int) or isinstance(time, float):
            self.ms = round(time)
            minute = self.ms // 60000
            second = (self.ms - minute * 60000) // 1000
            ms = self.ms - minute * 60000 - second * 1000
            self.ll = [minute, second, ms]
        elif isinstance(time, list):
            self.ms = round((time[0] * 60 + time[1]) * 1000 + time[2])
            minute = self.ms // 60000
            second = (self.ms - minute * 60000) // 1000
            ms = self.ms - minute * 60000 - second * 1000
            self.ll = [minute, second, ms]

    def __repr__(self):
        return '{}'.format(self.ll)

    def __add__(self, other):
        if isinstance(other, Time):
            return Time(self.ms + other.ms)
        else:
            return Time(self.ms + Time(other).ms)

    def __truediv__(self, other):
        return Time(self.ms/other)

    def __sub__(self, other):
        if isinstance(other, Time):
            return Time(self.ms - other.ms)
        else:
            return Time(self.ms - Time(other).ms)

    def __mul__(self, other):
        return Time(self.ms*other)

    def __radd__(self, other):
        return Time(self.ms + Time(other))

    def __rmul__(self, other):
        return Time(self.ms*other)

    def __eq__(self, other):
        if isinstance(other, Time):
            return self.ms == other.ms
        else:
            return self.ms == Time(other).ms

    def __lt__(self, other):
        if isinstance(other, Time):
            return self.ms < other.ms
        else:
            return self.ms < Time(other).ms


class TimeList(list):
    def __init__(self, *args):
        if args == ():
            super().__init__(args)
        elif len(args) == 1 and isinstance(args[0], list):
            g = [Time(x) for x in args[0]]
            super().__init__(g)
        else:
            g = [Time(x) for x in args]
            super().__init__(g)

    def insert(self, index, time):
        if isinstance(time, Time):
            super().insert(index, time)
        else:
            super().insert(index, Time(time))

    def append(self, time):
        if isinstance(time, Time):
            return super().append(time)
        else:
            return super().append(Time(time))

    def extend(self, time_list):
        for x in time_list:
            self.append(x)

    def __add__(self, other):
        for i in range(0, len(self)):
            self[i] = self[i] + other
        return self

    def __mul__(self, other):
        for i in range(0, len(self)):
            self[i] = self[i] * other
        return self

    def __sub__(self, other):
        for i in range(0, len(self)):
            self[i] = self[i] - other
        return self

    def __truediv__(self, other):
        for i in range(0, len(self)):
            self[i] = self[i]/other
        return self


def draw(rmobject, start_column='auto'):
    with open(prefix_path+'prefix.imd', 'rb') as fp:
        prefix = fp.read()
    if start_column == 'c':
        lines_list = rmobject.imd()
    else:
        lines_list = rmobject.imd(start_column)
    tot_lines = int.to_bytes(len(lines_list), 4, byteorder='little')

    with open(prefix_path+'drawing_'+str(keyboard)+'k_ez.imd', 'wb') as fp:
        fp.write(prefix)
        fp.write(tot_lines)
        for x in lines_list:
            fp.write(x)
    from ezgo_reader import Imd
    imd = Imd(prefix_path+'drawing_'+str(keyboard)+'k_ez.imd')
    imd.reordering()
    imd.save(prefix_path+'drawing_'+str(keyboard)+'k_ez.imd')
    import os
    os.system('start ' + prefix_path+'drawing_'+str(keyboard)+'k_ez.imd')


class Position(object):
    def __init__(self, values):
        if isinstance(values, list) and len(values) == 1:
            self.v = round(values[0])
        elif isinstance(values, list) and len(values) > 1:
            self.v = [round(x) for x in values]
        elif isinstance(values, int):
            self.v = values
        elif isinstance(values, str) and (values == 'l' or values == 'r'):
            self.v = values
        else:
            self.v = 'f'

    def save(self, fp):
        line = bytearray()
        if isinstance(self.v, list):
            for x in self.v:
                line += int.to_bytes(x, 1, byteorder='little', signed=True)
        elif isinstance(self.v, int):
            line += int.to_bytes(self.v, 1, byteorder='little', signed=True)
        else:
            line += self.v.encode('utf-8')
        length_byte = int.to_bytes(len(line), 1, byteorder='little')
        fp.write(length_byte)
        fp.write(line)

    @staticmethod
    def load(fp):
        length = int.from_bytes(fp.read(1), byteorder='little')
        data = fp.read(length)
        if data == b'f' or data == b'l' or data == b'r':
            return data.decode('utf-8')
        else:
            value = []
            for x in data:
                if x < 128:
                    value.append(x)
                else:
                    value.append(x-256)
            return value

    def choice(self):
        if self.v == 'f':
            return randrange(keyboard)
        elif isinstance(self.v, int):
            return self.v % keyboard
        elif isinstance(self.v, list):
            idx = randrange(len(self.v))
            return self.v[idx] % keyboard
        elif isinstance(self.v, str) and self.v == 'l':
            return randrange(keyboard//2)
        elif isinstance(self.v, str) and self.v == 'r':
            return keyboard - 1 - randrange(keyboard//2)

    def v_l(self):
        if self.v == 'f':
            return set([x for x in range(0, keyboard)])
        elif isinstance(self.v, int):
            return {self.v}
        elif isinstance(self.v, list):
            return set(self.v)
        elif isinstance(self.v, str) and self.v == 'l':
            return set([x for x in range(0, keyboard//2)])
        elif isinstance(self.v, str) and self.v == 'r':
            return set([keyboard - 1 - x for x in range(0, keyboard//2)])

    def __repr__(self):
        return 'P: {}'.format(self.v)


class D(object):
    def __init__(self, start=0, position='free'):
        self.t = Time(start)
        self.p = Position(position)

    def __repr__(self):
        return '{}, {}'.format(self.t, self.p)

    def imd(self, start_column='auto'):
        imd_line = b'\x00\x00' + int.to_bytes(self.t.ms, 4, byteorder='little')
        if isinstance(start_column, int):
            column = start_column
        else:
            column = self.p.choice()
        imd_line += int.to_bytes(column, 1, byteorder='little')
        imd_line += b'\x00\x00\x00\x00'
        return [imd_line, ]

    def save(self, fp):
        name = 'D'.encode('utf-8')
        time_byte = int.to_bytes(self.t.ms, 4, byteorder='little')
        fp.write(name)
        fp.write(time_byte)
        self.p.save(fp)

    @staticmethod
    def load(fp):
        time_ms = int.from_bytes(fp.read(4), byteorder='little')
        p = Position.load(fp)
        return D(time_ms, p)


class H(object):
    def __init__(self, start, end, position='free'):
        self.t = TimeList([start, end])
        self.p = Position(position)

    def __repr__(self):
        return '{}, {}'.format(self.t, self.p)

    def p_check(self):
        return list(self.p.v_l())

    def imd(self, start_column='auto'):
        if isinstance(start_column, int):
            column = start_column
        else:
            column = self.p.choice()
        line = b'\x02\x00' + int.to_bytes(self.t[0].ms, 4, byteorder='little')
        line += int.to_bytes(column, 1, byteorder='little')
        duration = self.t[1].ms - self.t[0].ms
        line += int.to_bytes(duration, 4, byteorder='little')
        return [line, ]

    def save(self, fp):
        name = 'H'
        fp.write(name.encode('utf-8'))
        fp.write(int.to_bytes(self.t[0].ms, 4, byteorder='little'))
        fp.write(int.to_bytes(self.t[1].ms, 4, byteorder='little'))
        Position.save(self.p, fp)

    @staticmethod
    def load(fp):
        # fp.read(1)
        t_start = int.from_bytes(fp.read(4), byteorder='little')
        t_end = int.from_bytes(fp.read(4), byteorder='little')
        value = Position.load(fp)
        return H(t_start, t_end, value)


class T(object):
    def __init__(self, timing, moving, position='free'):
        self.p = Position(position)
        if len(moving) < len(timing):
            self.m = moving
            self.t = TimeList(timing[0:len(self.m)])
        elif len(moving) > len(timing):
            self.t = TimeList(timing)
            self.m = moving[0:len(timing)]
        else:
            self.t = TimeList(timing)
            self.m = moving
        if initial_check:
            self.p.v = self.p_check()

    def __repr__(self):
        return '{}, Start: {}'.format(self.m, self.t[0])

    def p_check(self):
        current_p = 0
        minimum = 0
        maximum = 0
        for move in self.m:
            current_p += move
            if current_p < minimum:
                minimum = deepcopy(current_p)
            if current_p > maximum:
                maximum = deepcopy(current_p)
        available_p = self.p.v_l()
        values = list()
        for x in range(-minimum, keyboard - maximum):
            if x in available_p:
                values.append(x)
        if not values:
            print('Warning. No choices, please update moving or position ')
            return []
        else:
            return values

    def mr(self):
        new_moving = [-x for x in self.m]
        new_timing = list()
        for t in self.t:
            new_timing.append(t.ms)
        return T(new_timing, new_moving, self.p.v)

    def et(self, arg):
        if isinstance(arg, int) or isinstance(arg, float):
            new_arg = []
            for i in range(0, len(self.m)):
                new_arg.append(arg)
            arg = new_arg
        new_moving = list()
        idx = 0
        while idx < len(self.m):
            if self.m[idx] != 0 and arg:
                new_moving.append(round(self.m[idx]*arg[0]))
                arg.pop(0)
            else:
                new_moving.append(self.m[idx])
            idx += 1
        new_timing = list()
        # print(new_moving)
        for t in self.t:
            new_timing.append(t.ms)
        return T(new_timing, new_moving, self.p.v)

    def imd(self, start_column='auto'):
        if len(self.t) == 1 and self.m[0] != 0:
            if isinstance(start_column, int):
                column = start_column
            else:
                possible_position = Position(self.p_check())
                column = possible_position.choice()
            line = b'\x01\x00' + int.to_bytes(self.t[0].ms, 4, byteorder='little')
            line += int.to_bytes(column, 1, 'little')
            line += int.to_bytes(self.m[0], 4, byteorder='little', signed=True)
            return [line, ]
        elif len(self.t) == 1 and self.m[0] == 0:
            print('Format error')
            return []
        elif len(self.t) == 2 and self.m[0] == 0 and self.m[1] == 0:
            print('Format error')
            return []
        else:
            lines = list()
            if isinstance(start_column, int):
                current_column = start_column
            else:
                possible_position = Position(self.p_check())
                current_column = possible_position.choice()
            if self.m[0] == 0:
                line = b'\x62\x00' + int.to_bytes(self.t[0].ms, 4, byteorder='little')
                line += int.to_bytes(current_column, 1, byteorder='little')
                line += int.to_bytes(self.t[1].ms-self.t[0].ms, 4, byteorder='little')
                lines.append(line)
            else:
                line = b'\x61\x00' + int.to_bytes(self.t[0].ms, 4, byteorder='little')
                line += int.to_bytes(current_column, 1, byteorder='little')
                line += int.to_bytes(self.m[0], 4, byteorder='little', signed=True)
                current_column += self.m[0]
                lines.append(line)
                line = b'\x22\x00' + int.to_bytes(self.t[0].ms, 4, byteorder='little')
                line += int.to_bytes(current_column, 1, byteorder='little')
                line += int.to_bytes(self.t[1].ms-self.t[0].ms, 4, byteorder='little')
                lines.append(line)
            for idx in range(1, len(self.t)-1):
                if self.m[idx] == 0:
                    print('Format error.')
                    return []
                else:
                    line2 = b'\x21\x00' + int.to_bytes(self.t[idx].ms, 4, byteorder='little')
                    line2 += int.to_bytes(current_column, 1, byteorder='little')
                    line2 += int.to_bytes(self.m[idx], 4, byteorder='little', signed=True)
                    current_column += self.m[idx]
                    line1 = b'\x22\x00' + int.to_bytes(self.t[idx].ms, 4, byteorder='little')
                    line1 += int.to_bytes(current_column, 1, byteorder='little')
                    line1 += int.to_bytes(self.t[idx+1].ms-self.t[idx].ms, 4, byteorder='little')
                    lines.append(line2)
                    lines.append(line1)
            if self.m[-1] == 0:
                line1 = lines.pop(-1)
                line_end = b'\xa2' + line1[1:]
                lines.append(line_end)
            else:
                line_end = b'\xa1\x00' + int.to_bytes(self.t[-1].ms, 4, byteorder='little')
                line_end += int.to_bytes(current_column, 1, byteorder='little')
                line_end += int.to_bytes(self.m[-1], 4, byteorder='little', signed=True)
                lines.append(line_end)
            return lines

    def save(self, fp):
        name = 'T'
        fp.write(name.encode('utf-8'))
        length = len(self.t)
        fp.write(int.to_bytes(length, 1, byteorder='little'))
        for x in range(0, length):
            fp.write(int.to_bytes(self.t[x].ms, 4, byteorder='little'))
            fp.write(int.to_bytes(self.m[x], 1, byteorder='little', signed=True))
        Position.save(self.p, fp)

    @staticmethod
    def load(fp):
        # fp.read(1)
        length = int.from_bytes(fp.read(1), byteorder='little')
        timing = []
        moving = []
        for x in range(0, length):
            timing.append(int.from_bytes(fp.read(4), byteorder='little'))
            moving.append(int.from_bytes(fp.read(1), byteorder='little', signed=True))
        value = Position.load(fp)
        return T(timing, moving, value)


class B(object):
    def __init__(self, rmobjects, relative_positions, cross=0):
        f_p = relative_positions.index('p')
        relative_positions[0], relative_positions[f_p] = relative_positions[f_p], relative_positions[0]
        rmobjects[0], rmobjects[f_p] = rmobjects[f_p], rmobjects[0]
        self.obj = []
        self.r_p = []
        for i in range(0, len(rmobjects)):
            if isinstance(rmobjects[i], B) and i != 0:
                self.obj.append(rmobjects[i].obj[0])
                self.r_p.append(relative_positions[i])
                for j in range(1, len(rmobjects[i].obj)):
                    self.obj.append(rmobjects[i].obj[j])
                    self.r_p.append(rmobjects[i].r_p[j] + relative_positions[i])
            elif isinstance(rmobjects[i], B) and i == 0:
                self.obj = rmobjects[i].obj
                self.r_p = rmobjects[i].r_p
            else:
                self.obj.append(rmobjects[i])
                self.r_p.append(relative_positions[i])
        self.p = self.obj[0].p
        self.cross = cross
        for i in range(1, len(self.obj)):
            self.obj[i].p = Position('f')
        if initial_check:
            self.p.v = self.p_check()

    def __repr__(self):
        name_list = []
        for x in self.obj:
            if isinstance(x, D):
                name_list.append('D')
            elif isinstance(x, H):
                name_list.append('H')
            elif isinstance(x, T):
                name_list.append('T')
        return '{}, r_p: {}'.format(name_list, self.r_p)

    def mr(self):
        new_obj = []
        new_r_p = []
        for x in self.r_p:
            if x == 'p':
                new_r_p.append(x)
            else:
                new_r_p.append(-x)
        for y in self.obj:
            if isinstance(y, T):
                new_obj.append(y.mr())
            else:
                new_obj.append(y)

        return B(new_obj, new_r_p, self.cross)

    def p_check(self):
        traces_p = []
        r_p = []
        for i in range(0, len(self.obj)):
            if isinstance(self.obj[i], T):
                r_p.append(self.r_p[i])
                local_available_p = self.obj[i].p_check()
                if i == 0:
                    global_available_p = {x for x in local_available_p}
                else:
                    global_available_p = {x-self.r_p[i] for x in local_available_p}
                traces_p.append(global_available_p)
        available_p = self.p.v_l()
        for x in traces_p:
            available_p.intersection_update(x)
        if not available_p:
            print('Warning. No choices, please update relative_positions, or objects ')
            return []
        else:
            values = list(available_p)
            return values

    def get_columns(self, start_column='auto'):
        if isinstance(start_column, int):
            columns = [start_column, ]
        else:
            possible_start = Position(self.p_check())
            columns = [possible_start.choice(), ]
        for i in range(1, len(self.r_p)):
            if self.cross == 0 and columns[0] + self.r_p[i] >= keyboard:
                return []
            elif self.cross == 0:
                columns.append(columns[0] + self.r_p[i])
            elif self.cross == 1:
                columns.append((columns[0] + self.r_p[i]) % keyboard)
            elif self.cross == -1:
                if columns[0] + self.r_p[i] >= 0:
                    column_tot = columns[0] + self.r_p[i]
                else:
                    column_tot = -columns[0] - self.r_p[i]
                column_find = 0
                sign = 1
                while column_tot > 0:
                    column_tot -= 1
                    column_find += 1*sign
                    if column_find == keyboard-1:
                        sign = -1
                    elif column_find == 0:
                        sign = 1
                columns.append(column_find)
        return columns

    def imd(self, start_column='auto'):
        columns = self.get_columns(start_column)
        lines = []
        for i in range(0, len(self.obj)):
            lines += self.obj[i].imd(columns[i])
        return lines

    def save(self, fp):
        name = 'B'
        fp.write(name.encode('utf-8'))
        fp.write(int.to_bytes(self.cross, 1, byteorder='little', signed=True))
        length = len(self.obj)
        fp.write(int.to_bytes(length, 2, byteorder='little'))
        for r_p in self.r_p:
            if r_p == 'p':
                fp.write(int.to_bytes(0, 2, byteorder='little', signed=True))
            else:
                fp.write(int.to_bytes(r_p, 2, byteorder='little', signed=True))
        for x in self.obj:
            x.save(fp)

    @staticmethod
    def load(fp):
        cross = int.from_bytes(fp.read(1), byteorder='little', signed=True)
        length = int.from_bytes(fp.read(2), byteorder='little')
        relative_positions = []
        rmobjects = []
        for i in range(0, length):
            relative_positions.append(int.from_bytes(fp.read(2), byteorder='little', signed=True))
        for i in range(0, length):
            obj_name = fp.read(1).decode('utf-8')
            if obj_name == 'D':
                rmobjects.append(D.load(fp))
            elif obj_name == 'H':
                rmobjects.append(H.load(fp))
            elif obj_name == 'T':
                rmobjects.append(T.load(fp))
        relative_positions[0] = 'p'
        return B(rmobjects, relative_positions, cross)


class R(object):
    def __init__(self, rmobjects, fr_tp='f'):
        self.obj = []
        if not (fr_tp == 'f' or fr_tp == 'l' or fr_tp == 'r' or isinstance(fr_tp, list)):
            raise ValueError('free type should be f, l, or r')
        for x in rmobjects:
            if isinstance(x, D) or isinstance(x, H) or isinstance(x, T) or isinstance(x, B):
                x.p = Position(fr_tp)
                self.obj.append(x)
            elif isinstance(x, R):
                for j in range(0, len(x.obj)):
                    self.obj.append(x.obj[j])
        if initial_check:
            values_list = self.p_check()
            for i in range(len(self.obj)):
                self.update(i, values_list[i])

    def __repr__(self):
        name_list = []
        for x in self.obj:
            if isinstance(x, D):
                name_list.append('D')
            elif isinstance(x, H):
                name_list.append('H')
            elif isinstance(x, T):
                name_list.append('T')
            elif isinstance(x, B):
                name_list.append('B')
        return '{}, {}'.format(name_list, self.obj[0].p)

    def p_check(self):
        values_list = []
        for x in self.obj:
            if isinstance(x, T) or isinstance(x, B):
                values_list.append(x.p_check())
            else:
                values_list.append(x.p.v)
        return values_list

    def update(self, index, free_type_or_values):
        self.obj[index].p.v = free_type_or_values

    def append(self, obj, fr='f'):
        obj.p = Position(fr)
        self.obj.append(obj)

    def pop(self, idx):
        self.obj.pop(idx)

    def save(self, fp):
        name = 'R'
        length = len(self.obj)
        fp.write(name.encode('utf-8'))
        fp.write(int.to_bytes(length, 3, byteorder='little'))
        for i in range(length):
            self.obj[i].save(fp)

    @staticmethod
    def load(fp):
        objs = []
        free_types = []
        length = int.from_bytes(fp.read(3), byteorder='little')
        for i in range(length):
            obj_name = fp.read(1).decode('utf-8')
            if obj_name == 'D':
                objs.append(D.load(fp))
            elif obj_name == 'H':
                objs.append(H.load(fp))
            elif obj_name == 'T':
                objs.append(T.load(fp))
            elif obj_name == 'B':
                objs.append(B.load(fp))
        for x in objs:
            free_types.append(x.p.v)
        rr = R(objs)
        for i in range(len(objs)):
            rr.update(i, free_types[i])
        return rr

    def imd(self, start_column='auto'):
        lines = []
        for x in range(len(self.obj)):
            lines += self.obj[x].imd(start_column)
        return lines


class Pocket(object):
    def __init__(self, *args):
        self.obj = [x for x in args]

    def __repr__(self):
        name_list = []
        for x in self.obj:
            if isinstance(x, D):
                name_list.append('D')
            elif isinstance(x, H):
                name_list.append('H')
            elif isinstance(x, T):
                name_list.append('T')
            elif isinstance(x, R):
                name_list.append('R')
            elif isinstance(x, B):
                name_list.append('B')
            elif isinstance(x, Equiv):
                name_list.append('Equiv')
            elif isinstance(x, Pocket):
                name_list.append('Pocket')
        return '{}'.format(name_list)

    def append(self, rm_obj):
        self.obj.append(rm_obj)

    def pop(self, idx):
        self.obj.pop(idx)

    def save(self, fp):
        fp.write('K'.encode('utf-8'))
        length = len(self.obj)
        fp.write(int.to_bytes(length, 1, byteorder='little'))
        for x in self.obj:
            x.save(fp)

    @staticmethod
    def load(fp):
        length = int.from_bytes(fp.read(1), byteorder='little')
        obj = []
        for i in range(length):
            name = fp.read(1).decode('utf-8')
            if name == 'D':
                obj.append(D.load(fp))
            elif name == 'H':
                obj.append(H.load(fp))
            elif name == 'T':
                obj.append(T.load(fp))
            elif name == 'B':
                obj.append(B.load(fp))
            elif name == 'R':
                obj.append(R.load(fp))
            elif name == 'E':
                obj.append(Equiv.load(fp))
            elif name == 'K':
                obj.append(Pocket.load(fp))
        return Pocket(*obj)

    def __add__(self, other):
        new_args = []
        for x in self.obj:
            new_args.append(x)
        for y in other.obj:
            new_args.append(y)
        return Pocket(*new_args)


class Equiv(Pocket):
    def choice(self):
        idx = randrange(len(self.obj))
        return self.obj[idx]

    def save(self, fp):
        fp.write('E'.encode('utf-8'))
        length = len(self.obj)
        fp.write(int.to_bytes(length, 1, byteorder='little'))
        for x in self.obj:
            x.save(fp)

    @staticmethod
    def load(fp):
        length = int.from_bytes(fp.read(1), byteorder='little')
        obj = []
        for i in range(length):
            name = fp.read(1).decode('utf-8')
            if name == 'D':
                obj.append(D.load(fp))
            elif name == 'H':
                obj.append(H.load(fp))
            elif name == 'T':
                obj.append(T.load(fp))
            elif name == 'B':
                obj.append(B.load(fp))
            elif name == 'R':
                obj.append(R.load(fp))
            elif name == 'K':
                obj.append(Pocket.load(fp))
        return Equiv(*obj)


def retiming(rmobj, time):
    if isinstance(time, int) or isinstance(time, float):
        time = Time(time)
    elif not isinstance(time, Time):
        print('Got a non time-like object.')
        return rmobj
    if isinstance(rmobj, D) or isinstance(rmobj, H) or isinstance(rmobj, T):
        new_rmobj = deepcopy(rmobj)
        new_rmobj.t = new_rmobj.t + time
        return new_rmobj
    elif isinstance(rmobj, B):
        new_rmobj = deepcopy(rmobj)
        for x in new_rmobj.obj:
            x.t = x.t + time
        return new_rmobj
    elif isinstance(rmobj, R):
        new_objs = []
        for x in rmobj.obj:
            new_objs.append(retiming(x, time))
        new_r = R(new_objs)
        for i in range(len(rmobj.obj)):
            new_r.update(i, rmobj.obj[i].p.v)
        return new_r
    elif isinstance(rmobj, Pocket):
        new_pocket = Pocket()
        for x in rmobj.obj:
            new_pocket.append(retiming(x, time))
        if isinstance(rmobj, Equiv):
            return Equiv(*new_pocket.obj)
        else:
            return new_pocket
    else:
        print('Unknown rmobject')
        return rmobj


def start_end(rmobj):
    """"To determine the start and the end time of the rmobj. Start and end time are Time objects"""
    start = 0
    end = 0
    if isinstance(rmobj, D):
        start = rmobj.t
        end = rmobj.t
    elif isinstance(rmobj, H):
        start = rmobj.t[0]
        end = rmobj.t[1]
    elif isinstance(rmobj, T):
        start = rmobj.t[0]
        end = rmobj.t[-1]
    elif isinstance(rmobj, B) or isinstance(rmobj, R) or isinstance(rmobj, Pocket):
        start, end = start_end(rmobj.obj[0])
        for x in rmobj.obj:
            start_t, end_t = start_end(x)
            if start_t < start:
                start = start_t
            if end_t > end:
                end = end_t

    return start, end