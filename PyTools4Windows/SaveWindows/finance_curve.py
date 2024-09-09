import numpy as np
import matplotlib as mpl
from typemacros import list_union, dict_union

#dt = 1 / 365



#Make new curve copy old curve data at 'time' and adjust.
#In other words, find a functor Curve -> Curve that adds, removes, and/or modifies
#the different equation components.
#Have these equation components be stored in lists in Curve.

"""""
class Curve():
    vars_ = {
        "starting_funds":0, "baseline":0, "money_in":0, "monthly_expenses":0,
        "loan_principle":0, "loan_repayment_amount":0, "apr":0,
        "inflation":0, "savings_interest":0
    }

    def __init__(self, time, starting_funds = 0, inflation = 0,
                 loans = [], savings = [],
                 expenses = [], incomes = []
                 ):
        self.time = time
        self.loans = loans
        self.savings = savings
        self.expenses = expenses
        self.incomes = incomes
        self.starting_funds = starting_funds
        self.inflation = inflation


    def __call__(self, new):
        new.loans = list_union(self.loans, new.loans)
        new.savings = list_union(self.savings, new.savings)
        new.expenses = list_union(self.expenses, new.expenses)
        new.incomes = list_union(self.incomes, new.incomes)

        

    def total_funds(self, t):
        return self.income(t) - self.expense(t) - self.loan_repayment(t)


    def income(self, t):
        T = 0
        for savings in self.savings:
            T += savings.savings_amount * ((1 + savings.savings_interest)**t - 1)
        for income in self.incomes:
            T += income.money_in * t
        T += self.starting_funds
        return T


    def expense(self, t):
        T = 0
        for expense in self.expenses:
            T += (12 * expense.monthly_expenses * t) * (1 + self.inflation)**t
        return T


    def loan_repayment(self, t):
        T = 0
        for loan in self.loans:
            T += 12 * loan.loan_repayment_amount * ((1 + loan.apr)**t - 1) / loan.apr
        return T
"""""

class Curve():
    def __init__(self):
        stats0 = {"slope":2, "principle":2}
        self.events = {0.0:Event(0, **stats0)} #indexed by time


    def new_event(self, event):
        time = event.time
        if time in self.events.keys():
            self.events[time] = self.events[time] + event
        else:
            self.events[time] = event


    def draw(self):
        def plot(t, x):
            print(t, x)
            pass

        t0 = 0.0
        dt = 0.1
        t_max = 2

        round_to_interval = lambda x: round(x / dt) / (1/dt)

        event = self.events[0]
        for t in np.arange(0, t_max, dt):

            #update current object on event
            if t in map(round_to_interval, self.events.keys()):

                rounds = {}
                T = 1.0e9
                for n in sorted(self.events.keys()):
                    d = max(abs(n - t), dt/2)
                    if d <= T:
                        if d in rounds.keys():
                            rounds = {d:rounds[d] + self.events[n]} #combine objects that are equidistant
                        else:
                            rounds = {d:self.events[n]}
                        T = d

                #All event interpolations go here
                new_event = rounds[T]  #Shift vertical offset at each new point
                new_event["principle"] = self.curve(t, event) - self.curve(t, rounds[T]) \
                                          + 2 * new_event["principle"] - event["principle"]
                event = new_event

            plot(round_to_interval(t), self.curve(t, event))


    def curve(self, t: float, obj):
        equation = lambda x, o: x*o["slope"] + o["principle"]
        return equation(t, obj)



class Event():
        def __init__(self, time: float, **kwargs):
            self.time = time
            self.data = kwargs

        def __add__(self, other):
            return Event(other.time, **(self.data | other.data))

        def __radd__(self, other):
            return self if other == 0 else self.__add__(other)

        def __getitem__(self, item):
            return self.data[item]

        def __setitem__(self, key, value):
            self.data[key] = value




curve = Curve()

curve.new_event(Event(1.0, principle = 2, slope = 1))
curve.new_event(Event(1.5, principle = 0))

curve.draw()