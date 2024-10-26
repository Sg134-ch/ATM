from flask import Flask, render_template, request, redirect, url_for, session
from models import Customer, db_init

app = Flask(__name__)
app.secret_key = 'secret_key'  # For session management

# Initialize the SQLite database
db_init()

@app.route('/')
def home():
    return redirect(url_for('login'))

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        customer = Customer.login(username, password)
        
        if customer:
            session['username'] = customer.username
            return redirect(url_for('dashboard'))
        else:
            return "Login Failed! Please check your credentials."
    return render_template('login.html')

@app.route('/dashboard')
def dashboard():
    if 'username' not in session:
        return redirect(url_for('login'))
    
    customer = Customer.get_customer(session['username'])
    return render_template('dashboard.html', customer=customer)

@app.route('/balance')
def show_balance():
    if 'username' not in session:
        return redirect(url_for('login'))
    
    customer = Customer.get_customer(session['username'])
    return render_template('show_balance.html', balance=customer.balance)

@app.route('/transaction', methods=['GET', 'POST'])
def transaction():
    if 'username' not in session:
        return redirect(url_for('login'))
    
    customer = Customer.get_customer(session['username'])
    
    if request.method == 'POST':
        amount = float(request.form['amount'])
        action = request.form['action']
        
        if action == 'deposit':
            customer.deposit(amount)
        elif action == 'withdraw':
            if customer.withdraw(amount):
                pass
            else:
                return "Insufficient funds!"
        
        return redirect(url_for('dashboard'))
    
    return render_template('transaction.html')

@app.route('/logout')
def logout():
    session.pop('username', None)
    return redirect(url_for('login'))

if __name__ == '__main__':
    app.run(debug=True)
