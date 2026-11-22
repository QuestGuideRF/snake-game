import random
import time
import os
import sys
class SnakeGame :
    def __init__ (self ,width =25 ,height =15 ):
        self .width =width
        self .height =height
        self .snake =[(width //2 ,height //2 )]
        self .direction ='RIGHT'
        self .food =self .generate_food ()
        self .score =0
        self .game_over =False
        self .speed =0.15
    def generate_food (self ):
        while True :
            food_x =random .randint (1 ,self .width -2 )
            food_y =random .randint (1 ,self .height -2 )
            food =(food_x ,food_y )
            if food not in self .snake :
                return food
    def clear_screen (self ):
        os .system ('cls'if os .name =='nt'else 'clear')
    def draw_board (self ):
        board =[]
        for y in range (self .height ):
            row =[]
            for x in range (self .width ):
                if x ==0 or x ==self .width -1 or y ==0 or y ==self .height -1 :
                    row .append ('█')
                else :
                    row .append (' ')
            board .append (row )
        food_x ,food_y =self .food
        board [food_y ][food_x ]='🍎'
        for i ,(x ,y )in enumerate (self .snake ):
            if i ==0 :
                if self .direction =='UP':
                    board [y ][x ]='▲'
                elif self .direction =='DOWN':
                    board [y ][x ]='▼'
                elif self .direction =='LEFT':
                    board [y ][x ]='◄'
                else :
                    board [y ][x ]='►'
            else :
                board [y ][x ]='●'
        self .clear_screen ()
        print ('🐍 ЗМЕЙКА')
        print ()
        for row in board :
            print (''.join (row ))
        print ()
        print (f'Счёт: {self .score }')
        print (f'Длина змейки: {len (self .snake )}')
        print ()
        print ('Управление: W-вверх, S-вниз, A-влево, D-вправо')
        print ('Для выхода нажмите Q')
    def get_input (self ):
        try :
            if os .name =='nt':
                import msvcrt
                if msvcrt .kbhit ():
                    key =msvcrt .getch ().decode ('utf-8').lower ()
                    return key
            else :
                import select
                import tty
                import termios
                old_settings =termios .tcgetattr (sys .stdin )
                try :
                    tty .setraw (sys .stdin .fileno ())
                    if select .select ([sys .stdin ],[],[],0.1 )[0 ]:
                        key =sys .stdin .read (1 ).lower ()
                        return key
                finally :
                    termios .tcsetattr (sys .stdin ,termios .TCSADRAIN ,old_settings )
        except :
            pass
        return None
    def update_direction (self ,key ):
        if key =='w'and self .direction !='DOWN':
            self .direction ='UP'
        elif key =='s'and self .direction !='UP':
            self .direction ='DOWN'
        elif key =='a'and self .direction !='RIGHT':
            self .direction ='LEFT'
        elif key =='d'and self .direction !='LEFT':
            self .direction ='RIGHT'
        elif key =='q':
            self .game_over =True
    def move_snake (self ):
        head_x ,head_y =self .snake [0 ]
        if self .direction =='UP':
            new_head =(head_x ,head_y -1 )
        elif self .direction =='DOWN':
            new_head =(head_x ,head_y +1 )
        elif self .direction =='LEFT':
            new_head =(head_x -1 ,head_y )
        else :
            new_head =(head_x +1 ,head_y )
        if (new_head [0 ]<=0 or new_head [0 ]>=self .width -1 or
        new_head [1 ]<=0 or new_head [1 ]>=self .height -1 ):
            self .game_over =True
            return
        if new_head in self .snake :
            self .game_over =True
            return
        self .snake .insert (0 ,new_head )
        if new_head ==self .food :
            self .score +=10
            self .food =self .generate_food ()
            if self .speed >0.05 :
                self .speed -=0.005
        else :
            self .snake .pop ()
    def show_game_over (self ):
        self .clear_screen ()
        print ()
        print ('╔══════════════════════════════════════╗')
        print ('║            🎮 ИГРА ОКОНЧЕНА!         ║')
        print ('╠══════════════════════════════════════╣')
        print (f'║  💯 Ваш счёт: {self .score :<20} ║')
        print (f'║  🐍 Длина змейки: {len (self .snake ):<14} ║')
        print ('╠══════════════════════════════════════╣')
        if self .score <50 :
            level ="Новичок 🥉"
        elif self .score <150 :
            level ="Любитель 🥈"
        elif self .score <300 :
            level ="Эксперт 🥇"
        else :
            level ="Мастер 👑"
        print (f'║  🏆 Уровень: {level :<19} ║')
        print ('╚══════════════════════════════════════╝')
        print ()
        print ('Нажмите Enter для выхода...')
        input ()
    def show_welcome (self ):
        self .clear_screen ()
        print ()
        print ('╔══════════════════════════════════════╗')
        print ('║         🐍 ДОБРО ПОЖАЛОВАТЬ!        ║')
        print ('║            В ИГРУ ЗМЕЙКА             ║')
        print ('╠══════════════════════════════════════╣')
        print ('║                                      ║')
        print ('║  🎯 ПРАВИЛА:                        ║')
        print ('║  • Собирайте яблоки 🍎              ║')
        print ('║  • Избегайте стен и себя             ║')
        print ('║  • Змейка растёт с каждым яблоком    ║')
        print ('║                                      ║')
        print ('║  🎮 УПРАВЛЕНИЕ:                     ║')
        print ('║  • W - вверх                         ║')
        print ('║  • S - вниз                          ║')
        print ('║  • A - влево                         ║')
        print ('║  • D - вправо                        ║')
        print ('║  • Q - выход                         ║')
        print ('║                                      ║')
        print ('╚══════════════════════════════════════╝')
        print ()
        print ('Нажмите Enter для начала игры...')
        input ()
    def run (self ):
        self .show_welcome ()
        if os .name !='nt':
            import termios
            import tty
            old_settings =termios .tcgetattr (sys .stdin )
        try :
            while not self .game_over :
                self .draw_board ()
                key =self .get_input ()
                if key :
                    self .update_direction (key )
                self .move_snake ()
                time .sleep (self .speed )
            self .show_game_over ()
        except KeyboardInterrupt :
            print ("\n\n👋 До свидания!")
        finally :
            if os .name !='nt':
                termios .tcsetattr (sys .stdin ,termios .TCSADRAIN ,old_settings )
def main ():
    try :
        game =SnakeGame ()
        game .run ()
    except Exception as e :
        print (f"❌ Ошибка: {e }")
        print ("Убедитесь, что ваш терминал поддерживает необходимые функции")
if __name__ =="__main__":
    main ()