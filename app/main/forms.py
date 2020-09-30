from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, SubmitField, SelectField, RadioField
from wtforms.validators import DataRequired, Length, Email


class ContactForm(FlaskForm):
    name = StringField('Ваше имя', validators=[Length(8, 64), DataRequired()])
    email = StringField('E-Mail', validators=[Length(1, 64), Email(), DataRequired()])
    enquiry = TextAreaField('Проблема', validators=[DataRequired()], render_kw={'style': 'resize: vertical; min-height: 150px'})
    submit = SubmitField('Отправить')


class HowManyProducts(FlaskForm):
    howMany = SelectField('Показывать:', choices=[12, 24, 36])


class SortingForm(FlaskForm):
    sortBy = SelectField('Сортировать по:', choices=['популярности', 'рейтингу',
                                                     'возрастанию цены', 'убыванию цены'])


class ShippingForm(FlaskForm):
    FirstName = StringField('Фамилия', validators=[Length(1, 64), DataRequired()])
    LastName = StringField('Имя', validators=[Length(1, 64), DataRequired()])
    Email = StringField('E-Mail', validators=[Length(8, 64), Email(), DataRequired()])
    phone = StringField('Телефон', validators=[DataRequired()])
    town = StringField('Полный адрес')
    postcode = StringField('Почтовый индекс')
    submit = SubmitField('Продолжить')


class ReviewForm(FlaskForm):
    name = StringField('Ваши имя и фамилия', validators=[Length(8, 64), DataRequired()])
    enquiry = TextAreaField('Комментарий', validators=[DataRequired()])
    rating = RadioField('Рейтинг:', choices=[1, 2, 3, 4, 5])
    submit = SubmitField('Отправить')


class DeliveryandPaymentForm(FlaskForm):
    deliverychoice = RadioField('Способ доставки:', choices=[('Самовывоз', 'Самовывоз'), ('Курьером', 'Курьером'), ('Почтой', 'Почтой')], validators=[DataRequired()])
    paymentchoice = RadioField('Способ оплаты:', choices=['Оплата картой на сайте', 'Оплата при получении'], validators=[DataRequired()])
    submit = SubmitField('Продолжить')
