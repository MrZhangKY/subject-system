import pickle
import logging
import sys
USERINFOPATH = r'D:\python学习\python全栈\面向对象\选课系统\userinfo'
STUINFOPATH = r'D:\python学习\python全栈\面向对象\选课系统\studentInfo'
LOGPATH = r'D:\python学习\python全栈\面向对象\选课系统\operation.log'


class Course(object):
    def __init__(self, name, price, period):
        self.name = name
        self.price = price
        self.period = period


class Student(object):
    opt_list = [('查看课程', 'show_courses'), ('选择课程', 'choose_course'),
                ('查看以选择课程', 'show_selected'), ('退出', 'exit')]
    def __init__(self, name):
        self.name = name
        self.classes = []
    def show_courses(self):
        pass
    def choose_course(self):
        pass
    def show_selected(self):
        pass
    def exit(self):
        pass
    @staticmethod
    def create(ret, logger):
        with open(STUINFOPATH, 'rb') as f:
            while True:
                try:
                    stu = pickle.load(f)
                    if stu.name == ret[0]:
                        obj = stu
                        return obj
                except:
                    logger.error(f'学生{stu.name}查无此人信息，请检查{STUINFOPATH}')


class Manager(object):
    opt_list = [('创建课程', 'create_course'), ('创建学生', 'create_student'),
                ('查看课程', 'show_courses'), ('查看学生', 'show_students'),
                ('查看学生和已选课程', 'show_stu_course'), ('退出', 'exit')]
    def __init__(self, name, logger):
        self.name = name
        self.logger = logger
    def create_course(self):
        pass
    def create_student(self):
        user = input('usename: ')
        pwd = '123456'
        stu = Student(user)
        '''
        ？？？？？？？？？？？？？？？？？？？？？？？？？？？？？？？？？？？？？？？？？？？？？？？？？？？？？？？？？？？
        重复创建问题，遍历。。。。。。。
        '''
        with open(USERINFOPATH, mode='a', encoding='utf-8') as f:
            print(f'{user}|{pwd}|Student', file=f)
        with open(STUINFOPATH, mode='ab') as f:
            pickle.dump(stu, f)
        self.logger.info(f'管理员{self.name}创建学生{user}')

    def show_courses(self):
        pass
    def show_students(self):
        pass
    def show_stu_course(self):
        pass
    def exit(self):
        pass
    @classmethod
    def create(cls, ret, logger):
        return cls(ret[0], logger)


def login():
    '''
    None
    :return: 登陆成功，返回用户名和身份；否则，返回false
    '''
    username = input('username:')
    password = input('password:')
    with open(USERINFOPATH) as f:
        for line in f:
            user, pwd, ident = line.strip().split('|')
            if username == user and password == pwd:
                return username, ident
    return False


def initLog():
    fh = logging.FileHandler(filename=LOGPATH, mode='a', encoding='utf-8')
    ch = logging.StreamHandler()
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    fh.setFormatter(formatter)
    ch.setFormatter(formatter)
    logger = logging.getLogger()
    logger.setLevel(logging.DEBUG)
    logger.addHandler(fh)
    logger.addHandler(ch)
    return logger


if __name__ == '__main__':
    logger = initLog()
    ret = login()
    if ret:
        print(f'登录成功，{ret[0]}欢迎使用选课系统')
        cls = getattr(sys.modules['__main__'], ret[1])
        obj = cls.create(ret, logger)
        for i, opt in enumerate(cls.opt_list, 1):
            print(i, opt[0])
        num = int(input('您需要选择的操作：'))
        if hasattr(obj, cls.opt_list[num-1][1]):
            getattr(obj, cls.opt_list[num-1][1])()
    else:
        print('登陆失败')

