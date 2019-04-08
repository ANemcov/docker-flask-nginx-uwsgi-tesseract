from flask_wtf import FlaskForm
from wtforms import TextField, BooleanField
from wtforms.validators import Required
from flask_wtf.file import FileField, FileRequired, FileAllowed
from flask_uploads import UploadSet, IMAGES

images = UploadSet('images', IMAGES)
    
class LoginForm(FlaskForm):
    openid = TextField('openid', validators = [Required()])
    remember_me = BooleanField('remember_me', default = False)

class UploadForm(FlaskForm):
    
    imagefile = FileField(validators=[FileRequired(),
                                        FileAllowed(images, 'Images only!')
                                    ])
