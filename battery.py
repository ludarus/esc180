# battery state enums
STATE_IDLE = 0
STATE_DEPLETING = 1
STATE_SLOWCHARGING = 2
STATE_FASTCHARGING = 3

# constants
BATTERY_HEALTH_WINDOW = 360  # in minutes
BAD_HEALTH_LIMIT = 80  # in percent

# fast charging
FC_TEMP_RANGE = (0, 40)  # min temp, max temp
FC_PERCENTAGE_RANGE = (0, 80)  # min percentage, max percentage
FC_PERCENT_RATE = 3  # in percentage/minute
FC_TEMP_RATE = 0.5  # in degrees/minute

# slow charging
SC_PERCENT_RATE = 1  # in percentage/minute
SC_TEMP_RATE = 0.25  # in degrees/minute

# idle
IDLE_PERCENT_RATE = -0.5  # in percentage/minute
IDLE_TEMP_RATE = -1  # in degrees/minute

# usage
DEPLETING_PERCENT_RATE = -2  # in percentage/minute
DEPLETING_TEMP_RATE = 1  # in degrees/minute

DEAD_TEMP_RATE = -1


# private functions
def _change_battery(amount: float) -> None:
    global cur_battery
    cur_battery += (
        max(amount, -cur_battery)
        if amount < 0
        else min(
            (100 if good_battery_health else BAD_HEALTH_LIMIT) - cur_battery, amount
        )
    )


def _change_temp(amount: float) -> None:
    global cur_temp
    cur_temp += max(-cur_temp, amount) if amount < 0 else amount


def initialize() -> None:
    """Initializes the global variables needed for the simulation and should only be called on startup"""
    # note: temp and percentage can never go below 0
    global cur_temp  # in degrees Celsius
    global cur_battery  # in percentage points
    global cur_time  # in minutes
    global good_battery_health  # boolean
    global battery_state  # enum
    global attempts_above_90  # list

    # default variable state
    cur_time = 0
    good_battery_health = True
    cur_battery = 50
    cur_temp = 20.0
    battery_state = STATE_IDLE
    attempts_above_90 = []  # list of timestamps when you charged above 90. if the cur time - back > 60 * 6 = 360 minutes, kick it out of there. then if len(this) is 3, slow charging time


def simulate_activity(activity, duration) -> None:

    # checking for positive duration
    if duration <= 0:
        return

    # scope in all global variables
    global cur_time
    global good_battery_health
    global battery_state
    global attempts_above_90
    global cur_battery

    # incrementing time
    cur_time += duration

    # switch statement
    match activity.lower():
        case "charge":
            # fast charging rate
            fc_duration = min(duration, duration_fast_charge_possible())
            battery_state = STATE_FASTCHARGING
            _change_battery(fc_duration * FC_PERCENT_RATE)
            _change_temp(fc_duration * FC_TEMP_RATE)
            duration -= fc_duration

            battery_state = STATE_SLOWCHARGING
            _change_battery(duration * SC_PERCENT_RATE)
            _change_temp(duration * SC_TEMP_RATE)

            if get_cur_charge() >= 90:
                attempts_above_90.append(cur_time)


        case "use":
            dur_until_dead = min(get_cur_charge() / abs(DEPLETING_PERCENT_RATE), duration)
            dur_after_dead = duration - dur_until_dead
            battery_state = STATE_DEPLETING
            _change_battery(duration * DEPLETING_PERCENT_RATE)
            _change_temp(dur_until_dead * DEPLETING_TEMP_RATE)
            _change_temp(dur_after_dead * DEAD_TEMP_RATE)

        case "idle":
            battery_state = STATE_IDLE
            _change_battery(duration * IDLE_PERCENT_RATE)
            _change_temp(duration * IDLE_TEMP_RATE)

     # resetting state
    battery_state = STATE_IDLE

    # battery health update
    if get_cur_battery_health():
        while (
            attempts_above_90
            and cur_time - attempts_above_90[0] > BATTERY_HEALTH_WINDOW
        ):
            attempts_above_90.pop(0)
    if len(attempts_above_90) >= 3:
        good_battery_health = False

    # health just flipped mid-charge, so the battery would have stopped at 90
    if not good_battery_health and cur_battery > 90:
        cur_battery = 90

def duration_fast_charge_possible() -> float:
    # Fast charging occurs when the temperature is between 0-40°C, battery charge is below 80%, and battery health is good.
    cur_charge = get_cur_charge()
    if not get_cur_battery_health():  # health =0
        return 0
    if cur_charge >= FC_PERCENTAGE_RANGE[1]:  # we cant fastcharge no more
        return 0
    if (
        not FC_TEMP_RANGE[0] <= (temp := get_cur_temp()) <= FC_TEMP_RANGE[1]
    ):  # temp is in fc temp range
        return 0
    temp_time = (FC_TEMP_RANGE[1] - temp) / FC_TEMP_RATE
    charge_time = (FC_PERCENTAGE_RANGE[1] - cur_charge) / FC_PERCENT_RATE
    return min(temp_time, charge_time)
    # temp until 40


def get_cur_temp() -> float:
    return cur_temp


def get_cur_charge() -> float:
    return cur_battery


def get_cur_battery_health() -> float:
    return good_battery_health


def charge_time_needed(minutes):
    battery_needed = minutes * abs(DEPLETING_PERCENT_RATE)
    battery_missing = battery_needed - get_cur_charge()

    if battery_missing <= 0:
        return 0

    max_battery = 100 if get_cur_battery_health() else BAD_HEALTH_LIMIT
    if battery_needed > max_battery:
        return None

    fast_duration = duration_fast_charge_possible()
    fast_charge_available = fast_duration * FC_PERCENT_RATE

    if battery_missing <= fast_charge_available:
        return battery_missing / FC_PERCENT_RATE

    remaining = battery_missing - fast_charge_available

    return fast_duration + remaining / SC_PERCENT_RATE


if __name__ == "__main__":
    initialize()

    print(duration_fast_charge_possible())  # 10
    print(charge_time_needed(50))  # 30

    simulate_activity("charge", 30)
    print(get_cur_charge())  # 100
    print(get_cur_temp())  # 30

    simulate_activity("use", 50)
    print(get_cur_charge())  # 0
    print(get_cur_temp())  # 80

    simulate_activity("use", 10)
    print(get_cur_charge())  # 0
    print(get_cur_temp())  # 70

    simulate_activity("charge", 100)
    print(get_cur_charge())  # 100
    print(get_cur_temp())  # 95

    simulate_activity("idle", 100)
    print(get_cur_charge())  # 50
    print(get_cur_temp())  # 0
    print(get_cur_battery_health())  # True
    print(duration_fast_charge_possible())  # 10

    simulate_activity("charge", 80)
    print(get_cur_charge())  # 90
    print(get_cur_temp())  # 22.5
    print(get_cur_battery_health())  # False

    simulate_activity("use", 40)
    print(get_cur_charge())  # 10
    print(get_cur_temp())  # 62.5

    simulate_activity("charge", 80)
    print(get_cur_charge())  # 80
    print(get_cur_temp())  # 82.5

    initialize()
    # add your tests here
