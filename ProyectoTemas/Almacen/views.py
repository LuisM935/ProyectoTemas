from django.shortcuts import render, redirect
from django.apps import apps
import firebase_admin
from firebase_admin import credentials
from firebase_admin import db
from .forms import ProductForm

def connectDB():
    if not firebase_admin._apps:
        cred = credentials.Certificate("../venv/fbcredentials.json")
        firebase_admin.initialize_app(cred, {
            "databaseURL": "https://almacen-2fa0f-default-rtdb.firebaseio.com/" #Your database URL
        })
    dbconn = db.reference("products")
    return dbconn

def productlist(request):
    products = []
    dbconn = connectDB()
    tblproducts = dbconn.get()
    for key, value in tblproducts.items():
        products.append({"id": value["ID"], "name": value["product_name"], "price": value["price"]})
    return render(request, 'index.html', {'products':products})

def addproduct(request):
    if request.method == 'GET':
        return render(request, 'addproduct.html', {'product':{}})
    if request.method == 'POST':
        form = ProductForm(request.POST)
        if form.is_valid():
            id = form.cleaned_data.get("id")
            name = form.cleaned_data.get("product_name")
            price = form.cleaned_data.get("price")
            dbconn = connectDB()
            dbconn.push( { "ID": id, "product_name": name, "price": price })
        return redirect('index')
    
def updateproduct(request, id):
    pt = []
    dbconn = connectDB()
    tblproducts = dbconn.get()

    if request.method == 'GET':
        for key, value in tblproducts.items():
            if(value["ID"] == id):
                global updatekey
                updatekey = key
                pt.append({"id": value["ID"], "name": value["product_name"], "price": value["price"]})
        return render(request, 'editproduct.html', {'product':pt[0]})
    if request.method == 'POST':
        form = ProductForm(request.POST)
        if form.is_valid():
            name = str(form.cleaned_data.get("product_name"))
            price = float(form.cleaned_data.get("price"))
            updateitem = dbconn.child(updatekey)
            updateitem.update( {  "ID": id, "product_name": name, "price": price } )
        return redirect('index')
    

def deleteproduct(request, id):
    dbconn = connectDB()
    tblproducts = dbconn.get()
    for key, value in tblproducts.items():
        if(value["ID"] == id):
            deletekey = key
            break
    delitem = dbconn.child(deletekey)
    delitem.delete()
    return redirect('index')