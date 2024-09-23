from flask import Flask,render_template,url_for
from flask import Flask,render_template,request,send_file
import requests
from bs4 import BeautifulSoup
from urllib.request import urlopen as uReq
import os
import numpy
from joblib import dump,load
from sklearn.datasets import load_iris

app= Flask(__name__)

@app.route("/")
def home():
    return render_template("home.html")

@app.route("/webscrapping")
def web_scrapping():
    return render_template("web_scrapping.html")

@app.route("/search" , methods=["POST","GET"])
def search():
    query=request.form.get("q")
    response = requests.get(f'https://www.google.com/search?q={query}&sca_esv=589042230&rlz=1C1RXQR_enIN980IN980&hl=en&tbm=isch&sxsrf=AM9HkKmo6NX6a1rBVpBjYjoCDzB_pKAeuw:1702030309471&source=lnms&sa=X&ved=2ahUKEwj3s_j_zP-CAxUw-TgGHat9CiIQ_AUoAXoECAUQAw&biw=1242&bih=563&dpr=1.1')
    soup = BeautifulSoup(response.content,'html.parser')
    images_tages = soup.find_all('img')
    del images_tages[0]
    #return f"{images_tages}"
    for i in images_tages:
        images_url=i['src']
        return render_template("images_page.html",name1=images_tages ,image_name=query)
    

@app.route("/iris",methods=['GET'])
def iris():
    
    return render_template("iris_form.html")


@app.route('/predict',methods=['POST'])
def predict():
    model=load("knn1.joblib")
    if model is None:
        return render_template('iris_form.html', prediction="Model is not available.")

    try:
        # Retrieve and convert input values
        sepal_length = float(request.form['sepal_length'])
        sepal_width = float(request.form['sepal_width'])
        petal_length = float(request.form['petal_length'])
        petal_width = float(request.form['petal_width'])

        # Create input features
        input_features = [[sepal_length, sepal_width, petal_length, petal_width]]
        
        # Make prediction
        prediction = model.predict(input_features)
        iris=load_iris()

        flower_names = iris.target_names
        flower_prediction = flower_names[prediction[0]]

        return render_template('iris_form.html', prediction=flower_prediction)

    except ValueError:
        return render_template('iris_form.html', prediction="Invalid input values. Please enter numeric values.")
    except Exception as e:
        return render_template('iris_form.html', prediction=f"Error: {str(e)}")


if __name__=="__main__":
    app.run(debug=True)