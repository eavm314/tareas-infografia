def get_line_1(x0, y0, x1, y1):
    dx = x1-x0
    dy = y1-y0

    pk = 2*dy-dx

    x = x0
    y = y0
    points = [(x,y)]
    while x<=x1:
        points.append((x,y))
        if pk<0:
            pk = pk + 2*dy
        else:
            y+=1
            pk = pk + 2*dy - 2*dx
        x+=1

    return points

def get_line(x0, y0, x1, y1):
    dx = x1-x0
    dy = y1-y0

    if abs(dx) > abs(dy):
        dm = abs(dx)
        dn = abs(dy)
        avx0 = avx1 = 0 if dx==0 else abs(dx)//dx
        avy0 = 0
        avy1 = 0 if dy==0 else abs(dy)//dy 
    else:
        dm = abs(dy)
        dn = abs(dx)
        avy0 = avy1 = 0 if dy==0 else abs(dy)//dy
        avx0 = 0
        avx1 = 0 if dx==0 else abs(dx)//dx 

    pk = 2*dn-dm
    xk = x0
    yk = y0
    points = []
    while not (xk==x1 and yk==y1):
        points.append((xk,yk))
        if pk<0:
            xk+=avx0
            yk+=avy0
            pk += 2*dn
        else:
            xk+=avx1
            yk+=avy1
            pk += 2*dn - 2*dm
    points.append((x1,y1))

    return points

if __name__ == "__main__":
    print(get_line(2, 2, 10, 5))