from flask import Blueprint, render_template, request, redirect, url_for, flash, jsonify
from flask_login import login_required, login_user, logout_user, current_user
import psycopg2
import base64



# Initialize Blueprint
blueprint = Blueprint('blueprint', __name__, template_folder='templates')

# Route for the home page (index)
@blueprint.route('/index')
@login_required
def index():
    return render_template('home/index.html', segment='index')


# Route for notifications
@blueprint.route('/api/notifications', methods=['GET'])
@login_required
def get_notifications():
    try:
        # Database connection
        conn = psycopg2.connect(
            dbname='pest_db',
            user='pest_db_user',
            password='ic2ssRtlfJNayDEtbKkMhrvi6l4IyNJ8',
            host='dpg-cqjkj2mehbks73cd0r30-a.oregon-postgres.render.com',
            port='5432'
        )
        cur = conn.cursor()

        # Query to fetch data
        cur.execute("SELECT disease, recommendation, image FROM disease_data ORDER BY detection_date DESC")
        rows = cur.fetchall()

        # Close the connection
        cur.close()
        conn.close()

        # Process the data into JSON format
        alerts = [
            {
                'disease': row[0],
                'recommendation': row[1],
                'image': base64.b64encode(row[2]).decode('utf-8') if row[2] else None
            }
            for row in rows
        ]

        # Return the data as JSON
        return jsonify(alerts=alerts)

    except Exception as e:
        print(f"Error fetching data: {e}")
        return jsonify(alerts=[]), 500  # Return an empty list and a 500 status code in case of error




# Route for login page
@blueprint.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user = user.authenticate(username, password)  # Replace with your user authentication logic
        if user:
            login_user(user)
            return redirect(url_for('blueprint.notifications'))
        else:
            flash('Invalid username or password', 'danger')
    return render_template('login.html')

# Route for logout
@blueprint.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('blueprint.index'))

# Catch-all route for custom templates
@blueprint.route('/<template>', methods=['GET'])
@login_required
def route_template(template):
    try:
        if not template.endswith('.html'):
            template += '.html'

        # Detect the current page
        segment = get_segment(request)

        # Serve the file (if exists) from app/templates/home/FILE.html
        return render_template("home/" + template, segment=segment)

    except TemplateNotFound:
        return render_template('home/page-404.html'), 404

    except Exception as e:
        print(f"Error loading template: {e}")
        return render_template('home/page-500.html'), 500

# Helper - Extract current page name from request
def get_segment(request):
    try:
        segment = request.path.split('/')[-1]
        if segment == '':
            segment = 'index'
        return segment
    except Exception as e:
        print(f"Error extracting segment: {e}")
        return None