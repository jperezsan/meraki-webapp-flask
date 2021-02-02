from flask import render_template, redirect, request, url_for, flash
from flask_login import login_user, logout_user, login_required

from . import auth
from .. import db
from ..decorators import permission_required
from ..models import User, Permission, Role

from .forms import LoginForm, RegistrationForm, ChangeRoleForm


@auth.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data.lower()).first()
        if user is not None and user.verify_password(form.password.data):
            login_user(user, form.remember_me.data)
            next = request.args.get('next')
            if next is None or not next.startswith('/'):
                next = url_for('main.index')

            flash('Successful login')
            return redirect(next)
        flash('Invalid email or password.')
    return render_template('auth/login.html', form=form)


@auth.route('/logout')
@login_required
def logout():
    logout_user()
    flash('You have been logged out.')
    return redirect(url_for('main.index'))


@auth.route('/register', methods=['GET', 'POST'])
@login_required
@permission_required(Permission.ADD_USERS)
def register():
    roles = Role.query.all()
    form = RegistrationForm(roles)
    if form.validate_on_submit():
        user = User(email=form.email.data.lower(),
                    username=form.email.data.lower(),
                    full_name=form.full_name.data,
                    password=form.password.data)

        role = Role.query.filter_by(name=form.user_role.data).first()
        user.role = role

        db.session.add(user)
        db.session.commit()
        flash('User added correctly!')

        form = RegistrationForm(roles)
        return render_template('auth/register.html', form=form)
    return render_template('auth/register.html', form=form)


@auth.route('/users', methods=['GET'])
@login_required
def users():
    all_users = User.query.all()
    return render_template('auth/users.html', users=all_users)


@auth.route('/changeUserRole', methods=['GET', 'POST'])
@login_required
@permission_required(Permission.ADD_USERS)
def change_user_role():
    roles = Role.query.all()
    form = ChangeRoleForm(roles)
    user_id = int(request.args.get('userid'))
    form.user_id = user_id

    if form.validate_on_submit():
        user = User.query.filter_by(id=form.user_id).first()
        role = Role.query.filter_by(name=form.user_role.data).first()
        user.role = role
        db.session.commit()
        flash("User with new Role must logout and login again.")
        return redirect(url_for('auth.users'))

    user = User.query.get(user_id)
    return render_template('auth/changeUserRole.html', user=user, form=form)


@auth.route('/deleteUser', methods=['GET', 'POST'])
@login_required
@permission_required(Permission.ADD_USERS)
def delete_user():
    user_id = int(request.args.get('userid'))

    if request.method == 'POST':
        User.query.filter_by(id=user_id).delete()
        db.session.commit()
        flash("User deleted")
        return redirect(url_for('auth.users'))

    user = User.query.get(user_id)
    return render_template('auth/deleteUser.html', user=user)
