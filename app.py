from flask import Flask, render_template, request
from config import Config
from knn_model import load_data_from_s3, train_knn_model, recommend_books
import psycopg2
import pandas as pd

app = Flask(__name__)
app.config.from_object(Config)

# Load data from S3
df_ratings = load_data_from_s3(Config.S3_BUCKET, 'ratings.csv', Config.AWS_ACCESS_KEY, Config.AWS_SECRET_KEY)

# Train the KNN model
knn_model, book_matrix = train_knn_model(df_ratings)

# Connect to RDS to fetch book details
def get_book_details(book_ids):
    conn = psycopg2.connect(
        host=Config.RDS_HOST,
        port=Config.RDS_PORT,
        user=Config.RDS_USER,
        password=Config.RDS_PASSWORD,
        dbname=Config.RDS_DB
    )
    query = f"SELECT book_id, title FROM books WHERE book_id IN ({', '.join(map(str, book_ids))})"
    df_books = pd.read_sql_query(query, conn)
    conn.close()
    return df_books

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        user_id = int(request.form['user_id'])
        
        # Get recommendations
        recommended_books = recommend_books(user_id, knn_model, book_matrix)
        
        # Fetch book details from RDS
        book_details = get_book_details(recommended_books)
        
        return render_template('index.html', books=book_details)
    
    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True)
