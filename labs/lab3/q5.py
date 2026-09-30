class Student:
    def __init__(self):
        self.knols: int = 0
        self.coffee_times: list[int] = []
        self.time: int = 0
        self.too_much_coffee: bool = False
        self.just_drank_coffee: bool = False
    def drink_coffee(self):
        self.coffee_times.append(self.time)
        self.just_drank_coffee = True
        if len(self.coffee_times) >= 3:
            if self.coffee_times[-1] - self.coffee_times[-3] <= 120:
                self.too_much_coffee = True
    def study(self, minutes: int):
        if not self.too_much_coffee:
            if self.just_drank_coffee:
                self.knols += minutes * 10
            else:
                self.knols += minutes * 5
        self.time += minutes
        self.just_drank_coffee = False


# if __name__ == '__main__':
s = Student()
s.study(60)
s.study(20)
s.drink_coffee()
s.study(10)
s.drink_coffee()
s.study(10)
s.drink_coffee()
s.study(10)

