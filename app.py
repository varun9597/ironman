from flask import Flask, render_template, request, redirect, url_for, session, flash, jsonify
from database import get_connection
from sqlalchemy import text
import os


app = Flask(__name__)
app.secret_key = 'your_secret_key'  # Make sure to set a secure secret key

@app.route("/")
def landing_page():
    return render_template('landing_page.html')

@app.route("/signin", methods=['GET', 'POST'])
def sign_in():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        try:
            conn = get_connection()
            query = text(f"SELECT id FROM tbl_users WHERE username = '{username}' AND password = '{password}'")
            result = list(conn.execute(query).fetchone())
            print(result)

            if result:
                session['user_id'] = result[0]
                return redirect(url_for('dashboard'))
        except Exception as e:
            print("Error:", e)
            #flash('User does not exists. Please register.', 'error')
            return redirect(url_for('sign_up'))

    return render_template('sign_in.html')

@app.route("/signup", methods=['GET', 'POST'])
def sign_up():
    if request.method == 'POST':
        name = request.form['name']
        username = request.form['username']
        password = request.form['password']

        try:
            conn = get_connection()
            query = text(f"INSERT INTO tbl_users (name, username, password) VALUES ('{name}', '{username}', '{password}')")
            conn.execute(query)
            flash('Account created successfully. Please sign in.', 'success')
            return redirect(url_for('sign_in'))

        except Exception as e:
            print("Error:", e)
            flash('An error occurred while creating the account. Please try again.', 'error')

    return render_template('sign_up.html')

@app.route("/logout")
def logout():
    session.pop('user_id', None)
    flash('You have been logged out successfully', 'success')
    return redirect(url_for('sign_in'))

@app.route("/dashboard")
def dashboard():
    user = fetch_user_name()
    if user:
        return render_template('dashboard.html', username = user)
    else:
        #flash('Please sign in to access the homepage', 'error')
        return redirect(url_for('sign_in'))

def fetch_user_name():
    name = None
    if 'user_id' in session:
        user_id = session['user_id']
        conn = get_connection()
        query = text(f"select name from tbl_users where id = '{user_id}';")
        result = list(conn.execute(query).fetchone())
        if result:
            name = result[0]
        return name

@app.route("/removeflat", methods=['GET','POST'])
def removeflat():
    user = fetch_user_name()
    if 'user_id' in session:
        user_id = session['user_id']
        if request.method == 'POST':
            flat_to_remove = request.form['flatNumber']
            print(flat_to_remove)
            cust_soc_name = request.form['society']
            print(cust_soc_name)
            # Fetch soc_id from tbl_society
            soc_id = None
            cust_id_to_delete = None
            try:
                conn = get_connection()
                soc_query = text(f"SELECT pk_soc_id FROM tbl_society WHERE LOWER(soc_name) = LOWER('{cust_soc_name}') and fk_user_id = '{user_id}';")
                result = conn.execute(soc_query).fetchone()
                print(str(result)+" fetching soc_id")
                if result:
                    soc_id = list(result)[0]
                fetch_cust_id_to_delete_query = text(f"select fk_cust_id from tbl_cust_flat where lower(flat_no) = lower('{flat_to_remove}') and fk_user_id = '{user_id}' and fk_soc_id = '{soc_id}';")
                result = conn.execute(fetch_cust_id_to_delete_query).fetchone()
                if result:
                    cust_id_to_delete = list(result)[0]
                delete_flat_query = text(f"DELETE FROM tbl_cust_flat where lower(flat_no) = lower('{flat_to_remove}') and fk_user_id = '{user_id}' and fk_soc_id = '{soc_id}';")
                result = conn.execute(delete_flat_query)
                delete_cust_query = text(f"delete from tbl_customer where pk_cust_id = '{cust_id_to_delete}';")
                result = conn.execute(delete_cust_query)
            except Exception as e:
                print(e)
                return redirect(url_for("removeflat"))

        #fetch society list
        soc_list_query = text(f"SELECT soc_name from tbl_society where fk_user_id = '{user_id}';")
        try:
            conn = get_connection()
            societies = [row[0] for row in conn.execute(soc_list_query).fetchall()]
            print(societies)
        except Exception as e:
            print(e)
            societies = []
        
        return render_template('remove_flat.html',societies=societies,username = user)

    else:
        #flash('Please sign in to access the homepage', 'error')
        return redirect(url_for('sign_in'))

@app.route('/get_flats', methods = ['POST'])
def get_flats():
    if 'user_id' in session:
        user_id = session['user_id']
        data = request.json
        society_name = data.get('society')
        #society_name = request.form.get('society')
        print(society_name)
        flat_list = []
        if society_name:
            try:
                conn = get_connection()
                flat_query = text(f"SELECT flat.flat_no FROM tbl_cust_flat flat join tbl_society soc on soc.pk_soc_id = flat.fk_soc_id WHERE LOWER(soc.soc_name) = LOWER('{society_name}') and flat.fk_user_id = {user_id};")
                flats = [row[0] for row in conn.execute(flat_query).fetchall()]
                print(flats)
                flat_list = flats
            except Exception as e:
                print(e)
                return redirect(url_for("addflat"))
        # flat_list = ['Flat 101', 'Flat 102', 'Flat 103']
        flat_list_json = jsonify({'flats': flat_list})
        print(flat_list_json)
        return jsonify(flat_list)


@app.route("/addflat", methods=['GET', 'POST'])
def addflat():
    user = fetch_user_name()
    if 'user_id' in session:
        user_id = session['user_id']
        if request.method == 'POST':
            print(request.form)
            cust_name = request.form['customerName']
            print(cust_name)
            cust_flat_no = request.form['flatNumber']
            print(cust_flat_no)
            cust_soc_name = request.form['society']
            print(cust_soc_name)
            cust_phn_no = request.form['customerPhoneNumber']
            print(cust_phn_no)
            # Check if the society exists in tbl_society
            soc_id = None

            try:
                conn = get_connection()
                soc_query = text(f"SELECT pk_soc_id FROM tbl_society WHERE LOWER(soc_name) = LOWER('{cust_soc_name}') and fk_user_id = '{user_id}';")
                result = conn.execute(soc_query).fetchone()
                print(str(result)+" fetching soc_id")
                if result:
                    soc_id = list(result)[0]
            except Exception as e:
                print(e)
                return redirect(url_for("addflat"))
            #add a new entry in tbl_customer
            add_cust_query = text(f"INSERT INTO tbl_customer (cust_name, fk_soc_id, cust_phone, fk_user_id) VALUES ('{cust_name}','{soc_id}','{cust_phn_no}','{user_id}');")
            cust_id = None
            try:
                conn = get_connection()
                result=conn.execute(add_cust_query)
                print(str(result)+ " insert cust details")
                cust_id = result.lastrowid
                print(str(cust_id)+" cust_id")
            except Exception as e:
                print(e)
                return redirect(url_for("addflat"))
            
            add_flat_query = text(f"INSERT INTO tbl_cust_flat (flat_no, fk_cust_id, fk_soc_id, fk_user_id) VALUES ('{cust_flat_no}','{cust_id}','{soc_id}','{user_id}');")
            try:
                conn = get_connection()
                conn.execute(add_flat_query)
            except Exception as e:
                print(e)
                return redirect(url_for("addflat"))
            return redirect(url_for("addflat"))
        
        #fetch society list
        soc_list_query = text(f"SELECT soc_name from tbl_society where fk_user_id = '{user_id}';")
        try:
            conn = get_connection()
            societies = [row[0] for row in conn.execute(soc_list_query).fetchall()]
            print(societies)
        except Exception as e:
            print(e)
            societies = []
        
        return render_template('add_flat.html',societies=societies,username = user)

    else:
        #flash('Please sign in to access the homepage', 'error')
        return redirect(url_for('sign_in'))

@app.route("/addsociety", methods = ['GET','POST'])
def addsociety():
    user = fetch_user_name()
    if 'user_id' in session:
        user_id = session['user_id']
        if request.method == 'POST':
            cust_soc_name = request.form['society']
            print(cust_soc_name)
            soc_id = None

            try:
                conn = get_connection()
                soc_query = text(f"SELECT pk_soc_id FROM tbl_society WHERE LOWER(soc_name) = LOWER('{cust_soc_name}') and fk_user_id = '{user_id}';")
                result = conn.execute(soc_query).fetchone()
                print(str(result)+" fetching soc_id")
                if result:
                    soc_id = list(result)[0]
                    flash("Society Name already exists.","error")
                    return redirect(url_for("addsociety"))
            except Exception as e:
                print(e)
                return redirect(url_for("addsociety"))

            if soc_id is None:
                # If the society doesn't exist, add a new entry in tbl_society
                try:
                    conn = get_connection()
                    add_soc_query = text(f"INSERT INTO tbl_society (soc_name,fk_user_id) VALUES ('{cust_soc_name}','{user_id}');")
                    result=conn.execute(add_soc_query)
                    print(str(result)+ " insert soc details")
                    soc_id = result.lastrowid
                    print(str(soc_id)+" soc_id")
                    flash("New society added.","success")
                    return redirect(url_for("addsociety"))
                except Exception as e:
                    print(e)
                    return redirect(url_for("addflat"))
        return render_template('add_society.html',username = user)
    else:
        #flash('Please sign in to access the homepage', 'error')
        return redirect(url_for('sign_in'))

@app.route("/collectorder",methods = ['GET','POST'])
def collectorder():
    user = fetch_user_name()
    if 'user_id' in session:
        user_id = session['user_id']
        #fetch society list
        soc_list_query = text(f"SELECT soc_name from tbl_society where fk_user_id = '{user_id}';")
        try:
            conn = get_connection()
            societies = [row[0] for row in conn.execute(soc_list_query).fetchall()]
            print(societies)
        except Exception as e:
            print(e)
            societies = []
        return render_template('collect_order.html',username = user,societies=societies)
    else:
        #flash('Please sign in to access the homepage', 'error')
        return redirect(url_for('sign_in'))



if __name__ == "__main__":
    app.run(debug=True)
