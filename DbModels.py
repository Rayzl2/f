from peewee import *

db = SqliteDatabase('users.db')


class BaseModel(Model):
    class Meta:
        database = db

class Deposits(BaseModel):
	#ransaction_id = IntegerField(unique=True)
	user_id = IntegerField()
	summ = IntegerField()
	#payment_status = BooleanField(default=False)

	@classmethod
	def create_order(cls, user_id, amount):
		order, created = cls.get(user_id=user_id, summ=amount)
		

class Withdraws(BaseModel):
	#transaction_id = IntegerField(unique=True)
	user_id = IntegerField()
	summ = IntegerField(default=1000)
	#payment_status = BooleanField(default=False)

class CasinoBalance(BaseModel):
    spent_mode = BooleanField(default=False)
    balance = IntegerField(default=0)
    period = IntegerField()

    @classmethod
    def add_balance(cls, money):
        try:
            el = cls.get(cls.period == 10)
            el.balance += int(float(money))
            el.save()
        except Exception as e:
            print(e)

    @classmethod
    def lose_balance(cls, money):
        try:
            el = cls.get(cls.period == 10)
            el.balance -= int(float(money))
            el.save()
        except Exception as e:
            print(e)

class Users(BaseModel):
    user_id = IntegerField(unique=True)
    balance = IntegerField(default=0)
    chance = TextField(default='0.2')
    prime = BooleanField(default=False)
    alltime_deposit = IntegerField(default=0)
    alltime_withdraw = IntegerField(default=0)
    profit = IntegerField(default=0)
    #parent_id = IntegerField(default=0)

    @classmethod
    def user_exists(cls, user_id):
        query = cls().select().where(cls.user_id == user_id) 
        return query.exists()

    @classmethod
    def create_user(cls, user_id):
        user, created = cls.get_or_create(user_id=user_id)

    @classmethod
    def get_about(cls, user_id):
    	obj = cls.get_user(user_id)
    	obj_list = [obj.user_id, obj.balance, obj.alltime_deposit, obj.alltime_withdraw]
    	return obj_list

    @classmethod
    def get_all_stats(cls, user_id):
        obj = cls.get_user(user_id)
        obj_list = [obj.user_id, obj.balance, obj.alltime_deposit, obj.alltime_withdraw, obj.chance, obj.prime, obj.profit]
        return obj_list

    @classmethod
    def get_user(cls, user_id):
        return cls.get(cls.user_id == user_id)


    @classmethod
    def add_balance(cls, user_id, money):
        try:
            el = cls.get(cls.user_id == user_id)
            el.balance += int(money)
            el.save()
        except Exception as e:
            print(e)

    @classmethod
    def lose_balance(cls, user_id, money):
        try:
            el = cls.get(cls.user_id == user_id)
            el.balance -= int(money)
            el.save()
        except Exception as e:
            print(e)

    @classmethod
    def add_deposit(cls, user_id, money):
        try:
            el = cls.get(cls.user_id == user_id)
            el.alltime_deposit += int(money)
            el.save()
        except Exception as e:
            print(e)

    @classmethod
    def change_balance(cls, user_id, money):
        try:
            el = cls.get(cls.user_id == user_id)
            el.balance = int(money)
            el.save()
        except Exception as e:
            print(e)




db.create_tables([Users, Deposits, Withdraws, CasinoBalance])