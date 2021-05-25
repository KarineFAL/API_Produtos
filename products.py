import pymysql
from app import app
from bd_prod import mysql
from flask import jsonify
from flask import flash, request,Response
from auth import BasicAuth

	
#Inclui um produto no banco
@app.route("/api/produtos", methods=["POST"])  
def add_product():
	try:
		_json=request.json
		_nome_produto=_json['nome_produto']
		_preco_produto=_json['preco_produto']
		_desc_produto=_json['desc_produto']
		_status=_json['status']

		
		if _nome_produto and _preco_produto and _desc_produto and _status and request.method=="POST":
			sqlQuery="INSERT INTO CATALOGO_PRODUTOS (nome_produto, preco_produto, desc_produto, status) VALUES (%s, %s, %s, %s);"
			bindData=(_nome_produto, _preco_produto, _desc_produto, _status)
			conn=mysql.connect()
			cursor=conn.cursor()
			cursor.execute(sqlQuery,bindData)
			conn.commit()
			response = jsonify('Produto cadastrado com sucesso!')
			response.status_code=200
			return response
		else:
			return  jsonify({"error":f"Erro"}),500
	except Exception as error:
		return jsonify({"error":f"{error}"}), 500
	finally:
		cursor.close()
		conn.close()
		
#Atualiza informações do produto
@app.route('/api/produtos/<int:id_produto>', methods=['PUT'])
def update_product(id_produto):
	try:

		conn = mysql.connect()
		cursor=conn.cursor()
		
		sqlQuery = "SELECT * FROM catalogo_produtos WHERE id_produto=%s"
		cursor.execute(sqlQuery,id_produto)
		select = cursor.fetchone()
		if not select:
			return Response('Produto não cadastrado', status=400)
		
		_json = request.json
		_id_produto = _json['id_produto']
		_nome_produto = _json['nome_produto']
		_preco_produto = _json['preco_produto']
		_desc_produto = _json['desc_produto']
		_status = _json['status']

		
	  

		if _nome_produto and _preco_produto and _desc_produto and _status and _id_produto and request.method == 'PUT':
			sqlQuery = "UPDATE catalogo_produtos SET nome_produto=%s, preco_produto=%s, desc_produto=%s, status=%s WHERE id_produto=%s"
			bindData = (_nome_produto, _preco_produto, _desc_produto, _status, _id_produto,)
			conn = mysql.connect()
			cursor = conn.cursor()
			cursor.execute(sqlQuery, bindData)
			conn.commit()
			response = jsonify('Produto atualizado com sucesso!')
			response.status_code = 200
			return response
		else:
			return  jsonify({"error":f"Erro"}),500	
	except Exception as error:
		return jsonify({"error":f"{error}"}), 500
	finally:
		cursor.close() 
		conn.close()

@app.route('/api/produtos')  #Consulta todas os registros do banco
def show_products():
	try:
		conn = mysql.connect()
		cursor = conn.cursor(pymysql.cursors.DictCursor)
		cursor.execute("SELECT * FROM catalogo_produtos")
		showRows = cursor.fetchall()
		response = jsonify(showRows)
		response.status_code = 200
		return response
	except Exception as error:
		return jsonify({"error":f"{error}"}), 500
	finally:
		cursor.close() 
		conn.close()

	


@app.route('/api/produtos/<int:id_produto>', methods=["GET"]) #Consulta um registro no banco
def show_product_id(id_produto): 
	try:
		conn = mysql.connect()
		cursor = conn.cursor(pymysql.cursors.DictCursor)
		cursor.execute("SELECT  id_produto,nome_produto,desc_produto,status,preco_produto FROM catalogo_produtos WHERE id_produto =%s", id_produto)
		view_Rows = cursor.fetchone()
		if not view_Rows:
			return Response('Produto não cadastrado.'), 404
		response = jsonify(view_Rows)
		
		response.status_code = 200
		return response  
	except Exception as error:
		return jsonify({"error":f"{error}"}), 500

	finally:
		cursor.close() 
		conn.close()


if __name__ == "__main__":
	app.run(debug=True,port=8000)