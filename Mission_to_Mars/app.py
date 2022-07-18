from flask import Flask, render_template, redirect
from flask_pymongo import PyMongo
import scrape_mars
import pymongo

app = Flask(__name__)

conn = 'mongodb://localhost:27017'
client = pymongo.MongoClient(conn)

mars_app=client.mars_app

article=client.mars_app.article
image=client.mars_app.image
facts=client.mars_app.facts
hemisphere=client.mars_app.hemisphere



@app.route("/")
def home():

    article_data = client.mars_app.article.find_one()
    try:
        temp_article1=article_data['title']
    except:
        temp_article1=""
    try:
        temp_article2=article_data['paragraph']
    except:
        temp_article2=""

    image_data = client.mars_app.image.find_one()
    try:
        temp_image=image_data['img_url']
    except:
        temp_image=""
    
    facts_data = client.mars_app.facts.find_one()
    try:
        temp_fact=facts_data['html']
    except:
        temp_fact=""

    hemisphere_data = client.mars_app.hemisphere.find({})
    temp_hemisphere=[]
    try:
        for row in hemisphere_data:
            temp_hemisphere.append({row['title']:row['img_url']})
    except:
        temp_hemisphere=""
    print("---------------------------------------------------------")

    return render_template("index.html",article_title=temp_article1,article_paragraph=temp_article2,image_url=temp_image,temp_fact=temp_fact,hemisphere_dict=temp_hemisphere)

@app.route("/scrape")
def scrape():

    article_collection=mars_app.article.find({})
    for row in article_collection:
        try:
            article.delete_one({"title":row['title']})
        except:
            print("nothing to delete")

    image_collection=mars_app.image.find({})
    for row in image_collection:
        image.delete_one({"img_url":row['img_url']})

    facts_collection=mars_app.facts.find({})
    for row in facts_collection:
        facts.delete_one({"html":row['html']})

    hemisphere_collection=mars_app.hemisphere.find({})
    for row in hemisphere_collection:
        hemisphere.delete_one({"title":row['title']})

    # Run the scrape function
    data = scrape_mars.scrape_mars()

    article.insert_one({'title':data[0],'paragraph':data[1]})
    image.insert_one({'img_url':data[2]})
    facts.insert_one({'html':data[3]})
    for row in data[4]:
        hemisphere.insert_one({'title':row['title'],'img_url':row['img_url']})

    # # Update the Mongo database using update and upsert=True
    # for a in MARS_HEMISPHERE_DICT:
    #     mongo.db.collection.insert_one({"title":a['title'],"img_url":a['img_url']})

    # Redirect back to home page



    return redirect("/")


if __name__ == "__main__":
    app.run(debug=True)
