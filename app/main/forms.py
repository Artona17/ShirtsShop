from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, PasswordField, SubmitField, SelectField, RadioField, BooleanField
from wtforms.validators import DataRequired, Length, Email, Regexp


class EditProfileForm(FlaskForm):
    FirstName = StringField('First Name', validators=[Length(1, 64)])
    LastName = StringField('Last Name', validators=[Length(1, 64)])
    email = StringField('E-Mail', validators=[Length(8, 64), Email()])
    phone = StringField('Telephone')
    submit = SubmitField('Submit')


class PasswordChangeForm(FlaskForm):
    password = PasswordField('Password', validators=[Length(8, 64)])
    passwordConfirm = PasswordField('Confirm Password', validators=[Length(8, 64)])


class ContactForm(FlaskForm):
    name = StringField('Ваше имя', validators=[Length(8, 64), DataRequired()])
    email = StringField('E-Mail', validators=[Length(1, 64), Email(), DataRequired()])
    enquiry = TextAreaField('Проблема', validators=[DataRequired()])
    submit = SubmitField('Отправить')


class HowManyProducts(FlaskForm):
    howMany = SelectField('Показывать:', choices=[12, 24, 36])


class SortingForm(FlaskForm):
    sortBy = SelectField('Сортировать по:', choices=['популярности', 'рейтингу',
                                                     'возрастанию цены', 'убыванию цены'])


class ShippingForm(FlaskForm):
    FirstName = StringField('Фамилия', validators=[Length(1, 64), DataRequired()])
    LastName = StringField('Имя', validators=[Length(1, 64), DataRequired()])
    FatherName = StringField('Отчество (если есть)', validators=[Length(1, 64)])
    Email = StringField('E-Mail', validators=[Length(8, 64), Email(), DataRequired()])
    phone = StringField('Телефон', validators=[DataRequired()])
    country = SelectField('Страна', choices=['Россия', 'Украина', 'Беларусь', 'Казахстан'])
    town = StringField('Полный адрес', validators=[DataRequired()])
    postcode = StringField('Почтовый индекс', validators=[DataRequired()])
    submit = SubmitField('Продолжить')


class ReviewForm(FlaskForm):
    name = StringField('Ваши имя и фамилия', validators=[Length(8, 64), DataRequired()])
    enquiry = TextAreaField('Комментарий', validators=[DataRequired()])
    rating = RadioField('Рейтинг:', choices=[1, 2, 3, 4, 5])
    submit = SubmitField('Отправить')


class DeliveryandPaymentForm(FlaskForm):
    deliverychoice = RadioField('Способ доставки:', choices=['Самовывоз\n', 'Курьером\n', 'Почтой\n'], validators=[DataRequired()])
    paymentchoice = RadioField('Способ оплаты:', choices=['Оплата картой на сайте', 'Оплата при получении'], validators=[DataRequired()])
    submit = SubmitField('Продолжить')