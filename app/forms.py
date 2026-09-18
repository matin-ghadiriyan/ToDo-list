"""WTForms form definitions with strict validation."""
from datetime import date, timedelta

from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, SelectField, DateField, SubmitField
from wtforms.validators import DataRequired, Length, Optional, ValidationError


def _no_html(form, field):
    """Reject raw HTML in text fields (defence in depth vs stored XSS)."""
    value = field.data or ""
    if "<" in value or ">" in value:
        raise ValidationError("استفاده از کاراکترهای < و > مجاز نیست.")


def _reasonable_date(form, field):
    """Keep due dates within a sane window."""
    if field.data is None:
        return
    today = date.today()
    if field.data < today - timedelta(days=365):
        raise ValidationError("تاریخ سررسید خیلی قدیمی است.")
    if field.data > today + timedelta(days=365 * 5):
        raise ValidationError("تاریخ سررسید خیلی دور است.")


class TaskForm(FlaskForm):
    """Form used to create or edit a task."""

    title = StringField(
        "عنوان کار",
        validators=[
            DataRequired(message="عنوان الزامی است"),
            Length(min=1, max=200, message="عنوان باید بین ۱ تا ۲۰۰ کاراکتر باشد"),
            _no_html,
        ],
    )
    description = TextAreaField(
        "توضیحات",
        validators=[
            Optional(),
            Length(max=2000, message="توضیحات حداکثر ۲۰۰۰ کاراکتر"),
            _no_html,
        ],
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
    due_date = DateField(
        "تاریخ سررسید",
        validators=[Optional(), _reasonable_date],
        format="%Y-%m-%d",
    )
    submit = SubmitField("ذخیره")
