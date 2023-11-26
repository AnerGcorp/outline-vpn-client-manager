
INTERVAL = 30
PENALTY = 0
REMAINING = 30
NUMBER_OF_DEVICES = 1
PRICE = 100
PAID = False
DEBT = 0
DISCOUNT = 0

class Client(object):
	def __init__(self):
		self.id = None
		self.name = None
		self.phone = None
		self.mail = None
		self.device = NUMBER_OF_DEVICES
		self.price = PRICE
		self.discount = DISCOUNT
		self.key = None
		self.server = None
		self.startDate = None
		self.expireDate = None
		self.interval = INTERVAL
		self.penalty = PENALTY
		self.remaining = REMAINING
		self.paid = PAID
		self.status = None
		self.debt = DEBT

	def to_dict(self):
		return {
        "_id": self.id,
        "name": self.name,
        "phone": self.phone,
        "mail": self.mail,
		"device": self.device,
		"price": self.price,
		"discount": self.discount,
        "key": self.key,
        "server": self.server,
        "startDate": self.startDate,
        "expireDate": self.expireDate,
        "interval": self.interval,
        "penalty": self.penalty,
        "remaining": self.remaining,
        "paid": self.paid,
		"debt": self.debt,
        "status": self.status
    }
