import os
from sqlalchemy import *
from sqlalchemy.pool import NullPool
from flask import Flask, request, render_template, g, redirect, Response, url_for, flash
from flask_login import login_user, logout_user, current_user, login_required, LoginManager
import click
from forms import LoginForm, CustomerForm1, CustomerTable1, CashierForm, CashierGoodForm, ManagerForm
import os
from model import User, Customer, Employee
from datetime import date

dburl = "postgresql://nm3150:0611@34.74.165.156/proj1part2"

tmpl_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'templates')
app = Flask(__name__, template_folder=tmpl_dir)

login = LoginManager(app)
login.login_view = 'login'
@login.user_loader
def load_user(user_id):
    return User(user_id)


SECRET_KEY = os.urandom(32)
app.config['SECRET_KEY'] = SECRET_KEY
engine = create_engine(dburl)
conn = engine.connect()

@click.command()
@click.option('--debug', is_flag=True)
@click.option('--threaded', is_flag=True)
@click.argument('HOST', default='0.0.0.0')
@click.argument('PORT', default=8111, type=int)
def run(debug, threaded, host, port):
    print("here")
    print("running on %s:%d" % (host, port))
    # app.run()

@app.route('/', methods = ['GET', 'POST'])
@app.route('/index', methods = ['GET', 'POST'])
def index():
    context = dict()
    context['title'] = 'Home'
    context['user'] = {'username': 'Jeff'}
    form = LoginForm()
    context['form'] = form

    if form.validate_on_submit():
        temp_usrname = form.username.data
        temp_pswd = form.password.data
        temp_id = form.identity.data
        temp_id_pswd = ''
        if temp_id == 'customer':
            temp_id_pswd = 'c'
        if temp_id == 'employee':
            temp_id_pswd = 'employ'
        cursor = conn.execute('select ' + temp_id_pswd + 'pswd from ' + temp_id + ' where ' + temp_id_pswd + 'id = ' + '\'' + temp_usrname + '\'')
        pswd = ""
        for result in cursor:
            if temp_id == 'customer':
                pswd = str(result['cpswd']).strip()
            if temp_id == 'employee':
                pswd = str(result['employpswd']).strip()
        if pswd != temp_pswd:
            flash('invalid')
            print("here")
            print(form.identity.data)
            next_page = url_for('index')
            return redirect(next_page)
        else:
            cursor.close()
            flash('success')
            current_user = User(temp_usrname)
            login_user(current_user)
            next_page = url_for('login_success_' + temp_id)
            return redirect(next_page)

    return render_template('index.html', **context)

@app.route('/login_success_customer', methods = ['GET', 'POST'])
def login_success_customer():
    context = dict()
    # load basic information
    cursor = conn.execute('select * from customer where cid = \'' + current_user.id + '\'')
    context['id'] = current_user.id
    for result in cursor:
        context['cname'] = result['cname'].strip()
        context['mid'] = result['mid'].strip()
        context['caddr'] = result['caddr'].strip()
    cursor.close()
    # load membership information
    cursor1 = conn.execute('select * from membership where mid = \'' + context['mid'] + '\'')
    for result1 in cursor1:
        context['mlvl'] = result1['mlvl'].strip()
        context['mexpr'] = result1['mexpr']
        context['mbalance'] = result1['mbalance']
    cursor1.close()
    
    form1 = CustomerForm1()
    context['form1'] = form1

    # load billing information
    # TODO: add date filter
    context['columns'] = ('Bill ID', 'Amount', 'Quantity', 'Cashier', 'Date', 'Payment')
    cursor2 = conn.execute('select billid, billpaid, quantity, employid, billdate, billpmnt from bill where cid = \'' + context['id'] + '\'')
    item = []
    for result2 in cursor2:
        item.append(result2)
    print(item)
    context['items'] = item
    # if form1.validate_on_submit():
    #     cursor2 = conn.execute('select bid, billpaid, quantity, employid, billdate, billpmnt from bill where cid = \'' + context['id'] + '\'')
    #     table1 = Table(cursor2)
    #     context['table'] = table1    
    #     cursor2.close()
    cursor2.close()
    return render_template('login-success-customer.html', **context)

# global values required for cashier
global cart
cart = []
@app.route('/login_success_employee', methods = ['GET', 'POST'])
def login_success_employee():
    context = dict()
    # load basic information
    cursor = conn.execute('select * from employee where employid = \'' + current_user.id + '\'')
    context['id'] = current_user.id

    for result in cursor:
        context['employname'] = result['employname'].strip()
        context['employpos'] = result['employpos'].strip()
    cursor.close()
    
    # load customer part
    cashierform = CashierForm()
    context['cashierform'] = cashierform
    cashiergoodform = CashierGoodForm()
    context['cashiergoodform'] = cashiergoodform
    context['cart'] = cart   
    
    if cashierform.validate_on_submit():
        context['cur_cust_id'] = cashierform.customerid.data
        if cashierform.submit.data == True:
            cursor = conn.execute('select * from customer where cid = \'' + cashierform.customerid.data + '\'')
            for result in cursor:
                # context['cur_cust_id'] = cashierform.customerid.data
                context['cur_cust_name'] = result['cname'].strip()
            cursor.close()
            if 'cur_cust_name' in context.keys() and context['cur_cust_name'] != None:
                messagefound = 'Found customer: ' + cashierform.customerid.data + '. Now working on ' + context['cur_cust_name'] +'.'
                context['messagefound'] = messagefound
                return render_template('login-success-employee.html', **context)
            else:
                messagefound = 'Customer not found. Please try again'
                context['messagefound'] = messagefound
            
        elif cashierform.clear.data == True:
            context['cur_cust_id'] = None
            context['cur_cust_name'] = None
            cashierform.customerid.data = ''
            messagefound = 'Cleared!'
            context['messagefound'] = messagefound
        
        elif cashierform.submit1.data == True:
            cursor = conn.execute('select * from goods where goodbatch = \'' + cashiergoodform.goodid.data + '\' and storage > ' + cashierform.quantity.data)
            gprice = None
            for result in cursor:
                temp_goodname = ''
                temp_manufactor = ''
                gprice = result['gprice']
                cursor1 = conn.execute('select * from supplierapprovedBy where invoiceid = \'' + result['invoiceid'] + '\'')
                for result1 in cursor1:
                    temp_goodname = result1['goodname']
                    temp_manufactor = result1['suppliername']
                cursor1.close()
                cart.append((temp_goodname, temp_manufactor, cashierform.quantity.data, gprice, cashierform.submit1.data))
        
        elif cashierform.checkout.data == True:
            cursor = conn.execute('select billid from bill where billdate = (select max(billdate) from bill)')
            temp_billid = ''
            for result in cursor:
                temp_billid = result['billid']
            cursor.close()
            new_billid = int(temp_billid) + 1
            new_billid = str(new_billid).zfill(10)
            nowdate = date.today().strftime('%Y-%m-%d')
            for row in cart:
                payment = int(row[2]) * float(row[3])
                billpmnt = 'cash'
                execution = 'insert into bill values (\'' + new_billid + '\', \'' + nowdate +'\','  + str(payment) +', + ' + str(row[2]) + ', \'' + context['cur_cust_id'] + '\', \'' + current_user.id + '\', \'' + cashiergoodform.goodid.data + '\', \'' + billpmnt + '\')'
                print(execution)
                cursor = conn.execute(execution)
                cursor.close()
                # TODO: storage - 1
                # TODO: notify on successful
                # TODO: option on payment
    
    # manager form
    managerform = ManagerForm()
    context['managerform'] = managerform
    worker_list = []
    cursor = conn.execute('select * from employee where employpos = \'cashier\' or employpos = \'tallyman\'')
    for result in cursor:
        managerform.workers.choices.append((result['employid'], result['employname']))
    cursor.close()
    supplement = dict()
    cursor = conn.execute('select * from supplierapprovedBy where managerid = \'' + current_user.id + '\'')
    for result in cursor:
        managerform.suppliers.choices.append((result['supplierid'], result['goodname'] + 'from ' + result['suppliername']))
        if result['suppliername'] not in supplement:
            supplement[result['suppliername']] = [result['goodname']]
        else:
            supplement[result['suppliername']].append(result['goodname'])
    cursor.close()
    print(managerform.suppliers.choices)
    print(supplement)
    if managerform.validate_on_submit():
        if managerform.suppliers.data in supplement.keys():
            managerform.goods.choices = supplement[managerform.suppliers.data]
    # add to cart part
    # if cashiergoodform.validate_on_submit():
    #     print(cart)
    #     print("here")
    #     cursor = conn.execute('select * from goods where goodbatch = \'' + cashiergoodform.goodid.data + '\' and storage > ' + cashiergoodform.quantity.data)
    #     for result in cursor:
    #         temp_goodname = ''
    #         temp_manufactor = ''
    #         cursor1 = conn.execute('select * from supplierapprovedBy where invoiceid = \'' + result['invoiceid'] + '\'')
    #         for result1 in cursor1:
    #             temp_goodname = result1['goodname']
    #             temp_manufactor = result1['suppliername']
    #         cursor1.close()
    #         cart.append(('dsa'))
    #     return render_template('login-success-employee.html', **context)
    return render_template('login-success-employee.html', **context)

if __name__ == "__main__":
    app.run(debug = true, port=8111)
