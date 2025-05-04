from flask import Flask, render_template


app = Flask(__name__)

def get_product_by_id(product_id):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT id, name, description, price, image_url FROM products WHERE id = %s", (product_id,))
    product = cursor.fetchone()
    cursor.close()
    conn.close()
    return product
    

@app.route('/product/<int:product_id>')
def product_detail(product_id):
    product = get_product_by_id(product_id)
    if product:
      return render_template('productdetail.html', product={
        'id': product[0],
        'name': product[1],
        'description': product[2],
        'price': product[3],
        'image_url': product[4],
            
     })
    else: 
        return "<h1>Product not found<h1/>", 404


if __name__ == '__main__':
    app.run(debug=True)