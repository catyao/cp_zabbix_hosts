#-*-coding:utf-8-*-
import sys,  os
APP_HOME = sys.path[0]


class thefunction():
    def authwrite2file(theauth, huanjing="yum"):
        filename = APP_HOME + '/theauth.txt.' + huanjing
        try:
            with open(filename, 'w') as f:  # 如果filename不存在会自动创建， 'w'表示写数据，写之前会清空文件中的原有数据！
                f.write(theauth)
            themessage = ("写入[ %d ]成功" % filename)
        except:
            themessage = ("写入[ %d ]失败" % filename)
        return themessage



    def authread4file(huanjing="yum"):
        try:
            with open(APP_HOME + '/theauth.txt.'+huanjing, 'r') as f:
                file = f.read()
        except:
            file = ""
        return file

    # def genjpg(message, thefile):
    #     try:
    #         pygame.init()
    #         text = message
    #         font = pygame.font.Font(os.path.join("C:\\Windows\\fonts", "SIMYOU.TTF"), 18)
    #         font1 = pygame.font.Font(os.path.join("C:\\Windows\\fonts", "SIMYOU.TTF"), 18)
    #         rtext = font.render(text, True, (0, 0, 0), (255, 255, 255))
    #         rtext = font.render(text, True, (0, 0, 0), (255, 255, 255))
    #         pygame.image.save(rtext, thefile)
    #         return "ok"
    #     except Exception as e:
    #         return e

