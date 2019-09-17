from bases import *


def double(format_str, *args):
    """t, h, d"""
    if format_str[0] == '-':
        if not format_str[1] == 't':
            return
        else:
            distance = int(format_str[2])
            t1 = T(*args)
            t2 = t1.mr()
            return B([t1, t2], ['p', distance])
    else:
        distance = int(format_str[1])
        if format_str[0] == 't':
            t1 = T(*args)
            t2 = T(*args)
            return B([t1, t2], ['p', distance])
        if format_str[0] == 'h':
            h1 = H(*args)
            h2 = H(*args)
            return B([h1, h2], ['p', distance])
        if format_str[0] == 'd':
            d1 = D(*args)
            d2 = D(*args)
            return B([d1, d2], ['p', distance])
        return


def gliss_trace(time_list, step, start_column):
    timing = []
    moving = []
    current_column = deepcopy(start_column)
    for i in range(len(time_list)):
        timing.append(time_list[i].ms)
        if i == 0:
            moving.append(0)
        else:
            if 0 < current_column + step < keyboard - 1:
                moving.append(step)
                current_column += step
            elif current_column + step == keyboard - 1 or current_column + step == 0:
                moving.append(step)
                current_column += step
                step *= -1
            elif current_column + step > keyboard - 1:
                moving.append(keyboard - 1 - current_column)
                current_column = keyboard - 1
                step *= -1
            elif current_column + step < 0:
                moving.append(0 - current_column)
                current_column = 0
                step *= -1
    return T(timing, moving, start_column)


def gliss(format_str, start, end, cross=-1, *args):
    """d ,h, t type."""
    type_idx = 0
    while type_idx < len(format_str):
        if format_str[type_idx] == 'd' or format_str[type_idx] == 'h' or format_str[type_idx] == 't':
            break
        else:
            type_idx += 1
    number = int(format_str[0: type_idx])
    step = int(format_str[type_idx + 1])
    dt = (end - start)/(number - 1)
    time_list = TimeList(*[start + i*dt for i in range(0, number)])
    if args is ():
        start_column = 'f'
    else:
        start_column = args[0]
    if format_str[type_idx] == 'd':
        dots = []
        r_p = []
        for i in range(number):
            if i == 0:
                dots.append(D(time_list[i].ms, start_column))
                r_p.append('p')
            else:
                dots.append(D(time_list[i].ms))
                if i % 2 == 0:
                    r_p.append(0)
                else:
                    r_p.append(step)
        return B(dots, r_p, cross)
    if format_str[type_idx] == 't':
        traces = []
        start_column_candidates = Position(start_column).v_l()
        for i in start_column_candidates:
            if i != keyboard - 1:
                traces.append(gliss_trace(time_list, step, i))
            if i != 0:
                traces.append(gliss_trace(time_list, -step, i))
        return Equiv(*traces)
    if format_str[type_idx] == 'h':
        holds = []
        r_p = []
        if args == () or (args[0] > time_list[2] - time_list[0] and cross == -1):
            dt = time_list[2] - time_list[0] - 5
        else:
            dt = args[0]
        for i in range(len(time_list)):
            holds.append(H(time_list[i].ms, (time_list[i] + dt).ms))
            if i == 0:
                r_p.append('p')
            else:
                r_p.append(step*i)
        holds[0].p = Position(start_column)
        return B(holds, r_p, cross)


def vibro(format_str, start, end, long_end=False, *args):
    """d, h, b. Duration >= 70. Me,80"""
    distance = int(format_str[-1])
    if format_str[-2] == '-':
        distance *= -1
        type1 = format_str[-4]
        type2 = format_str[-3]
        number = int(format_str[:-4])
    else:
        type1 = format_str[-3]
        type2 = format_str[-2]
        number = int(format_str[:-3])
    dt = (end - start)/(number - 1)
    time_list = TimeList([start + i*dt for i in range(number)])
    if type1 == 'd' and type2 == 'd':
        dots = []
        r_p = []
        for i in range(len(time_list)):
            dots.append(D(time_list[i].ms))
            if i == 0:
                r_p.append('p')
            elif i % 2 == 1:
                r_p.append(distance)
            else:
                r_p.append(0)
        if long_end:
            end_duration = args[0]
            dots[-1] = H(time_list[-1].ms, (time_list[-1]+end_duration).ms)
        return B(dots, r_p)
    elif type1 == 'd' and type2 == 'h':
        objs = []
        r_p = []
        for i in range(len(time_list)):
            if not i == len(time_list) - 1:
                if i % 2 == 0:
                    objs.append(D(time_list[i].ms))
                    r_p.append(0)
                else:
                    objs.append(H(time_list[i].ms, time_list[i+1].ms))
                    r_p.append(distance)
            else:
                if i % 2 == 0:
                    objs.append(D(time_list[-1].ms))
                    r_p.append(0)
                else:
                    objs.append(H(time_list[-1].ms, (time_list[-1]+dt).ms))
                    r_p.append(distance)
        r_p[0] = 'p'
        if long_end:
            end_duration = args[0]
            objs[-1] = H(time_list[-1].ms, (time_list[-1]+end_duration).ms)
        return B(objs, r_p)
    elif type1 == 'h' and type2 == 'd':
        objs = []
        r_p = []
        for i in range(len(time_list)):
            if not i == len(time_list) - 1:
                if i % 2 == 1:
                    objs.append(D(time_list[i].ms))
                    r_p.append(distance)
                else:
                    objs.append(H(time_list[i].ms, time_list[i + 1].ms))
                    r_p.append(0)
            else:
                if i % 2 == 1:
                    objs.append(D(time_list[-1].ms))
                    r_p.append(distance)
                else:
                    objs.append(H(time_list[-1].ms, (time_list[-1] + dt).ms))
                    r_p.append(0)
        r_p[0] = 'p'
        if long_end:
            end_duration = args[0]
            objs[-1] = H(time_list[-1].ms, (time_list[-1]+end_duration).ms)
        return B(objs, r_p)
    elif type1 == 'd' and type2 == 'b':
        block1 = args[0]
        objs = []
        r_p = []
        for i in range(len(time_list)):
            if not i == len(time_list) - 1:
                if i % 2 == 0:
                    objs.append(D(time_list[i].ms))
                    r_p.append(0)
                else:
                    block2 = deepcopy(block1)
                    for x in block2.obj:
                        x.t = x.t + time_list[i]
                    objs.append(block2)
                    r_p.append(distance)
            else:
                if i % 2 == 0:
                    objs.append(D(time_list[-1].ms))
                    r_p.append(0)
                else:
                    block2 = deepcopy(block1)
                    for x in block2.obj:
                        x.t = x.t + time_list[i]
                    objs.append(block2)
                    r_p.append(distance)
        r_p[0] = 'p'
        if long_end:
            end_duration = args[1]
            if isinstance(objs[-1], D):
                objs[-1] = H(time_list[-1].ms, (time_list[-1] + end_duration).ms)
            else:
                columns = set(objs[-1].get_columns(distance))
                for cc in columns:
                    objs.append(H(time_list[-1].ms, (time_list[-1] + end_duration).ms))
                    r_p.append(cc)
        return B(objs, r_p)
    elif type1 == 'b' and type2 == 'd':
        block1 = args[0]
        objs = []
        r_p = []
        for i in range(len(time_list)):
            if not i == len(time_list) - 1:
                if i % 2 == 1:
                    objs.append(D(time_list[i].ms))
                    r_p.append(0)
                else:
                    block2 = deepcopy(block1)
                    for x in block2.obj:
                        x.t = x.t + time_list[i]
                    objs.append(block2)
                    r_p.append(distance)
            else:
                if i % 2 == 1:
                    objs.append(D(time_list[-1].ms))
                    r_p.append(0)
                else:
                    block2 = deepcopy(block1)
                    for x in block2.obj:
                        x.t = x.t + time_list[i]
                    objs.append(block2)
                    r_p.append(distance)
        r_p[0] = 'p'
        if long_end:
            end_duration = args[1]
            if isinstance(objs[-1], D):
                objs[-1] = H(time_list[-1].ms, (time_list[-1] + end_duration).ms)
            else:
                columns = set(objs[-1].get_columns(distance))
                for cc in columns:
                    objs.append(H(time_list[-1].ms, (time_list[-1] + end_duration).ms))
                    r_p.append(cc)
        return B(objs, r_p)
    elif type1 == 'b' and type2 == 'b':
        block1 = args[0]
        block2 = args[1]
        blocks = []
        r_p = []
        for i in range(len(time_list)):
            if i != len(time_list) - 1:
                if i % 2 == 0:
                    block11 = deepcopy(block1)
                    for x in block11.obj:
                        x.t = x.t + time_list[i]
                    blocks.append(block11)
                    r_p.append(0)
                else:
                    block11 = deepcopy(block2)
                    for x in block11.obj:
                        x.t = x.t + time_list[i]
                    blocks.append(block11)
                    r_p.append(distance)
            else:
                if i % 2 == 0:
                    block11 = deepcopy(block1)
                    for x in block11.obj:
                        x.t = x.t + time_list[i]
                    blocks.append(block11)
                    r_p.append(0)
                else:
                    block11 = deepcopy(block2)
                    for x in block11.obj:
                        x.t = x.t + time_list[i]
                    blocks.append(block11)
                    r_p.append(distance)
        if long_end:
            end_duration = args[2]
            columns1 = set(block1.get_columns(0))
            columns2 = set(block2.get_columns(distance))
            columns12 = columns1.union(columns2)
            for cc in columns12:
                blocks.append(H(time_list[-1].ms, (time_list[-1] + end_duration).ms))
                r_p.append(cc)
        r_p[0] = 'p'
        return B(blocks, r_p)


def ll(start, end, position='f'):
    return T([start, end], [-1, 0], position)


def lr(start, end, position='f'):
    return T([start, end], [1, 0], position)


def i_lr(start, end, position='f'):
    return T([start, end], [0, 1], position)


def i_ll(start, end, position='f'):
    return T([start, end], [0, -1], position)


def l_forms(start, end, position='f'):
    a = ll(start, end, position)
    b = lr(start, end, position)
    return Equiv(a, b)


def il_forms(start, end, position='f'):
    a = i_ll(start, end, position)
    b = i_lr(start, end, position)
    return Equiv(a, b)


def cl(start, end, position='f'):
    return T([start, end], [-1, 1], position)


def cr(start, end, position='f'):
    return cl(start, end, position).mr()


def c_forms(start, end, position='f'):
    return Equiv(cl(start, end, position), cr(start, end, position))


def baf(timing, distance, long_end=False, position='f', *arg):
    if long_end:
        end_duration = arg[0]
        timing.append(timing[-1] + end_duration)
        moving = [0, ]
        for i in range(len(timing) - 2):
            if i % 2 == 1:
                moving.append(-distance)
            else:
                moving.append(distance)
        moving.append(0)
        return T(timing, moving, position)
    else:
        moving = [0, ]
        for i in range(len(timing) - 1):
            if i % 2 == 1:
                moving.append(-distance)
            else:
                moving.append(distance)
        return T(timing, moving, position)


def c_trace(timing, moving, position='f'):
    """Reaction time is 100ms"""
    new_timing = [timing[0], ]
    new_moving = [moving[0], ]
    for i in range(1, len(moving)):
        if moving[i] == 1 or moving[i] == -1:
            new_moving.append(moving[i])
            new_timing.append(timing[i])
        else:
            steps = abs(moving[i])
            sign = moving[i]//steps
            dt = 100/steps
            for rr in range(steps):
                new_timing.append(timing[i] - 100 + (rr+1)*dt)
                new_moving.append(sign)
    return T(new_timing, new_moving, position)


def reversal_h(timing, position, dt=80):
    column = Position(position).choice()
    timing[0] -= dt
    r_p = []
    holds = []
    for i in range(len(timing)-1):
        holds.append(H(timing[i]+dt, timing[i+1], column))
        r_p.append(0)
    r_p[0] = 'p'
    return B(holds, r_p)


def arrange_reversal_timing(timing, your_columns, opening='all', ending='all'):
    open_dots = []
    end_dots = []
    your_keyboard = len(your_columns)
    if opening == 'all' and ending == 'all':
        dots = timing[1:-1]
        for i in range(your_keyboard):
            open_dots.append(timing[0])
            end_dots.append(timing[-1])
    elif opening == 'all' and ending != 'all':
        dots = timing[1:-your_keyboard]
        for i in range(your_keyboard):
            open_dots.append(timing[0])
        end_dots = timing[-your_keyboard:]
        if ending == 'r':
            pass
        elif ending == 'l':
            end_dots.reverse()
        else:
            for i in range(your_keyboard):
                idx = randrange(your_keyboard)
                end_dots[i], end_dots[idx] = end_dots[idx], end_dots[i]
    elif opening != 'all' and ending == 'all':
        dots = timing[your_keyboard: -1]
        for i in range(your_keyboard):
            end_dots.append(timing[-1])
        open_dots = timing[0:your_keyboard]
        if opening == 'r':
            pass
        elif opening == 'l':
            open_dots.reverse()
        else:
            for i in range(your_keyboard):
                idx = randrange(your_keyboard)
                open_dots[i], open_dots[idx] = open_dots[idx], open_dots[i]
    else:
        dots = timing[your_keyboard:-your_keyboard]
        open_dots = timing[0:your_keyboard]
        end_dots = timing[-your_keyboard:]
        if opening == 'r':
            pass
        elif opening == 'l':
            open_dots.reverse()
        else:
            for i in range(your_keyboard):
                idx = randrange(your_keyboard)
                open_dots[i], open_dots[idx] = open_dots[idx], open_dots[i]
        if ending == 'r':
            pass
        elif ending == 'l':
            end_dots.reverse()
        else:
            for i in range(your_keyboard):
                idx = randrange(your_keyboard)
                end_dots[i], end_dots[idx] = end_dots[idx], end_dots[i]
    return dots, open_dots, end_dots


def non_reversal_dots(timing, opening='all', ending='all'):
    my_columns = [x for x in range(keyboard)]
    dots, open_dots, end_dots = arrange_reversal_timing(timing, my_columns, opening, ending)
    objs = []
    r_p = []
    for i in range(len(open_dots)):
        objs.append(D(open_dots[i]))
        r_p.append(i)
    for i in range(len(dots)):
        objs.append(D(dots[i]))
        tt = randrange(keyboard)
        while tt == r_p[-1]:
            tt = randrange(keyboard)
        r_p.append(tt)
    for i in range(len(end_dots)):
        objs.append(D(end_dots[i]))
        r_p.append(i)
    r_p[0] = 'p'
    objs[0].p = Position(0)
    return B(objs, r_p)


def reversal_full(timing, cross=0, dt=100, opening='all', ending='all', *args):
    my_columns = [x for x in range(keyboard)]
    return reversal_within_columns(timing, my_columns, cross, dt, opening, ending, *args)


def reversal_within_columns(timing, your_columns, cross=0, dt=100, opening='all', ending='all', *args):
    """Recommend dt >= 100. Me 80 """
    dots, open_dots, end_dots = arrange_reversal_timing(timing, your_columns, opening, ending)
    your_keyboard = len(your_columns)
    columns = []
    if not cross:
        columns = [your_columns[randrange(your_keyboard)], ]
        for i in range(len(dots) - 1):
            c = your_columns[randrange(your_keyboard)]
            while c == columns[-1]:
                c = your_columns[randrange(your_keyboard)]
            columns.append(c)
    elif cross == 1:
        columns = [args[0], ]
        distance = args[1]
        for i in range(len(dots) - 1):
            new_column = distance + columns[-1]
            columns.append(new_column % your_keyboard)
        for x in columns:
            x = your_columns[x]
    elif cross == -1:
        columns = [args[0], ]
        distance = args[1]
        for i in range(1, len(dots)):
            if 0 < columns[-1] + distance < your_keyboard - 1:
                columns.append(columns[-1] + distance)
            elif columns[-1] + distance == your_keyboard - 1 or columns[-1] + distance == 0:
                columns.append(columns[-1] + distance)
                distance *= -1
            elif columns[-1] + distance > your_keyboard - 1:
                columns.append(2 * your_keyboard - 2 - columns[-2] - distance)
                distance *= -1
            elif columns[-1] + distance < 0:
                columns.append(-columns[-1] - distance)
                distance *= -1
        for x in columns:
            x = your_columns[x]
    objs = []
    r_p = []
    for c in range(your_keyboard):
        column_timing_list = [open_dots[c], ]
        for ww in range(len(columns)):
            if columns[ww] == your_columns[c]:
                column_timing_list.append(dots[ww])
        column_timing_list.append(end_dots[c])
        objs.append(reversal_h(column_timing_list, your_columns[c], dt))
        r_p.append(your_columns[c] - your_columns[0])
    r_p[0] = 'p'
    return B(objs, r_p, cross=0)


def mir(format_str, timing, *args):
    obj_type = format_str[-1]
    number = 1
    position = 0
    position1 = 0
    r_p = []
    if len(format_str) > 1:
        number = int(format_str[0])
    if number == 2:
        position = args[0]
        r_p = ['p', keyboard - 1 - 2 * position]
    elif number == 3:
        position = args[0]
        r_p = ['p', 2 - position, keyboard - 1 - 2*position]
    elif number == 4:
        position1 = args[0]
        position2 = args[1]
        r_p = ['p', position2 - position1, keyboard - 1 - position2 - position1, keyboard - 1 - 2*position1]
    if obj_type == 'd':
        if number == 2:
            a = D(timing, position)
            b = D(timing)
            return B([a, b], r_p)
        elif number == 3 and keyboard == 5:
            a = D(timing, position)
            b = D(timing)
            c = D(timing)
            return B([a, b, c], r_p)
        elif number == 4:
            a = D(timing, position1)
            b = D(timing)
            c = D(timing)
            d = D(timing)
            return B([a, b, c, d], r_p)
    elif obj_type == 'h':
        if number == 2:
            a = H(timing[0], timing[1], position)
            b = H(timing[0], timing[1])
            return B([a, b],r_p)
        elif number == 3:
            a = H(timing[0], timing[1], position)
            b = H(timing[0], timing[1])
            c = H(timing[0], timing[1])
            return B([a, b, c], r_p)
        elif number == 4:
            a = H(timing[0], timing[1], position1)
            b = H(timing[0], timing[1])
            c = H(timing[0], timing[1])
            d = H(timing[0], timing[1])
            return B([a, b, c, d], r_p)
    elif obj_type == 't':
        moving = args[0]
        position = args[1]
        r_p = ['p', keyboard - 1 - 2*position]
        a = T(timing, moving, position)
        b = a.mr()
        b.p = Position('f')
        return B([a, b], r_p)
    else:
        print('Invalid arguments')
