import os
from peewee import (
    SqliteDatabase, Model, AutoField, IntegerField, CharField,
    TextField, DateTimeField, DoesNotExist, fn
)
from datetime import datetime

DB_PATH = os.path.join(os.path.dirname(__file__), "..", "bookings.db")
db = SqliteDatabase(DB_PATH)


class UserQuery(Model):
    id = AutoField()
    user_id = IntegerField(verbose_name="Telegram ID")
    command = CharField(max_length=50, verbose_name="Команда")
    params = TextField(null=True, verbose_name="Параметры")
    created_at = DateTimeField(default=datetime.now, verbose_name="Время")

    class Meta:
        database = db
        table_name = "user_queries"


class Booking(Model):
    id = AutoField()
    apartment_name = CharField(max_length=200, verbose_name="Квартира")
    checkin_date = CharField(max_length=20, verbose_name="Заезд")
    checkout_date = CharField(max_length=20, verbose_name="Выезд")
    nights = IntegerField(verbose_name="Ночей")
    guests = IntegerField(verbose_name="Гостей")
    customer_name = CharField(max_length=100, verbose_name="Имя")
    customer_phone = CharField(max_length=50, verbose_name="Телефон")
    user_id = IntegerField(null=True, verbose_name="Telegram ID")
    username = CharField(max_length=100, null=True, verbose_name="Username")
    created_at = DateTimeField(default=datetime.now, verbose_name="Создано")
    status = CharField(max_length=20, default="new", verbose_name="Статус")

    class Meta:
        database = db
        table_name = "bookings"


def init_db():
    db.connect()
    db.create_tables([Booking, UserQuery], safe=True)
    print("✅ База данных инициализирована (Peewee)")


def add_booking(booking_data):
    booking = Booking.create(
        apartment_name=booking_data["apartment_name"],
        checkin_date=booking_data["checkin"],
        checkout_date=booking_data["checkout"],
        nights=booking_data["nights"],
        guests=booking_data["guests"],
        customer_name=booking_data["customer_name"],
        customer_phone=booking_data["customer_phone"],
        user_id=booking_data["user_id"],
        username=booking_data["username"],
    )
    return booking.id


def get_bookings(limit=50):
    bookings = Booking.select().order_by(Booking.created_at.desc()).limit(limit)

    return [
        (
            b.id,
            b.apartment_name,
            b.checkin_date,
            b.checkout_date,
            b.customer_name,
            b.customer_phone,
            b.status,
            b.created_at.strftime("%Y-%m-%d %H:%M"),
        )
        for b in bookings
    ]


def get_booking_by_id(booking_id):
    try:
        return Booking.get_by_id(booking_id)
    except DoesNotExist:
        return None


def update_booking_status(booking_id, status):
    query = Booking.update(status=status).where(Booking.id == booking_id)
    query.execute()


def get_statistics():
    total = Booking.select().count()
    today = (
        Booking.select()
        .where(
            Booking.created_at.year == datetime.now().year,
            Booking.created_at.month == datetime.now().month,
            Booking.created_at.day == datetime.now().day,
        )
        .count()
    )

    popular = (
        Booking.select(Booking.apartment_name, fn.COUNT(Booking.id).alias("count"))
        .group_by(Booking.apartment_name)
        .order_by(fn.COUNT(Booking.id).desc())
        .limit(5)
    )

    return {
        "total": total,
        "today": today,
        "popular": [(p.apartment_name, p.count) for p in popular],
    }


def get_bookings_by_phone(phone):
    bookings = Booking.select().where(Booking.customer_phone.contains(phone))
    return list(bookings)


def save_user_query(user_id, command, params):
    UserQuery.create(user_id=user_id, command=command, params=params)


def get_user_bookings(user_id, limit=10):
    return (
        Booking.select()
        .where(Booking.user_id == user_id)
        .order_by(Booking.created_at.desc())
        .limit(limit)
    )