# constants
BATTERY_HEALTH_WINDOW: int = 360  # in minutes
BAD_HEALTH_LIMIT: int = 80  # in percent

# fast charging
FC_TEMP_RANGE: tuple[int, int] = (0, 40)  # min temp, max temp
FC_PERCENTAGE_RANGE: tuple[int, int] = (0, 80)  # min percentage, max percentage
FC_PERCENT_RATE: float = 3.0  # in percentage/minute
FC_TEMP_RATE: float = 0.5  # in degrees/minute

# slow charging
SC_PERCENT_RATE: float = 1.0  # in percentage/minute
SC_TEMP_RATE: float = 0.25  # in degrees/minute

# idle
IDLE_PERCENT_RATE: float = -0.5  # in percentage/minute
IDLE_TEMP_RATE: float = -1.0  # in degrees/minute

# usage
DEPLETING_PERCENT_RATE: float = -2.0  # in percentage/minute
DEPLETING_TEMP_RATE: float = 1.0  # in degrees/minute

DEAD_TEMP_RATE: float = -1.0

cur_temp: float
cur_battery: float
cur_time: float
good_battery_health: bool
attempts_above_90: list[float]


# private functions
def _change_battery(amount: float) -> None:
    global cur_battery
    if amount < 0:
        cur_battery = max(0, cur_battery + amount)
    else:
        # limit is either 100, the bad health limit, or the current battery (if we entered bad health above 80)
        limit = 100 if good_battery_health else max(BAD_HEALTH_LIMIT, cur_battery)
        cur_battery = min(cur_battery + amount, limit)


def _change_temp(amount: float) -> None:
    global cur_temp
    cur_temp += max(-cur_temp, amount) if amount < 0 else amount


def _record_overcharge(time: float) -> None:
    global good_battery_health

    while attempts_above_90 and time - attempts_above_90[0] > BATTERY_HEALTH_WINDOW:
        _ = attempts_above_90.pop(0)
    attempts_above_90.append(time)
    if len(attempts_above_90) >= 3:
        good_battery_health = False


def initialize() -> None:
    """Initializes the global variables needed for the simulation and should only be called on startup"""
    # note: temp and percentage can never go below 0
    global cur_temp  # in degrees Celsius
    global cur_battery  # in percentage points
    global cur_time  # in minutes
    global good_battery_health  # boolean
    global attempts_above_90  # list

    # default variable state
    cur_time = 0
    good_battery_health = True
    cur_battery = 50.0
    cur_temp = 20.0
    attempts_above_90 = []  # list of timestamps when you charged above 90. if the cur time - back > 60 * 6 = 360 minutes, kick it out of there. then if len(this) is 3, slow charging time


def simulate_activity(activity: str, duration: float) -> None:
    if duration <= 0 or activity.lower() not in ("charge", "use", "idle"):
        return

    global cur_time

    match activity.lower():
        case "charge":
            # fast charging is normal, as health transition cant happen here
            fc_duration: float = min(duration, duration_fast_charge_possible())
            _change_battery(fc_duration * FC_PERCENT_RATE)
            _change_temp(fc_duration * FC_TEMP_RATE)
            cur_time += fc_duration

            # slow charging
            slow_duration: float = duration - fc_duration
            # time to 90 percent, zero if already there
            time_to_90: float = max(0, (90 - cur_battery) / SC_PERCENT_RATE)
            # time before 90. either the slow duration (if we never hit 90 or just hit it), or time until 90
            before_90: float = min(slow_duration, time_to_90)
            _change_battery(before_90 * SC_PERCENT_RATE)
            _change_temp(before_90 * SC_TEMP_RATE)
            cur_time += before_90

            if good_battery_health and before_90 == time_to_90:
                _record_overcharge(cur_time)

            remaining: float = slow_duration - before_90
            _change_battery(remaining * SC_PERCENT_RATE)
            _change_temp(remaining * SC_TEMP_RATE)
            cur_time += remaining

        case "use":
            dur_until_dead: float = min(
                get_cur_charge() / abs(DEPLETING_PERCENT_RATE), duration
            )
            dur_after_dead: float = duration - dur_until_dead
            _change_battery(duration * DEPLETING_PERCENT_RATE)
            _change_temp(dur_until_dead * DEPLETING_TEMP_RATE)
            _change_temp(dur_after_dead * DEAD_TEMP_RATE)
            cur_time += duration

        case "idle":
            _change_battery(duration * IDLE_PERCENT_RATE)
            _change_temp(duration * IDLE_TEMP_RATE)
            cur_time += duration
        case _:
            pass


def duration_fast_charge_possible() -> float:
    # Fast charging occurs when the temperature is between 0-40°C, battery charge is below 80%, and battery health is good.
    cur_charge: float = get_cur_charge()
    if not get_cur_battery_health():  # health =0
        return 0
    if cur_charge >= FC_PERCENTAGE_RANGE[1]:  # we cant fastcharge no more
        return 0
    if (
        not FC_TEMP_RANGE[0] <= (temp := get_cur_temp()) <= FC_TEMP_RANGE[1]
    ):  # temp is in fc temp range
        return 0
    temp_time: float = (FC_TEMP_RANGE[1] - temp) / FC_TEMP_RATE
    charge_time: float = (FC_PERCENTAGE_RANGE[1] - cur_charge) / FC_PERCENT_RATE
    return min(temp_time, charge_time)
    # temp until 40


def get_cur_temp() -> float:
    return cur_temp


def get_cur_charge() -> float:
    return cur_battery


def get_cur_battery_health() -> bool:
    return good_battery_health


def charge_time_needed(minutes: float) -> float | None:
    battery_needed: float = minutes * abs(DEPLETING_PERCENT_RATE)
    battery_missing: float = battery_needed - get_cur_charge()

    # we got the battery you need
    if battery_missing <= 0:
        return 0

    max_battery: int = 100 if get_cur_battery_health() else BAD_HEALTH_LIMIT
    # even on full charge it would be impossible
    if battery_needed > max_battery:
        return None

    fast_duration: float = duration_fast_charge_possible()
    fast_charge_available: float = fast_duration * FC_PERCENT_RATE

    # just fast charge does it
    if battery_missing <= fast_charge_available:
        return battery_missing / FC_PERCENT_RATE

    slow_charge_start: float = get_cur_charge() + fast_charge_available
    slow_time_needed: float = (battery_needed - slow_charge_start) / SC_PERCENT_RATE

    if get_cur_battery_health() and battery_needed > 90:
        # either were at/past 90, or not
        time_before_90: float = max(
            0, (90 - slow_charge_start) / SC_PERCENT_RATE
        )
        # the time we hit the overcharge (cur time aint updated yet)
        overcharge_time: float = cur_time + fast_duration + time_before_90
        recent_overcharges: int = sum(
            overcharge_time - timestamp <= BATTERY_HEALTH_WINDOW
            for timestamp in attempts_above_90
        )
        # we cant charge more
        if recent_overcharges >= 2:
            return None

    return fast_duration + slow_time_needed


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
