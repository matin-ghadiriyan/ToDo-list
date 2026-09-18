"""WTForms form definitions."""
from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, SelectField, DateField, SubmitField
from wtforms.validators import DataRequired, Length, Optional


class TaskForm(FlaskForm):
    """Form used to create or edit a task."""

    title = StringField(
        "عنوان کار",
        validators=[DataRequired(message="عنوان الزامی است"), Length(max=200)],
    )
    description = TextAreaField(
        "توضیحات", validators=[Optional(), Length(max=2000)]
    )
    priority = SelectField(
        "اولویت",
        choices=[
            ("low", "کم"),
            ("normal", "معمولی"),
            ("high", "زیاد"),
        ],
        default="normal",
    )
    due_date = DateField("تاریخ سررسید", validators=[Optional()], format="%Y-%m-%d")
    submit = SubmitField("ذخیره")
