from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, DateField
from wtforms.validators import DataRequired, Email, Length, EqualTo, Regexp, Optional
from datetime import date

class SimpleRegistrationForm(FlaskForm):
    username = StringField('사용자명', validators=[
        DataRequired(message="사용자명을 입력해주세요."),
        Length(min=3, max=20, message="사용자명은 3-20자 사이여야 합니다."),
        Regexp('^[A-Za-z0-9_]+$', message="사용자명은 영문, 숫자, 언더스코어만 사용 가능합니다.")
    ])
    
    email = StringField('이메일', validators=[
        DataRequired(message="이메일을 입력해주세요."),
        Email(message="올바른 이메일 형식을 입력해주세요.")
    ])
    
    full_name = StringField('이름', validators=[
        DataRequired(message="이름을 입력해주세요."),
        Length(min=2, max=50, message="이름은 2-50자 사이여야 합니다.")
    ])
    
    phone = StringField('전화번호', validators=[
        Optional(),
        Length(max=20, message="전화번호는 최대 20자까지 입력 가능합니다.")
    ])
    
    birth_date = DateField('생년월일', validators=[
        Optional()
    ])
    
    password = PasswordField('비밀번호', validators=[
        DataRequired(message="비밀번호를 입력해주세요."),
        Length(min=6, message="비밀번호는 최소 6자 이상이어야 합니다.")
    ])
    
    password_confirm = PasswordField('비밀번호 확인', validators=[
        DataRequired(message="비밀번호 확인을 입력해주세요."),
        EqualTo('password', message="비밀번호가 일치하지 않습니다.")
    ])
    
    submit = SubmitField('가입하기')