# Training-Material-Collector
AI Training Material Collector
## English
This is a website for collecting Large Language Model training material texts
Users can add prompts to the database by submitting input and output information
Administrators can log in to the Dashboard through the Login page to manage the content already in the database, or download txt documents generated in json format.
Since this is just a sudden idea, I have only made very simple functions and have not added a register page yet. If you want to register an administrator account, you can add it to the database through the flask shell

#### You can log in with the default username 
username:xiaoqi
password:xiaoqi666
#### You can also register a new administrator in the flask shell 
 from app import db, Admin

 #Create a new admin user
 admin_user = Admin(username='xiaoqi', password='xiaoqi666')

 #Adding a new user to the database
 db.session.add(admin_user)

 #Commit changes
 db.session.commit()

### The main function of this website is: when a person wants to train a large language model in a specific aspect, he needs to write a lot of prompt words and they are not comprehensive. However, he can call on more netizens through the Internet to jointly complete the creation of the prompt words

### This website only implements the most basic functions and is very simple. I hope it can be improved with everyone's help.
## Chinese
这是一个用来收集AI大语言模型训练素材文本的网站
网友可以通过提交input和output信息来向数据库中添加prompt
管理员可以通过Login页面登陆Dashboard来对已经在数据库中的内容进行管理，也可以下载按照json格式生成的txt文档
由于这只是一个突然的想法，所以只做了非常简单的功能，暂时还没有添加register页面。想要注册管理员账户可以通过flask shell添加到数据库

#### 你可以通过默认的用户名登陆 
username:xiaoqi
password:xiaoqi666
#### 你也可以在flask shell中注册新的管理员
 from app import db, Admin

 #创建一个新的 admin 用户
 admin_user = Admin(username='xiaoqi', password='xiaoqi666')

 #将新用户添加到数据库
 db.session.add(admin_user)

 #提交更改
 db.session.commit()

### 这个网站的主要功能是：当一个人想要训练某个特殊方面的Large Language Model的时候，需要写非常多的提示词而且不全面。但是他可以通过网络召集更多网友来共同完成这个提示词的创作
### 这个网站仅仅只实现了最基础的功能，非常简单。希望在大家的帮助下可以越来越完善
