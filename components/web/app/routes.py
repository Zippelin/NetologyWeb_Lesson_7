from views import home, UserView, athenticate, logout,AdvertView


def setup_router(app):
    app.router.add_get('/', home)
    app.router.add_get('/users', UserView)
    app.router.add_get('/users/{user_id:\d+}', UserView)
    app.router.add_post('/users', UserView)
    app.router.add_post('/authenticate', athenticate)
    app.router.add_post('/logout', logout)
    app.router.add_get('/advert', AdvertView)
    app.router.add_get('/advert/{advert_id:\d+}', AdvertView)
    app.router.add_patch('/advert/{advert_id:\d+}', AdvertView)
    app.router.add_delete('/advert/{advert_id:\d+}', AdvertView)
    app.router.add_post('/advert', AdvertView)