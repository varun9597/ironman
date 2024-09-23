from flask import Flask, render_template, request, redirect, url_for, session, flash, jsonify
from database import get_connection
from sqlalchemy import text
import os
import ast
from dotenv import load_dotenv, dotenv_values
from routes.auth_routes import auth_bp
from flask_cors import CORS
# from razorpay_utils import Razor

load_dotenv()

rzr_key = os.getenv('RZRPAY_API_ID')
rzr_secret = os.getenv('RZRPAY_API_SECRET')

razor_api = {'key':rzr_key,'secret':rzr_secret}
# razor = Razor(razor_api)

app = Flask(__name__)
app.secret_key = 'your_secret_key'  # Make sure to set a secure secret key
CORS(app)

app.register_blueprint(auth_bp)


#OLD CODE
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
                flash('Flat removed successfully', 'success')
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
                    add_rate_card_query = text(f"INSERT INTO tbl_rate_card(fk_item_id,fk_user_id,fk_soc_id) SELECT tbl_items.pk_item_id as fk_item_id, '{user_id}' as fk_user_id, '{soc_id}' as fk_soc_id FROM tbl_items WHERE fk_user_id = '{user_id}';")
                    conn.execute(add_rate_card_query)
                    flash("New society added and rate card created.","success")
                    return redirect(url_for("addsociety"))
                except Exception as e:
                    print(e)
                    return redirect(url_for("addflat"))
        return render_template('add_society.html',username = user)
    else:
        #flash('Please sign in to access the homepage', 'error')
        return redirect(url_for('sign_in'))

@app.route("/modifyratecard", methods = ['GET','POST'])
def modifyratecard():
    user = fetch_user_name()
    if 'user_id' in session:
        user_id = session['user_id']
        if request.method == 'POST':
            soc_name = request.form['society']
            data = request.form.to_dict()
            data.pop('society',None)
            print(data)
            try:
                conn = get_connection()
                for item_name, new_rate in data.items():
                    update_query = text(f"UPDATE tbl_rate_card SET rate = '{new_rate}', update_date = CURRENT_TIMESTAMP WHERE fk_user_id = '{user_id}' AND fk_soc_id = (SELECT pk_soc_id FROM tbl_society WHERE LOWER(soc_name) = LOWER('{soc_name}')) AND fk_item_id = (SELECT pk_item_id FROM tbl_items WHERE LOWER(item_name) = LOWER('{item_name}'));")
                    conn.execute(update_query)
                flash('Rate card updated successfully', 'success')
            except Exception as e:
                print(e)
                return redirect(url_for('modifyratecard'))
         #fetch society list
        soc_list_query = text(f"SELECT soc_name from tbl_society where fk_user_id = '{user_id}';")
        try:
            conn = get_connection()
            societies = [row[0] for row in conn.execute(soc_list_query).fetchall()]
            print(societies)
        except Exception as e:
            print(e)
            societies = []
        return render_template('mod_rate_card.html',username = user,societies=societies)
    else:
        #flash('Please sign in to access the homepage', 'error')
        return redirect(url_for('sign_in'))

@app.route('/get_item_list', methods = ['POST'])
def get_item_list():
    if 'user_id' in session:
        user_id = session['user_id']
        data = request.json
        society_name = data.get('society')
        #society_name = request.form.get('society')
        print(society_name)
        item_list = {}
        if society_name:
            try:
                conn = get_connection()
                item_query = text(f"SELECT items.item_name, rates.rate FROM tbl_rate_card rates \
                                  JOIN tbl_items items ON items.pk_item_id = rates.fk_item_id \
                                  JOIN tbl_society soc ON rates.fk_soc_id = soc.pk_soc_id \
                                  WHERE rates.fk_user_id = {user_id} AND LOWER(soc.soc_name) = LOWER('{society_name}') AND rates.rate > 0;")
                items = conn.execute(item_query).fetchall()
                item_list = {item[0]: str(item[1]) for item in items}
                print(item_list)
            except Exception as e:
                print(e)
                return redirect(url_for("modifyratecard"))
        #flat_list = ['Flat 101', 'Flat 102', 'Flat 103']
        item_list_json = jsonify(item_list)
        print(item_list_json)
        return jsonify(item_list)

@app.route('/get_item_list_rate_card', methods = ['POST'])
def get_item_list_rate_card():
    if 'user_id' in session:
        user_id = session['user_id']
        data = request.json
        society_name = data.get('society')
        #society_name = request.form.get('society')
        print(society_name)
        item_list = {}
        if society_name:
            try:
                conn = get_connection()
                item_query = text(f"SELECT items.item_name, rates.rate FROM tbl_rate_card rates JOIN tbl_items items ON items.pk_item_id = rates.fk_item_id JOIN tbl_society soc ON rates.fk_soc_id = soc.pk_soc_id WHERE rates.fk_user_id = {user_id} AND LOWER(soc.soc_name) = LOWER('{society_name}');")
                items = conn.execute(item_query).fetchall()
                item_list = {item[0]: str(item[1]) for item in items}
                print(item_list)
            except Exception as e:
                print(e)
                return redirect(url_for("modifyratecard"))
        #flat_list = ['Flat 101', 'Flat 102', 'Flat 103']
        item_list_json = jsonify(item_list)
        print(item_list_json)
        return jsonify(item_list)

@app.route("/collectorder",methods = ['GET','POST'])
def collectorder():
    user = fetch_user_name()
    if 'user_id' in session:
        user_id = session['user_id']
        if request.method == 'POST' :
            society = request.form['society']
            print(society)
            flatNumber = request.form['flatNumber']
            print(flatNumber)
            totalCount = request.form['totalCount']
            print(totalCount)
            totalAmount = request.form['totalAmount']
            print(totalAmount)
            itemDetails = request.form['itemDetails']
            print(itemDetails)
            # itemDetails_list = ast.literal_eval(itemDetails)
            # print(itemDetails_list)
            filtered_itemsDetails = [item for item in ast.literal_eval(itemDetails) if item['itemCount'] != 0]
            print(len(filtered_itemsDetails))
            if(len(filtered_itemsDetails) > 0):

                try:
                    conn = get_connection()
                    #creating order in tbl_orders
                    order_query = text(f"INSERT INTO tbl_orders(fk_cust_id, fk_user_id, total_amt) select cflat.fk_cust_id, {user_id} as fk_user_id, {totalAmount} as total_amt from tbl_cust_flat cflat join tbl_society soc on soc.pk_soc_id = cflat.fk_soc_id where LOWER(soc.soc_name) = LOWER('{society}') and LOWER(cflat.flat_no) = LOWER('{flatNumber}');")
                    result = conn.execute(order_query)
                    order_id = result.lastrowid
                    print(order_id)
                    #inserting item_order in tbl_order_items
                    for item in filtered_itemsDetails:
                        order_item_query = text(f"INSERT INTO tbl_order_items(fk_order_id, fk_item_id, quantity, price) SELECT {order_id} as fk_order_id, items.pk_item_id as fk_item_id, {item['itemCount']} as quantity, {item['itemTotal']} as price from tbl_items items where LOWER(items.item_name) = LOWER('{item['itemName']}') and items.fk_user_id = {user_id};")
                        conn.execute(order_item_query)
                    flash('Order Placed successfully', 'success')
                except Exception as e:
                    print(e)
                    return redirect(url_for('collectorder'))
            else:
                flash('Empty Order Cannot be placed', 'error')
            return redirect(url_for('collectorder'))
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

@app.route("/deleteorder", methods = ['GET','POST'])
def deleteorder():
    user = fetch_user_name()
    if 'user_id' in session:
        user_id = session['user_id']
        if request.method == 'POST' :
            data= request.json
            order_list = data.get('orderIds')
            print(order_list)
            try:
                conn = get_connection()
                delete_query = text("DELETE FROM tbl_orders WHERE pk_order_id IN (%s);" % ','.join("'%s'" % id for id in order_list))
                print(delete_query)
                conn.execute(delete_query)
            except Exception as e:
                print(e)
                return redirect(url_for('deleteorder'))
     #fetch society list
        soc_list_query = text(f"SELECT soc_name from tbl_society where fk_user_id = '{user_id}';")
        try:
            conn = get_connection()
            societies = [row[0] for row in conn.execute(soc_list_query).fetchall()]
            print(societies)
        except Exception as e:
            print(e)
            societies = []
        return render_template('delete_order.html',username = user,societies=societies)
    else:
        #flash('Please sign in to access the homepage', 'error')
        return redirect(url_for('sign_in'))

@app.route('/fetchorders',methods=['POST'])
def fetch_orders():
    if 'user_id' in session:
        user_id = session['user_id']
        data = request.json
        print("fetchorders")
        society = data.get('society')
        flatno = data.get('flatNumber')
        orders = []
        try:
            conn = get_connection()
            fetch_order_query = text(f"SELECT o.pk_order_id as order_id,DATE_FORMAT(o.order_date, '%d/%m/%Y') as order_date, GROUP_CONCAT(CONCAT(i.item_name, ' × ', oi.quantity) SEPARATOR ', ') AS items_ordered, o.total_amt, o.paid_amount, o.os_amount, o.bill_status FROM tbl_orders o JOIN tbl_order_items oi ON o.pk_order_id = oi.fk_order_id JOIN tbl_items i ON oi.fk_item_id = i.pk_item_id JOIN tbl_cust_flat tcf on tcf.fk_cust_id = o.fk_cust_id join tbl_society ts on tcf.fk_soc_id = ts.pk_soc_id where o.fk_user_id = '{user_id}' and LOWER(tcf.flat_no) = LOWER('{flatno}') and LOWER(ts.soc_name) = LOWER('{society}') and LOWER(bill_status) = 'not paid' GROUP BY o.pk_order_id ORDER BY o.order_date DESC LIMIT 10;")
            result = conn.execute(fetch_order_query).fetchall()
            orders = [{'order_id': row[0], 'order_date': row[1], 'items_ordered': row[2],'total_amount':float(row[3]),'paid_amount':float(row[4]),'os_amount':float(row[5]),'bill_status':row[6]} for row in result]
            print(orders)
        except Exception as e:
            print(e)
            return redirect(url_for('deleteorder'))

        return jsonify(orders)

@app.route("/additem", methods = ['GET','POST'])
def additem():
    user = fetch_user_name()
    if 'user_id' in session:
        user_id = session['user_id']
        if request.method == 'POST':
            item_name = request.form['item']
            print(item_name)
            item_id = None

            try:
                conn = get_connection()
                item_query = text(f"SELECT pk_item_id FROM tbl_items WHERE LOWER(item_name) = LOWER('{item_name}') and fk_user_id = '{user_id}';")
                result = conn.execute(item_query).fetchone()
                print(str(result)+" fetching item_id")
                if result:
                    item_id = list(result)[0]
                    flash("Item Name already exists.","error")
                    return redirect(url_for("additem"))
            except Exception as e:
                print(e)
                return redirect(url_for("additem"))

            if item_id is None:
                # If the society doesn't exist, add a new entry in tbl_society
                try:
                    conn = get_connection()
                    add_item_query = text(f"INSERT INTO tbl_items (item_name,fk_user_id) VALUES ('{item_name}','{user_id}');")
                    result=conn.execute(add_item_query)
                    print(str(result)+ " insert item details")
                    item_id = result.lastrowid
                    print(str(item_id)+" item_id")
                    soc_list_query = text(f"SELECT pk_soc_id from tbl_society where fk_user_id = '{user_id}';")
                    societies = [row[0] for row in conn.execute(soc_list_query).fetchall()]
                    for soc_id in societies:
                        add_rate_card_query = text(f"INSERT INTO tbl_rate_card(fk_item_id,fk_user_id,fk_soc_id) SELECT '{item_id}' as fk_item_id, '{user_id}' as fk_user_id, '{soc_id}' as fk_soc_id;")
                        conn.execute(add_rate_card_query)
                    flash("New Item added.","success")
                    return redirect(url_for("additem"))
                except Exception as e:
                    print(e)
                    return redirect(url_for("additem"))
        return render_template('add_item.html',username = user)
    else:
        #flash('Please sign in to access the homepage', 'error')
        return redirect(url_for('sign_in'))

@app.route('/viewsociety', methods = ['GET'])
def viewsociety():
    if 'user_id' in session:
        user_id = session['user_id']
        # data = request.json
        # society_name = data.get('society')
        # #society_name = request.form.get('society')
        # print(society_name)
        soc_list = []
        try:
            conn = get_connection()
            soc_query = text(f"SELECT soc_name from tbl_society where fk_user_id = {user_id};")
            societies = [row[0] for row in conn.execute(soc_query).fetchall()]
            print(societies)
            soc_list = societies
        except Exception as e:
            print(e)
            return redirect(url_for("addflat"))
        # flat_list = ['Flat 101', 'Flat 102', 'Flat 103']
        soc_list_json = jsonify({'soc': soc_list})
        print(soc_list_json)
        return jsonify(soc_list)
        # return render_template('view_societies.html', societies = jsonify(soc_list))
    return render_template('view_societies.html')

@app.route('/societies')
def societies_page():
    user = fetch_user_name()
    return render_template('view_societies.html', username = user)  # Render the HTML file

if __name__ == "__main__":
    app.run(debug=True)
