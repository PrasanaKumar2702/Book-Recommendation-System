# Book-Recommendation-System

1. Setup Your Python Environment
First, ensure you have the necessary Python libraries installed. You can create a requirements.txt file for the project:

bash
Copy code
# requirements.txt
flask==2.0.2
pandas==1.4.2
numpy==1.22.3
scikit-learn==1.0.2
boto3==1.24.18
sqlalchemy==1.4.37
psycopg2-binary==2.9.3
2. AWS Configuration
Ensure that AWS is set up with S3, RDS, and EC2 instances, with necessary roles and policies for read/write access.

S3: Store your book dataset (CSV files).
RDS: Store your user-book ratings in a relational database like PostgreSQL.
EC2: Host your Flask app.
Ensure your EC2 instance has the appropriate IAM role for accessing S3 and RDS.

3. Code Structure
Folder Structure:

arduino
Copy code
book_recommender/
├── app.py
├── config.py
├── knn_model.py
├── requirements.txt
└── templates/
    └── index.html
4. config.py (AWS Configurations)
python
Copy code
import os

class Config:
    AWS_ACCESS_KEY = os.getenv('AWS_ACCESS_KEY')
    AWS_SECRET_KEY = os.getenv('AWS_SECRET_KEY')
    S3_BUCKET = os.getenv('S3_BUCKET_NAME')
    RDS_HOST = os.getenv('RDS_HOST')
    RDS_PORT = os.getenv('RDS_PORT', 5432)
    RDS_USER = os.getenv('RDS_USER')
    RDS_PASSWORD = os.getenv('RDS_PASSWORD')
    RDS_DB = os.getenv('RDS_DB')
5. knn_model.py (KNN Model)
python
Copy code
import pandas as pd
from sklearn.neighbors import NearestNeighbors
import boto3
import io

def load_data_from_s3(bucket_name, file_key, aws_access_key, aws_secret_key):
    # Connect to S3 and download dataset
    s3 = boto3.client('s3', aws_access_key_id=aws_access_key, aws_secret_access_key=aws_secret_key)
    obj = s3.get_object(Bucket=bucket_name, Key=file_key)
    df = pd.read_csv(io.BytesIO(obj['Body'].read()))
    return df

def train_knn_model(ratings_df):
    # Pivot the data into a user-item matrix
    book_matrix = ratings_df.pivot_table(index='user_id', columns='book_id', values='rating').fillna(0)
    
    # Use KNN with cosine similarity
    knn = NearestNeighbors(metric='cosine', algorithm='brute')
    knn.fit(book_matrix.values)
    
    return knn, book_matrix

def recommend_books(user_id, model, book_matrix, n_neighbors=5):
    distances, indices = model.kneighbors([book_matrix.loc[user_id].values], n_neighbors=n_neighbors+1)
    
    recommended_books = []
    for idx in indices[0][1:]:
        book_id = book_matrix.columns[idx]
        recommended_books.append(book_id)
        
    return recommended_books
6. app.py (Flask App)
python
Copy code
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
7. templates/index.html
html
Copy code
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Book Recommender</title>
</head>
<body>
    <h1>Book Recommendation System</h1>
    <form method="POST">
        <label for="user_id">Enter User ID:</label>
        <input type="text" name="user_id" id="user_id" required>
        <button type="submit">Get Recommendations</button>
    </form>
    
    {% if books %}
    <h2>Recommended Books:</h2>
    <ul>
        {% for book in books %}
        <li>{{ book['title'] }}</li>
        {% endfor %}
    </ul>
    {% endif %}
</body>
</html>
8. Deployment on EC2
Clone Your Project: Once you push this code to GitHub, you can clone it to your EC2 instance.

bash
Copy code
git clone https://github.com/your-username/book-recommender.git
cd book-recommender
Install Dependencies:

bash
Copy code
pip install -r requirements.txt
Set Environment Variables:

bash
Copy code
export AWS_ACCESS_KEY=your_aws_access_key
export AWS_SECRET_KEY=your_aws_secret_key
export S3_BUCKET_NAME=your_s3_bucket_name
export RDS_HOST=your_rds_host
export RDS_USER=your_rds_user
export RDS_PASSWORD=your_rds_password
export RDS_DB=your_rds_db
Run the Flask App:

bash
Copy code
python app.py
Access the Web Interface: You can access the Flask app via the public IP of your EC2 instance.

This is a basic working version of the book recommendation system with a KNN model, AWS integration, and a Flask web interface. You can modify the user interface, improve error handling, or even add more features (like filtering by genre, etc.) as needed.
