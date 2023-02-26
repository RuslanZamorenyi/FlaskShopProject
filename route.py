# import app
#
#
# @app.route("/collect/<string:command>", methods=("POST", "GET"))
# def brands(command):
#     if command == "brand":
#         bran = request.headers.get("name")
#         cos = request.headers.get("cost")
#         desc = request.headers.get("des")
#         if bran and cos and desc:
#             new_brand = Names(
#                 name=bran,
#                 prise=cos,
#                 description=desc
#             )
#             db.session.add(new_brand)
#             db.session.commit()
#     elif command == "size":
#         siz = request.headers.get("size")
#         if siz:
#             new_size = Sizes(
#                 size=siz
#             )
#             db.session.add(new_size)
#             db.session.commit()
#     elif command == "colour":
#         col = request.headers.get("colour")
#         if col:
#             new_colour = Colours(
#                 colour=col
#             )
#             db.session.add(new_colour)
#             db.session.commit()
#     return "was add"
