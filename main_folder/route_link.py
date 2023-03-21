# import MySQLdb
# import jwt
# from flask_login import current_user
# from functools import wraps, reduce
# from flask import Flask, request, json, jsonify, make_response, Blueprint
#
# from main_folder import token_required
# # from main_folder.app import db
# from main_folder.database import db
# from main_folder.models import Names, Sizes, Colours, Basket, BlackJWTList
#
# route_links = Blueprint('route_links', __name__)
#
# JWT_SECRET = 'secret'
# JWT_ALGORITHM = 'HS256'
# JWT_EXP_DELTA_SECONDS = 200
#
# @route_links.route("/add_brand", methods=("POST", "GET"))
# def add_brand():
#     bran = request.headers.get("name")
#     cos = request.headers.get("cost")
#     desc = request.headers.get("des")
#     z_id = request.headers.get("size_id")
#     c_id = request.headers.get("colour_id")
# # Create goods
#     names = Names(name=bran, description=desc, prise=cos)
#     db.session.add_all([names])
#     db.session.commit()
# # do with models
#     sizes = Sizes.query.get(z_id)
#     names.nam.append(sizes)
#     db.session.commit()
#
#     colours = Colours.query.get(c_id)
#     names.nam_2.append(colours)
#     db.session.commit()
#
#     return "bam"
#
#
# @route_links.route("/add_colour", methods=("POST", "GET"))
# def add_colour():
#     col = request.headers.get("colour")
#     colours = Colours(colour=col)
#     db.session.add_all([colours])
#     db.session.commit()
#     return str(colours)
#
#
# @route_links.route("/add_size", methods=("POST", "GET"))
# def add_size():
#     siz = request.headers.get("size")
#     sizes = Sizes(size=siz)
#     db.session.add_all([sizes])
#     db.session.commit()
#     return str(sizes)
#
#
# @route_links.route("/del_brand", methods=["DELETE"])
# def del_from_names():
#     del_names_id = request.headers.get("del_names_id")
#     id_names = Names.query.get(del_names_id)
#     db.session.delete(id_names)
#     db.session.commit()
#     return "Done"
#
#
# @route_links.route("/del_colour", methods=["DELETE"])
# def del_from_colours():
#     del_colours_id = request.headers.get("del_colours_id")
#     id_colours = Colours.query.get(del_colours_id)
#     db.session.delete(id_colours)
#     db.session.commit()
#     return "Done"
#
#
# @route_links.route("/del_size", methods=["DELETE"])
# def del_from_sizes():
#     del_size_id = request.headers.get("del_sizes_id")
#     id_sizes = Sizes.query.get(del_size_id)
#     db.session.delete(id_sizes)
#     db.session.commit()
#     return "Done"
#
#
# @route_links.route("/update", methods=["PUT"])
# def update_brands():
#     update_name_id = request.headers.get("update_name_id")
#     if not update_name_id:
#         return "No name id"
#     update_name = request.headers.get("update_name")
#     update_description = request.headers.get("update_description")
#     update_prise = request.headers.get("update_prise")
#     update_name_shoes_id = request.headers.get("update_name_shoes_id")
#     update_size_shoes_id = request.headers.get("update_size_shoes_id")
#     update_colour_shoes_id = request.headers.get("update_colour_shoes_id")
#
#     user_z = Sizes.query.get(update_size_shoes_id)
#     user_c = Colours.query.get(update_colour_shoes_id)
#     user = Names.query.get(update_name_shoes_id)
#     if update_name:
#         user.name = update_name
#     if update_description:
#         user.description = update_description
#     if update_prise:
#         user.prise = update_prise
#     if user_z:
#         user.nam = [user_z]
#     if user_c:
#         user.nam_2 = [user_c]
#     db.session.commit()
#     return "Done"
#
#
# @route_links.route("/info_one", methods=["GET"])
# def info_one():
#     get_name_id = request.headers.get("get_name_id")
#     get_size_id = request.headers.get("get_size_id")
#     get_colour_id = request.headers.get("get_colour_id")
#
#     user = Names.query.get(get_name_id)
#     user_size = Sizes.query.get(get_size_id)
#     user_colour = Colours.query.get(get_colour_id)
#     user_dict = {"user_id": user.id,
#                  "user_name": user.name,
#                  "user_description": user.description,
#                  "user_prise": user.prise,
#                  "user_size": user_size.size,
#                  "user_colour": user_colour.colour}
#     return jsonify(str(user_dict))
#
#
# def db_con():
#     conn = MySQLdb.connect(host='127.0.0.1',
#                            user='root',
#                            passwd='admin',
#                            db='flask')
#     return conn
#
#
# @route_links.route("/info_all", methods=["GET"])
# def info_many():
#     filter_value = request.headers.get("filter_value")
#     filter_key = request.headers.get("filter_key")
#     sort_key = request.headers.get("sort_key")
#     sort_value = request.headers.get("sort_value")
#     less_or_more = request.headers.get('less_or_more')
#
#     c = db_con().cursor()
#
#     users = Names.query.all()
#     user_list = []
#
#     for user_id in users:
#         user = Names.query.get(user_id.id)
#         colour_id = "SELECT colours_id FROM choose_shoes_2 WHERE names_id = %s"
#         argum = user_id.id
#         c.execute(colour_id, [str(argum)])
#         find_id = c.fetchall()
#         size_id = "SELECT sizes_id FROM choose_shoes WHERE names_id = %s"
#         argums = user_id.id
#         c.execute(size_id, [argums])
#         find_size_id = c.fetchall()
#         if find_id and find_size_id:
#             user_colour = Colours.query.get(find_id)
#             user_size = Sizes.query.get(find_size_id)
#         else:
#             user_colour = None
#             user_size = None
#         user_dict = {"user_id": user.id,
#                      "user_name": user.name,
#                      "user_description": user.description,
#                      "user_prise": user.prise,
#                      "user_size_id": user_size.id if user_size else None,
#                      "user_size": user_size,
#                      "user_colour_id": user_colour.id if user_colour else None,
#                      "user_colour": str(user_colour)}
#         user_list.append(user_dict)
# # Filter goods
#     if filter_value and filter_key:
#         try:
#             values = [int(filter_value)]
#             filter_list = [d for d in user_list if d[filter_key] in values]
#             return jsonify(str(filter_list))
#         except:
#             values = [filter_value]
#             filter_list = [d for d in user_list if d[filter_key] in values]
#             return jsonify(str(filter_list))
# # Sort goods
#
#     elif sort_key and sort_value:
#         if less_or_more == "less":
#             sort_list = [d for d in user_list if d[sort_key] <= int(sort_value)]
#             return jsonify(str(sort_list))
#         elif less_or_more == "more":
#             sort_list = [d for d in user_list if d[sort_key] > int(sort_value)]
#             return jsonify(str(sort_list))
#     else:
#         return jsonify(str(user_list))
#
#
# @route_links.route("/add_to_basket")
# # @token_required
# def add_basket(current_user):
#
#     c = db_con().cursor()
#     id_shoes = request.headers.get("id_good")
#     num_record = request.headers.get("num_record")
#     stat = request.headers.get("status")
#
#     customer = current_user.id
#     shoes = Names.query.get(id_shoes)
#
#     colour_id = "SELECT colours_id FROM choose_shoes_2 WHERE names_id = %s"
#     argum = shoes.id
#     c.execute(colour_id, [str(argum)])
#     find_id = c.fetchall()
#     size_id = "SELECT sizes_id FROM choose_shoes WHERE names_id = %s"
#     argums = shoes.id
#     c.execute(size_id, [argums])
#     find_size_id = c.fetchall()
#     user_colour = Colours.query.get(find_id)
#     user_size = Sizes.query.get(find_size_id)
#     basket = Basket(id_record=num_record, id_good=shoes.id, id_colour_shoes=user_colour.id, id_size_shoes=user_size.id,
#                     status=stat, all_summ=shoes.prise, id_customer=customer)
#     db.session.add_all([basket])
#     db.session.commit()
#     return 'successfully'
#
#
# @route_links.route('/change_status')
# def status_change():
#     new_status = request.headers.get("new_status")
#     id_for_change = request.headers.get("id_for_change")
#     basket_status = Basket.query.get(id_for_change)
#     if new_status:
#         basket_status = Basket.query.get(id_for_change)
#         basket_status.status = new_status
#     else:
#         if basket_status.status == "in the basket":
#             del_obj = Basket.query.get(id_for_change)
#             db.session.delete(del_obj)
#             return "success delete "
#         else:
#             return "Your status don`t in the basket"
#
#     db.session.commit()
#     return new_status
