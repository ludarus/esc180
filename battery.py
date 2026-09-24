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
FC_PERCENTAGE_RANGE = (0, 79)  # min percentage, max percentage
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
DEPLETING_TEMP_RATE = -1  # in degrees/minute


# private functions
def _change_battery(amount: int) -> None:
    global cur_battery
    cur_battery += (
        min(cur_battery, amount)
        if amount < 0
        else min(100 if good_battery_health else BAD_HEALTH_LIMIT - cur_battery, amount)
    )


def _change_temp(amount: int) -> None:
    global cur_temp
    cur_temp += min(cur_temp, amount) if amount < 0 else amount


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
    attempts_above_90 = (
        []
    )  # list of timestamps when you charged above 90. if the cur time - back > 60 * 6 = 360 minutes, kick it out of there. then if len(this) is 3, slow charging time


def simulate_activity(activity, duration) -> None:

    # checking for positive duration
    if duration <= 0:
        return

    # scope in all global variables
    global cur_time
    global good_battery_health
    global battery_state

    # incrementing time
    cur_time += duration

    # switch statement
    match activity.lower():
        case "charge":
            # fast charging rate
            fc_duration = duration_fast_charge_possible()
            if fc_duration > 0:
                battery_state = STATE_FASTCHARGING
                _change_battery(fc_duration * FC_PERCENT_RATE)
                _change_temp(fc_duration * FC_TEMP_RATE)
                duration -= fc_duration

            if duration > 0:
                battery_state = STATE_SLOWCHARGING
                _change_battery(duration * SC_PERCENT_RATE)
                _change_temp(duration * SC_TEMP_RATE)

        case "use":
            battery_state = STATE_DEPLETING
            _change_battery(duration * DEPLETING_PERCENT_RATE)
            _change_temp(duration * DEPLETING_TEMP_RATE)

        case "idle":
            battery_state = STATE_IDLE
            _change_battery(duration * IDLE_PERCENT_RATE)
            _change_temp(duration * IDLE_TEMP_RATE)

    # resetting state
    battery_state = STATE_IDLE

    # battery health update
    if get_cur_battery_health() and attempts_above_90:
        if cur_time - attempts_above_90[0] > BATTERY_HEALTH_WINDOW:
            _ = attempts_above_90.pop(0)
        if len(attempts_above_90) >= 3:
            good_battery_health = False


def duration_fast_charge_possible() -> float:
    # Fast charging occurs when the temperature is between 0-40°C, battery charge is below 80%, and battery health is good.
    if not get_cur_battery_health():
        return 0
    if get_cur_charge() >= BAD_HEALTH_LIMIT:
        return 0
    if not FC_TEMP_RANGE[0] <= (temp := get_cur_temp()) < FC_TEMP_RANGE[1]:
        return 0
    temp_time = (FC_TEMP_RANGE[1] - temp) / FC_TEMP_RATE
    charge_time = (BAD_HEALTH_LIMIT - get_cur_charge()) / FC_PERCENT_RATE
    return min(temp_time, charge_time)
    # temp until 40


def get_cur_temp() -> float:
    return cur_temp


def get_cur_charge() -> float:
    return cur_battery


def get_cur_battery_health() -> float:
    return good_battery_health


def charge_time_needed(minutes):
    if duration_fast_charge_possible() >= minutes:
        rate = FC_TEMP_RATE
    else:
        rate = 

    if minutes > 50:  # 100/2 fast charge per minute
        return None
    elif get_cur_charge() + minutes * DEPLETING_PERCENT_RATE >= 0:
        return 0
    else:
        return abs(get_cur_charge() + minutes * DEPLETING_PERCENT_RATE) / abs(rate)


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
