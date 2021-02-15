# -*- encoding:utf-8 -*-
class Request(object):
    def __init__(self):
        pass


class ApplyRequest(Request):
    def __init__(self, user, money):
        super(ApplyRequest, self).__init__()
        self.user = user
        self.money = money


class TravelRequest(Request):
    def __init__(self, user, days):
        super(TravelRequest, self).__init__()
        self.user = user
        self.days = days


class Handler(object):
    def __init__(self):
        self.next = None

    def set_next(self, _next):
        if not isinstance(_next, Handler):
            raise TypeError("Expected type Handler, got {}".format(type(_next)))
        self.next = _next

    def handle(self, request):
        raise NotImplementedError


class PM(Handler):
    def __init__(self):
        super(PM, self).__init__()

    def handle(self, request):
        if not isinstance(request, ApplyRequest):
            return super(PM, self).handle(request)
            # raise TypeError(
            #     "Can only handle ApplyRequest, got {}".format(type(request)))
        return self.__handle(request)

    def __handle(self, request):
        if request.money < 100:
            return "PM {} agree {} {} apply".format(
                id(self), request.user, request.money)

        return self.next.handle(request)


class PMRedefine(PM):
    def __init__(self):
        super(PMRedefine, self).__init__()

    def handle(self, request):
        if not isinstance(request, TravelRequest):
            return super(PMRedefine, self).handle(request)
        return self.__handle(request)

    def __handle(self, request):
        if request.days <= 3:
            return "PMRedefine {} agree {} {} days".format(
                id(self), request.user, request.days)
        return self.next.handle(request)


class Manager(Handler):
    def __init__(self):
        super(Manager, self).__init__()

    def handle(self, request):
        if not isinstance(request, ApplyRequest):
            return super(Manager, self).handle(request)
            # raise TypeError(
            #     "Can only handle ApplyRequest, got {}".format(type(request)))
        return self.__handle(request)

    def __handle(self, request):
        if request.money >= 100:
            return "Manager {} agree {} {} apply".format(
                id(self), request.user, request.money)
        return self.next.handle(request)


class ManagerRedefine(Manager):
    def __init__(self):
        super(ManagerRedefine, self).__init__()

    def handle(self, request):
        if not isinstance(request, TravelRequest):
            return super(ManagerRedefine, self).handle(request)
        return self.__handle(request)

    def __handle(self, request):
        if request.days > 3:
            return "ManagerRedefine {} agree {} {} days".format(
                id(self), request.user, request.days)


if __name__ == '__main__':
    ar = ApplyRequest("DJH", 100)
    pm = PM()
    manager = Manager()
    pm.set_next(manager)
    res = pm.handle(ar)
    print(res)
    print("*"*20)
    tr = TravelRequest("DDD", 4)
    pm2 = PMRedefine()
    manager2 = ManagerRedefine()
    pm2.set_next(manager2)
    res2 = pm2.handle(tr)
    print(res2)
