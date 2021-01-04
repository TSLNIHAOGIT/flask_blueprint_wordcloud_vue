import pymysql
from config import MYSQL_IP, MYSQL_USER, MYSQL_PASS, MYSQL_DB
from datetime import datetime, timezone, timedelta

tz = timezone(timedelta(0, 28800))  # 转化为东8区时间


def candidate_schedule_generator(date_begin, date_end=None):
    tm = datetime.strptime(date_begin, "%Y-%m-%d %H:%M:%S")
    tm_tz = datetime(tm.year, tm.month, tm.day, tm.hour, tm.minute, tm.second, tzinfo=tz)
    date_begin_time_stamp = datetime.timestamp(tm_tz)
    count = -1
    if not date_end:
        tm_tz = datetime(9000, tm.month, tm.day, tm.hour, tm.minute, tm.second, tzinfo=tz)
        date_end_time_stamp = datetime.timestamp(tm_tz)
    else:
        tm_end = datetime.strptime(date_end, "%Y-%m-%d %H:%M:%S")
        tm_tz = datetime(tm_end.year, tm_end.month, tm_end.day, tm_end.hour, tm_end.minute, tm_end.second, tzinfo=tz)
        date_end_time_stamp = datetime.timestamp(tm_tz)
    while True:
        count += 1
        extra_day = count // 3
        lockage_order = (count + 1) % 3
        if lockage_order == 1:
            tm_tz_candidate = datetime(tm.year, tm.month, tm.day, 2, 0, 0, tzinfo=tz)
        elif lockage_order == 2:
            tm_tz_candidate = datetime(tm.year, tm.month, tm.day, 3, 30, 0, tzinfo=tz)
        else:
            tm_tz_candidate = datetime(tm.year, tm.month, tm.day, 15, 0, 0, tzinfo=tz)
        candidate_time_stamp = datetime.timestamp(tm_tz_candidate) + extra_day * 86400
        if candidate_time_stamp > date_end_time_stamp:
            break
        if extra_day == 0:
            if date_begin_time_stamp <= candidate_time_stamp:
                yield int(candidate_time_stamp)
        else:
            yield int(candidate_time_stamp)


def fetch_sheduled_plan(ship_lock_id, lock_time_stamp):
    sql = """
    SELECT
        vsl.length,
        vsl.width,
        vitem.position
    FROM
        sch_ship_lock_plan vplan
        LEFT JOIN sch_ship_lock_plan_item vitem ON vplan.id = vitem.ship_lock_plan_id
        LEFT JOIN sch_vessel vsl ON vitem.vessel_id = vsl.id 
    WHERE
        vplan.id =  '{}' and vplan.ship_lock_id = '{}'""".format(lock_time_stamp, ship_lock_id)

    db = pymysql.connect(MYSQL_IP, MYSQL_USER, MYSQL_PASS, MYSQL_DB, charset='utf8')
    cursor = db.cursor()
    cursor.execute(sql)
    sql_data = cursor.fetchall()
    cursor.close()
    db.close()
    return sql_data


def fetch_vessel_info(vessel_id):
    sql = """
    SELECT 
        code,
        name,
        length,
        width
    FROM 
        sch_vessel
    WHERE 
        id = '{}' """.format(vessel_id)
    db = pymysql.connect(MYSQL_IP, MYSQL_USER, MYSQL_PASS, MYSQL_DB, charset='utf8')
    cursor = db.cursor()
    cursor.execute(sql)
    sql_data = cursor.fetchall()
    cursor.close()
    db.close()
    return sql_data


def add_to_plan(vessel_width, scheduled_plan=None):
    """
    32.8 * 264
    """
    width_max = 32.8
    length_max = 264

    if not scheduled_plan:
        return '0,0'
    pos_width_dict = {i[2]: i[1] for i in scheduled_plan}
    if pos_width_dict.get('0,0', 0) + pos_width_dict.get('2,0', 0) + vessel_width <= width_max:
        if '0,0' not in pos_width_dict.keys():
            return '0,0'
        else:
            return '2,0'
    elif pos_width_dict.get('0,1', 0) + pos_width_dict.get('2,1', 0) + vessel_width <= width_max:
        if '0,1' not in pos_width_dict.keys():
            return '0,1'
        else:
            return '2,1'
    else:
        return None


def query_available_schedule(vessel_id, ship_lock_id, date_begin, date_end=None, candidate_num=10):
    try:
        (vessel_code, vessel_name, vessel_length, vessel_width) = fetch_vessel_info(vessel_id)[0]
    except:
        print("No such vessel with id {}".format(vessel_id))
        return
    count = 0
    available_schedule = []
    for lock_time_stamp in candidate_schedule_generator(date_begin, date_end):
        scheduled_plan = fetch_sheduled_plan(ship_lock_id, lock_time_stamp)
        vessel_position = add_to_plan(vessel_width, scheduled_plan)
        if vessel_position:
            available_schedule.append((vessel_position, lock_time_stamp))
            count += 1
        if count == candidate_num:
            return available_schedule


def query_unscheduled_voyages(voyage_id):
    sql = """
        SELECT
            sch_vessel.id,
            sch_voyage.expect_check_time,
            sch_voyage.ie_flag,
            sch_vessel.length,
            sch_vessel.width
        FROM
            sch_voyage
            LEFT JOIN sch_vessel ON sch_vessel.code = sch_voyage.vessel_code 
        WHERE
            sch_voyage.id = '{}' 
        """.format(voyage_id)
    db = pymysql.connect(MYSQL_IP, MYSQL_USER, MYSQL_PASS, MYSQL_DB, charset='utf8')
    cursor = db.cursor()
    cursor.execute(sql)
    sql_data = cursor.fetchall()
    cursor.close()
    db.close()
    return sql_data


def clear_scheduled_record(voyage_id):
    sql = """
        SELECT
            * 
        FROM
            sch_ship_lock_plan_item 
        WHERE
            ship_lock_plan_id = ( SELECT ship_lock_plan_id FROM sch_ship_lock_plan_item WHERE voyage_id = '{}' )
    """.format(voyage_id)
    db = pymysql.connect(MYSQL_IP, MYSQL_USER, MYSQL_PASS, MYSQL_DB, charset='utf8')
    cursor = db.cursor()
    cursor.execute(sql)
    sql_data = cursor.fetchall()
    # delete plan
    if not sql_data:
        return None
    elif len(sql_data) == 1:
        plan_id = sql_data[0][0]
        sql = """
            DELETE 
            FROM
                sch_ship_lock_plan 
            WHERE
                id = '{}'
        """.format(plan_id)
        cursor.execute(sql)
    else:
        pass
    # delete item
    sql = """
            DELETE 
            FROM
                sch_ship_lock_plan_item 
            WHERE
                voyage_id = '{}'
    """.format(voyage_id)
    cursor.execute(sql)

    db.commit()
    cursor.close()
    db.close()


def insert_plan_into_db(voyage_id, vessel_id, ship_lock_id, direction, vessel_position, plan_timestamp):
    # useful general info
    tm = datetime.fromtimestamp(plan_timestamp, tz)
    plan_date = datetime.strftime(tm, "%Y-%m-%d 00:00:00")
    plan_start_time = datetime.strftime(tm, "%Y-%m-%d %H:%M:%S")
    created_date = datetime.now(tz).strftime("%Y-%m-%d %H:%M:%S")
    if direction == 'E':
        plan_direction = 'Down'
    else:
        print("Need further work!")

    # Insert plan first
    sql = """
        SELECT 
            *
        FROM
            sch_ship_lock_plan
        WHERE
            id = '{}'
    """.format(plan_timestamp)
    db = pymysql.connect(MYSQL_IP, MYSQL_USER, MYSQL_PASS, MYSQL_DB, charset='utf8')
    cursor = db.cursor()
    cursor.execute(sql)
    sql_data = cursor.fetchall()
    if not sql_data:
        sql = """
            INSERT INTO 
                sch_ship_lock_plan 
                (id, ship_lock_id, plan_date, direction, start_time, created_date)
            VALUES
                (%s, %s, %s, %s, %s, %s)
        """
        params = (plan_timestamp, ship_lock_id, plan_date, plan_direction, plan_start_time, created_date)
        cursor.execute(sql, params)
    else:
        pass
    # Insert plan item
    (vessel_code, vessel_name, _, __) = fetch_vessel_info(vessel_id)[0]
    sql = """
        INSERT INTO 
            sch_ship_lock_plan_item 
            (ship_lock_plan_id, position, vessel_id, vessel_code, vessel_name, voyage_id, status, created_date)
        VALUES
            (%s, %s, %s, %s, %s, %s, %s, %s)
    """
    params = (plan_timestamp, vessel_position, vessel_id, vessel_code, vessel_name, voyage_id, '3', created_date)
    cursor.execute(sql, params)

    #     # Update sch_voyage
    #     sql = """
    #         UPDATE
    #             sch_voyage
    #         SET
    #             voyage_status = '3'
    #         WHERE
    #             id = '{}'
    #     """.format(voyage_id)
    #     cursor.execute(sql)
    #     # Insert sch_voyage_histroy_node, note that the name history misspelled to histroy
    #     sql = """
    #         INSERT INTO
    #             sch_voyage_histroy_node
    #             (id, voyage_id, status, created_date)
    #         VALUES
    #             (UUID(), '{}', '3', '{}')
    #     """.format(voyage_id, created_date)
    #     cursor.execute(sql)
    #     # Insert sch_voyage_node
    #     security_check_timestamp = plan_timestamp - 3600*6
    #     security_anchor_timestamp = security_check_timestamp - 3600*6
    #     yunyang_bridge_timestamp = security_anchor_timestamp - 3600*24*2
    #     departure_timestamp = yunyang_bridge_timestamp - 3600*24*3
    #     t_lock =  datetime.strftime( datetime.fromtimestamp(plan_timestamp,tz), '%Y-%m-%d %H:%M:%S')
    #     t_check =  datetime.strftime( datetime.fromtimestamp(security_check_timestamp,tz), '%Y-%m-%d %H:%M:%S')
    #     t_anchor = datetime.strftime( datetime.fromtimestamp(security_anchor_timestamp,tz), '%Y-%m-%d %H:%M:%S')
    #     t_bridge = datetime.strftime( datetime.fromtimestamp(yunyang_bridge_timestamp,tz), '%Y-%m-%d %H:%M:%S')
    #     t_departure = datetime.strftime( datetime.fromtimestamp(departure_timestamp,tz), '%Y-%m-%d %H:%M:%S')
    #     node_time = [t_departure, t_bridge, t_anchor, t_check, t_lock]
    #     node_name = ['发航时间', '云阳大桥', '安检锚地', '安检', '过闸']
    #     node_description = ['建议发航时间', '建议到达云阳大桥时间', '需按时到达', '安检要求', '按计划过闸']
    #     node_duration = ['', '3d', '2d', '6h', '6h']
    #     for node in range(5):
    #         sql = """
    #             INSERT INTO
    #                 sch_voyage_node
    #                 (id, voyage_id, name, duration, description, estimated_time, created_date)
    #             VALUES
    #                 (UUID(), '{}', '{}', '{}', '{}', '{}', '{}')
    #         """.format(voyage_id, node_name[node], node_duration[node], node_description[node], node_time[0], created_date)
    #         cursor.execute(sql)

    # commit and close
    db.commit()
    cursor.close()
    db.close()


def schedule_api(voyage_id):
    voyage_info = query_unscheduled_voyages(voyage_id)
    if not voyage_info:
        print("no voyage_info for voyage_id: {}".format(voyage_id))
        return None
    (vessel_id, check_time, direction, vessel_length, vessel_width) = voyage_info[0]
    if not vessel_id:
        print("no vessel_id for voyage_id: {}".format(voyage_id))
        return None

    if not vessel_id:
        print('Cant find vessel_id from vessel_name for voyage_id - {}'.format(voyage_id))
        return None
    check_time = check_time.strftime("%Y-%m-%d %H:%M:%S")
    if direction == 'E':
        ship_lock_id = "0001"
        clear_scheduled_record(voyage_id)
        (vessel_position, plan_timestamp) = query_available_schedule(vessel_id, ship_lock_id, check_time, None, 1)[0]
        insert_plan_into_db(voyage_id, vessel_id, ship_lock_id, direction, vessel_position, plan_timestamp)

if __name__ == '__main__':
    for voyage_id in ['956b1ec9-384f-48c3-9c5c-92172e8d40c3']:
        schedule_api(voyage_id)