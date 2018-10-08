from flask import Flask, jsonify, render_template
import pymongo
import scrape_mars


# Flask set-up

app = Flask(__name__)

@app.route("/scrape")
def scrape():
    # Import scrapted dictionary data from scrape_mars.py
    post = scrape_mars.scrape()

   # https://docs.mongodb.com/manual/reference/default-mongodb-port/
    conn = 'mongodb://localhost:27017'
    client = pymongo.MongoClient(conn)

    # Declare the database
    db = client.mars_db

    # Declare the collection
    collection = db.mars_data

    # Drops collection if available to remove duplicates
    collection.drop()

    # Insert the document into the database
    collection.insert_one(post)

    return ('Data uploaded.')



@app.route("/")
def showdata():

    conn = 'mongodb://localhost:27017'
    client = pymongo.MongoClient(conn)
    db = client.mars_db
    collection = db.mars_data

    results = list(collection.find())
    result = results[0]
    
    # Return the template with the teams list passed in
    return render_template('index.html', dict= result)

if __name__ == '__main__':
    app.run(debug=True)
