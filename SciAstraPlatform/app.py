from flask import Flask, render_template, request, redirect, url_for
from datetime import datetime
import mysql.connector

app = Flask(__name__)

# Database connection setup (MySQL)
def get_db_connection():
    conn = mysql.connector.connect(
        host='localhost',  # Your MySQL server
        user='root',  # Your MySQL username
        password=' ',#put your password here,  # Your MySQL password
        database='scia_platform'  # Your database name
    )
    return conn

@app.route('/')
def index():
    return render_template('index.html')

# Blog Routes
@app.route('/blogs')
def blogs():
    try:
        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)
        cursor.execute('SELECT * FROM blogs ORDER BY published_at DESC')
        blogs = cursor.fetchall()
        cursor.close()
        conn.close()

        # Format the 'published_at' date before passing it to the template
        for blog in blogs:
            blog['formatted_date'] = blog['published_at'].strftime('%B %d, %Y %H:%M')

        return render_template('blogs.html', blogs=blogs)
    except mysql.connector.Error as err:
        print(f"Error: {err}")
        return render_template('error.html', error_message="Error fetching blogs.")

# Route to view a single blog post
@app.route('/view_blog/<int:blog_id>')
def view_blog(blog_id):
    try:
        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)
        cursor.execute('SELECT * FROM blogs WHERE id = %s', (blog_id,))
        blog = cursor.fetchone()
        cursor.close()
        conn.close()
        if blog is None:
            return render_template('404.html')  # Handle blog not found
        return render_template('view_blog.html', blog=blog)
    except mysql.connector.Error as err:
        print(f"Error: {err}")
        return render_template('error.html', error_message="Error fetching blog details.")

# Route to add a new blog (GET for form display, POST for form submission)
@app.route('/add_blog', methods=['GET', 'POST'])
def add_blog():
    if request.method == 'POST':
        try:
            title = request.form['title']
            content = request.form['content']
            publish_date = datetime.strptime(request.form['publish_date'], '%Y-%m-%dT%H:%M')

            conn = get_db_connection()
            cursor = conn.cursor()
            cursor.execute('INSERT INTO blogs (title, content, published_at) VALUES (%s, %s, %s)', 
                           (title, content, publish_date))
            conn.commit()
            cursor.close()
            conn.close()

            return redirect(url_for('blogs'))
        except mysql.connector.Error as err:
            print(f"Error: {err}")
            return render_template('error.html', error_message="Error adding blog.")
    else:
        return render_template('add_blog.html')  # Display form to add a blog

# Course Routes
@app.route('/courses')
def courses():
    try:
        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)
        cursor.execute('SELECT * FROM courses')
        courses = cursor.fetchall()
        cursor.close()
        conn.close()
        return render_template('courses.html', courses=courses)
    except mysql.connector.Error as err:
        print(f"Error: {err}")
        return render_template('error.html', error_message="Error fetching courses.")

@app.route('/course/<int:course_id>')
def course(course_id):
    try:
        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)
        cursor.execute('SELECT * FROM courses WHERE id = %s', (course_id,))
        course = cursor.fetchone()
        cursor.close()
        conn.close()
        if course is None:
            return render_template('404.html')  # Handle course not found
        return render_template('course.html', course=course)
    except mysql.connector.Error as err:
        print(f"Error: {err}")
        return render_template('error.html', error_message="Error fetching course details.")

# Payment Routes
@app.route('/payment/<int:course_id>')
def payment(course_id):
    try:
        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)
        cursor.execute('SELECT * FROM courses WHERE id = %s', (course_id,))
        course = cursor.fetchone()
        cursor.close()
        conn.close()
        if course is None:
            return render_template('404.html')  # Handle course not found
        return render_template('payment.html', course=course)
    except mysql.connector.Error as err:
        print(f"Error: {err}")
        return render_template('error.html', error_message="Error fetching course details for payment.")

@app.route('/verify_payment', methods=['POST'])
def verify_payment():
    card_number = request.form['card_number']
    cvv = request.form['cvv']
    
    # Simulate payment verification logic
    if len(card_number) == 16 and len(cvv) == 3:
        return "Payment Successful! Thank you for your purchase."
    else:
        return "Payment Failed! Please try again."

if __name__ == '__main__':
    app.run(debug=True)
