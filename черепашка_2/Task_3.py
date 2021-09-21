import turtle as trl

def draw_n(n, x, y, font, d, mrg, w):
    
    normal_width = trl.width()
    trl.width(w)
    
    stack = str(n)
    x_i = x
    
    for i in stack:
        f_i=font[i];

        trl.penup()
        trl.goto(x_i+f_i[0][0]*d, y+f_i[0][1]*d);

        trl.pendown()
        for com in f_i[1:]:
            trl.goto(x_i+com[0]*d, y+com[1]*d);
        
        x_i += d + mrg
        
    trl.width(normal_width)
        
def init():

    font={}
    curr_key='';
    
    with open('font.txt', 'r') as font_file:
        for line in font_file.readlines():

            line= line.rstrip()
            
            if line[-1] == ':':
                curr_key = line[0]
                font[curr_key] = []
            else:
                line = tuple(int(i) for i in line.split(' '))                
                font[curr_key].append(line);
    return font
        

trl.shape('turtle')
trl.speed(5)

font = init()

draw_n(123456789, x=-100, y=100, font=font, d=20, mrg=5,  w=3)


input()
