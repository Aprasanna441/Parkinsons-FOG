from flask import Blueprint
from controllers.UserController import signup,login,login_signup,home,dashboard,logout


router = Blueprint('routes', __name__)

router.route('/home',methods=['GET'])(home)


router.route('/auth', methods=['GET'])(login_signup)
router.route('/signup',methods=['POST'])(signup)
router.route('/login',methods=['POST',"GET"])(login)
router.route('/dashboard',methods=['GET'])(dashboard)
router.route('/logout',methods=['GET'])(logout)

