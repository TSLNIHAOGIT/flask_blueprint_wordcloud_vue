import random
import collections

# Hyper parameter
lock_length, lock_width = 280, 34
size_dict = {'a': [130, 17], 'b': [86, 16]}


def size_to_type(vessel_size_list):
    waiting_list = []
    for vessel_size in vessel_size_list:
        if vessel_size[1] <= 17:
            if vessel_size[0] >= 93:
                waiting_list.append('a')
            else:
                waiting_list.append('b')
        else:
            waiting_list.append('c')
    return waiting_list


def Original_schedule(vessel_size_list):
    global lock_length, lock_width, size_dict
    waiting_list = size_to_type(vessel_size_list)
    original_schedule = []
    original_position = []
    left_space = [lock_length, lock_length]
    scheduled_order = 0
    for vessel in waiting_list:
        if vessel == 'c':
            if min(left_space) > 130:
                left_space[0] -= 130
                left_space[1] -= 130
                original_schedule.append(scheduled_order)
                original_position.append('c')
            else:
                left_space = [lock_length, lock_length]
                scheduled_order += 1
                original_schedule.append(scheduled_order)
                original_position.append('c')
                left_space[0] -= 130
                left_space[1] -= 130
        else:
            if size_dict[vessel][0] < max(left_space):
                position = left_space.index(max(left_space))
                left_space[position] -= size_dict[vessel][0]
                original_schedule.append(scheduled_order)
                original_position.append(str(position))
            else:
                left_space = [lock_length, lock_length]
                scheduled_order += 1
                original_schedule.append(scheduled_order)
                left_space[0] -= size_dict[vessel][0]
                original_position.append(str(0))

    schedule_dict = collections.OrderedDict()
    position_dict = collections.OrderedDict()
    for vessel, order, position in zip(waiting_list, original_schedule, original_position):
        if schedule_dict.get(str(order)):
            schedule_dict[str(order)] = schedule_dict[str(order)] + vessel
            position_dict[str(order)] = position_dict[str(order)] + position
        else:
            schedule_dict[str(order)] = vessel
            position_dict[str(order)] = position
    return list(position_dict.values())
if __name__ == '__main__':
        waiting_list = [[110, 17], [130, 15], [85, 15], [120, 19], [130, 15]]
        res = Original_schedule(waiting_list)
        print(res)