from flask import Blueprint, render_template, request, flash, redirect, url_for, session
from app.controllers.auth_controller import AuthController
from app.schemas.auth_schema import SimpleRegistrationForm, LoginForm

bp = Blueprint('auth', __name__, url_prefix='/auth')
auth_controller = AuthController()

@bp.route('/login', methods=['GET', 'POST'])
def login():
    """로그인 페이지"""
    form = LoginForm()
    
    if form.validate_on_submit():
        redirect_page = auth_controller.login(form)
        if redirect_page:
            return redirect(url_for(redirect_page))
    
    return render_template('login.html', form=form)

@bp.route('/logout')
def logout():
    """로그아웃"""
    redirect_page = auth_controller.logout()
    return redirect(url_for(redirect_page))

@bp.route('/register', methods=['GET', 'POST'])
def register():
    """회원가입 페이지"""
    form = SimpleRegistrationForm()
    
    if form.validate_on_submit():
        redirect_page = auth_controller.register(form)
        if redirect_page:
            return redirect(url_for(redirect_page))
    
    return render_template('team5.html', form=form) 