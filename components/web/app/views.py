# import os
#
# from flask.views import MethodView
# from flask import request, jsonify
# from sqlalchemy import exc
#
# # from models import User, Advert, Token
# # from permissions import permission, ISAUTHENTICATED, ISOWNER
# from app import web, app
# #
# #
# # class UserView(web.View):
# #
# #     @permission(ISAUTHENTICATED)
# #     def get(self, user_id=None, **kwargs):
# #         if user_id:
# #             if kwargs['auth_user'].is_superuser:
# #                 user = User.query.get(user_id)
# #             else:
# #                 user = kwargs['auth_user']
# #             return web.json_response(user.serialize())
# #         else:
# #             if kwargs['auth_user'].is_superuser:
# #                 return jsonify([
# #                     user.serialize()
# #                     for user in User.query.all()
# #                 ])
# #             else:
# #                 return web.json_response({'message': 'please specify user'})
# #
# #     @permission(ISAUTHENTICATED)
# #     def post(self, **kwargs):
# #         if kwargs['auth_user'].is_superuser:
# #             user = User(**request.json)
# #             try:
# #                 user.save()
# #                 return jsonify(user.serialize())
# #             except exc.IntegrityError as err:
# #                 return jsonify({'message': 'wrong data'})
# #         else:
# #             return jsonify({'message': 'not enough permissions to create user'})
# #
# #
# # class AdvertView(web.View):
# #
# #     def get(self, advert_id=None):
# #         if advert_id:
# #             advert = Advert.query.get(advert_id)
# #             if advert:
# #                 return jsonify(advert.serialize())
# #             else:
# #                 return jsonify()
# #         return jsonify([
# #             adv.serialize()
# #             for adv in Advert.query.all()
# #         ])
# #
# #     @permission(ISAUTHENTICATED)
# #     def post(self, **kwargs):
# #         advert = Advert(**request.json)
# #         advert.owner = kwargs['auth_user'].id
# #         try:
# #             advert.save()
# #             return jsonify(advert.serialize())
# #         except exc.IntegrityError:
# #             return jsonify({'message': 'wrong data'})
# #
# #     @permission(ISAUTHENTICATED)
# #     @permission(ISOWNER, cls=Advert)
# #     def patch(self, advert_id, **kwargs):
# #         advert = Advert.query.get(advert_id)
# #         advert.update(**request.json)
# #         return jsonify(advert.serialize())
# #
# #     def delete(self, advert_id):
# #         auth_user = is_authenticated(request.headers.get('Authentication'))
# #         if auth_user:
# #             advert = Advert.query.get(advert_id)
# #             if advert.owner == auth_user.id:
# #                 advert.delete()
# #                 return jsonify()
# #             else:
# #                 return jsonify({'message': 'you can modify only your own Advert'})
# #         else:
# #             return jsonify({'message': 'you must be authorized'})
# # #
# #
# # @app.route('/authenticate/', methods=['POST',])
# # def athenticate():
# #     try:
# #         user = User.query.filter_by(username=request.json['username']).one()
# #     except exc.NoResultFound:
# #         return jsonify({
# #             'message': 'no user found'
# #         })
# #
# #     if user.authenticate(request.json['password']):
# #
# #         try:
# #             token = Token.query.filter_by(user=user.id).one()
# #         except exc.NoResultFound:
# #             token = Token(user=user.id)
# #             token.save()
# #         return jsonify({'token': 'Token ' + token.key})
# #     else:
# #         return jsonify({
# #             'message': 'wrong credentials'
# #         })
# #
# #
# # @app.route('/logout/', methods=['POST',])
# # def logout():
# #     token = request.headers.get('Authentication')
# #     token = token.split('Token ')[1]
# #     if token:
# #         try:
# #             token = Token.query.filter_by(key=token).one()
# #             token.delete()
# #             return jsonify()
# #         except exc.NoResultFound:
# #             return jsonify({
# #                 'message': 'wrong token provided'
# #             })
# #     else:
# #         return jsonify({
# #             'message': 'no token provided'
# #         })
#
#
# async def home():
#     name = os.getenv('name', 'Unknown')
#     return f'Hello {name}'
#
#
# # def is_authenticated(token):
# #     if token:
# #         token = token.split('Token ')[1]
# #         try:
# #             token = Token.query.filter_by(key=token).one()
# #             return User.query.get(token.user)
# #         except exc.NoResultFound:
# #             return False
# #     return False
#
# app.add_routes([
#
#     web.get('/', home)
# ])
# # app.add_url_rule('/users/<int:user_id>', view_func=UserView.as_view('users_get_unique'), methods=['GET',])
# # app.add_url_rule('/users', view_func=UserView.as_view('users_get_all'), methods=['GET',])
# # app.add_url_rule('/users/', view_func=UserView.as_view('users_create'), methods=['POST',])
# #
# # app.add_url_rule('/advert/<int:advert_id>', view_func=AdvertView.as_view('advert_get_unique'), methods=['GET',])
# # app.add_url_rule('/advert', view_func=AdvertView.as_view('advert_get_all'), methods=['GET',])
# # app.add_url_rule('/advert/', view_func=AdvertView.as_view('advert_create'), methods=['POST',])
# # app.add_url_rule('/advert/<int:advert_id>', view_func=AdvertView.as_view('advert_patch'), methods=['PATCH',])
# # app.add_url_rule('/advert/<int:advert_id>', view_func=AdvertView.as_view('advert_delete'), methods=['DELETE',])

from aiohttp.web import Response, json_response, View
from models import User, Token, Advert
from permissions import permission, ISAUTHENTICATED, ISOWNER
import os


async def home(request):
    name = os.getenv('name', 'Unknown')
    return Response(text=f'Hello {name}')


class UserView(View):

    @permission(ISAUTHENTICATED)
    async def get(self, **kwargs):
        user_id = int(self.request.match_info.get('user_id', 0))
        if user_id:
            if kwargs['auth_user'].is_superuser:
                user = await User.get(user_id)
                print(user)
                if not user:
                    return json_response({'message': 'wrong id'})
            else:
                user = kwargs['auth_user']
            return json_response(await user.serialize())
        else:
            if kwargs['auth_user'].is_superuser:
                return json_response([
                    await user.serialize()
                    for user in await User.query.gino.all()
                ])
            else:
                return json_response({'message': 'please specify user'})

    @permission(ISAUTHENTICATED)
    async def post(self, **kwargs):
        if kwargs['auth_user'].is_superuser:
            user_data = await self.request.json()
            user = User(**user_data)
            try:
                await user.create()
                return json_response(await user.serialize())
            except:
                return json_response({'message': 'wrong data'})
        else:
            return json_response({'message': 'not enough permissions to create user'})


class AdvertView(View):

    async def get(self):
        advert_id = int(self.request.match_info.get('advert_id', 0))
        if advert_id:
            advert = await Advert.get(advert_id)
            if advert:
                return json_response(await advert.serialize())
            else:
                return json_response({})
        return json_response([
            await adv.serialize()
            for adv in await Advert.query.gino.all()
        ])

    @permission(ISAUTHENTICATED)
    async def post(self, **kwargs):
        advert_data = await self.request.json()
        advert = Advert(**advert_data)
        advert.owner = kwargs['auth_user'].id
        try:
            await advert.create()
            return json_response(await advert.serialize())
        except:
            return json_response({'message': 'wrong data'})

    @permission(ISAUTHENTICATED)
    @permission(ISOWNER, cls=Advert)
    async def patch(self, **kwargs):
        try:
            advert_id = int(self.request.match_info.get('advert_id'))
        except:
            return json_response({'message': 'wrong id'})
        advert = await Advert.get(advert_id)
        advert_data = await self.request.json()
        await advert.update(**advert_data).apply()
        return json_response(await advert.serialize())

    async def delete(self):
        try:
            advert_id = int(self.request.match_info.get('advert_id'))
        except:
            return json_response({'message': 'wrong id'})
        auth_user = is_authenticated(self.request.headers.get('Authentication'))
        if auth_user:
            advert = await Advert.get(advert_id)
            if advert.owner == auth_user.id:
                await advert.delete()
                return json_response({})
            else:
                return json_response({'message': 'you can modify only your own Advert'})
        else:
            return json_response({'message': 'you must be authorized'})


async def athenticate(request):
    data = await request.json()
    try:
        user = await User.query.where(User.username == data['username']).gino.one()
    except:
        return json_response({
            'message': 'no user found'
        })

    if await user.authenticate(data['password']):

        try:
            token = await Token.query.where(Token.user == user.id).gino.one()
        except:
            token = Token(user=user.id)
            await token.create()
        return json_response({'token': 'Token ' + token.key})
    else:
        return json_response({
            'message': 'wrong credentials'
        })


async def logout(request):
    token = request.headers.get('Authentication')
    token = token.split('Token ')[1]
    if token:
        try:
            token = await Token.query.where(Token.key == token).gino.one()
            await token.delete()
            return json_response({'message': 'ok'})
        except:
            return json_response({
                'message': 'wrong token provided'
            })
    else:
        return json_response({
            'message': 'no token provided'
        })


async def is_authenticated(token):
    if token:
        token = token.split('Token ')[1]
        try:
            token = await Token.query.where(Token.key == token).gino.one()
            return await User.get(token.user)
        except:
            return False
    return False