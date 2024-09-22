from flask import Flask,render_template,url_for
from flask import Flask,render_template,request,send_file
import requests
from bs4 import BeautifulSoup
from urllib.request import urlopen as uReq
import os

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

if __name__=="__main__":
    app.run(debug=True)