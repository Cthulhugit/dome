import math


def calc_length(d=10430,
                num_of_belts=3,
                k=2.4,
                sup_beam_length=400):
    xcoordinates = dict()
    ycoordinates = dict()
    zcoordinates = dict()
    lengths = dict()    # Длины балок
    literal = tuple('0abcdefghijklmnopqrstuvwxyz')[0:num_of_belts+1]
    quantity = {literal[i]: i + 1 for i in range(1, num_of_belts)}  # Количество типоразмеров по поясам
    quantity[literal[-1]] = 2

    f = ('РВС-' + str(d) + ' k=' + str(k) + '.txt')
    """Основные вычисления"""

    num_of_beams = {str(i): i * 6 for i in range(1, num_of_belts)}  # Количество балок по поясам
    num_of_beams[str(num_of_belts)] = num_of_beams[str(num_of_belts - 1)]
    knot_angles = [0]  # Углы поворота узлов (вершин)
    for i in range(1, num_of_belts):
        knot_angles.append(360 / num_of_beams.get(str(i)))
    offset_angle = knot_angles[-1] / 2  # Угол смещения вершин последнего пояса
    num_of_sup_beams = (num_of_belts - 1) * 6  # Количество опорных балок = Количество балок стягивающего пояса
    r1 = d / 2  # Радиус резервуара
    r2 = k * d  # Радиус кривизны купола
    h = r2 - math.sqrt((r2 ** 2) - (r1 ** 2))  # Высота купола
    xcoordinates['0'] = 0
    ycoordinates['0'] = 0
    zcoordinates['0'] = h

    def xcord(r, fi):  # Координаты 'x'
        return r * math.cos(math.radians(fi))

    def ycord(r, fi):  # Координаты 'y'
        return r * math.sin(math.radians(fi))

    def length(x1, y1, z1, x2, y2, z2):
        return round(math.sqrt((x2-x1)**2 + (y2-y1)**2 + (z2-z1)**2), 10)

    angle_rad = math.acos((((r2 ** 2) * 2) - (d ** 2)) / (2 * r2 ** 2))  # Угол купола (в радианах)
    angle_grad = math.degrees(angle_rad)  # Угол купола (в градусах)
    support_beam_arc_angle_grad = math.degrees(2 * math.asin(sup_beam_length / (2 * r2)))  # Угол дуги опорной балки
    angle_grad_without_support_beam = angle_grad - (
        support_beam_arc_angle_grad * 2)  # Угол купола (в градусах) без опорной балки
    angle_rad_without_support_beam = math.radians(
        angle_grad_without_support_beam)  # Угол купола (в радианах) без опорной балки
    d_last = 2 * r2 * math.sin(angle_rad_without_support_beam / 2)  # Диаметр стягивающего пояса
    tightening_belt_beams_length = d_last * math.sin(
        (math.radians(360 / num_of_sup_beams)) / 2)  # Длина балок стягивающего пояса
    d_last_center = math.sqrt((d_last / 2) ** 2 - (
            tightening_belt_beams_length / 2) ** 2) * 2  # Диаметр центров балок стягивающего пояса
    r_last_center = d_last_center / 2

    """Первоначальные размеры"""
    angle_belt_grad = angle_grad_without_support_beam / 2 / num_of_belts  # Угол половины пояса (градусы)
    angle_belts_rad = {str(i): math.radians(i * 2 * angle_belt_grad) for i in
                       range(1, num_of_belts + 1)}  # Углы поясов (в радианах)
    d_belts = {str(i): 2 * r2 * math.sin(angle_belts_rad.get(str(i)) / 2) for i in
               range(1, num_of_belts + 1)}  # Диаметры поясов
    r_belts = {str(i): d_belts.get(str(i)) / 2 for i in
               range(1, num_of_belts + 1)}  # Радиусы поясов
    belts_heigth = {str(i): h - (r2 - math.sqrt(r2 ** 2 - r_belts.get(str(i)) ** 2)) for i
                    in range(1, num_of_belts + 1)}  # Высоты поясов

    def leg(r, h1, h2, c=r_last_center):  # Катет
        return math.sqrt((c - r) ** 2 + (h1 - h2) ** 2)
    leg1 = leg(r_belts.get(str(num_of_belts - 1)),
               belts_heigth.get(str(num_of_belts)),
               belts_heigth.get(str(num_of_belts - 1)))
    last_belt_beams_length = math.sqrt((tightening_belt_beams_length / 2) ** 2 + leg1 ** 2)  # Длина балки нижнего пояса
    first_beam_length = 2 * r2 * math.sin(math.radians(angle_belt_grad / 2))    # Длина первой радиальной балки

    # print('Диаметр резервуара', d)
    # print('Коэффициент кривизны', k)
    # print('Длина опорной балки', sup_beam_length)
    # print('Количество поясов', num_of_belts)
    # print('Радиус кривизны купола', r2)
    # print('Высота купола', h)
    # print('Угол купола', angle_grad)
    # print('Длина дуги купола', arc_length)
    # print('Угол дуги опорной балки', support_beam_arc_angle_grad)
    # print('Длина дуги опорной балки', support_beam_arc_length)
    # print('Длина дуги купола без опорной балки', dome_arc_length_without_support_beam)
    # print('Угол купола без опорной балки', angle_grad_without_support_beam)
    # print('Диаметр стягивающего пояса', d_last)
    # print('Длина балок стягивающего пояса', tightening_belt_beams_length)
    # print('Диаметр центров балок стягивающего пояса', d_last_center)
    # print('Радиус центров балок стягивающего пояса', r_last_center)
    # print('Углы поясов', angle_belts_grad)
    # print('Диаметры поясов', d_belts)
    # print('Радиусы поясов', r_belts)
    # print('Высоты поясов', belts_height)
    # print('Катет', leg)
    # print('Длина балки последнего пояса', last_belt_beams_length)
    # print('Длина первой балки', first_beam_length)

    """Танцы с бубном!!!"""
    ratio = 1  # Коэффициент корректировки
    encrim = 1
    delta1 = last_belt_beams_length - first_beam_length  # Дельта (1)
    delta1_a = delta1 / ratio  # Дельта (1) вычисляемая
    increasing_angles = math.degrees(2 * math.asin(delta1_a / (2 * r2)))  # Увеличение углов

    """Расчеты длин балок"""
    while True:
        angle_belt_grad_a = angle_grad_without_support_beam / 2 \
                            / num_of_belts + increasing_angles  # Угол половины пояса (градусы)
        angle_belts_grad_a = {str(i): i * 2 * angle_belt_grad_a for i in
                              range(1, num_of_belts)}  # Углы поясов (в градусах)
        angle_belts_grad_a[str(num_of_belts)] = angle_grad_without_support_beam
        angle_belts_rad_a = {str(i): math.radians(i * 2 * angle_belt_grad_a) for i in
                             range(1, num_of_belts)}  # Углы поясов (в радианах)
        angle_belts_rad_a[str(num_of_belts)] = angle_rad_without_support_beam
        d_belts_a = {str(i): 2 * r2 * math.sin(angle_belts_rad_a.get(str(i)) / 2) for i in
                     range(1, num_of_belts)}  # Диаметры поясов
        d_belts_a[str(num_of_belts)] = d_last
        beams_length_by_belts_a = {str(i): d_belts_a.get(str(i)) * math.sin(
            (math.radians(360 / num_of_beams.get(str(i)))) / 2) for i in
                                   range(1, num_of_belts)}  # Длины балок по поясам
        beams_length_by_belts_a[str(num_of_belts)] = tightening_belt_beams_length
        r_belts_a = {str(i): d_belts_a.get(str(i)) / 2 for i in
                     range(1, num_of_belts)}  # Радиусы поясов
        r_belts_a[str(num_of_belts)] = d_last / 2
        belts_heigth_a = {str(i): h - (r2 - math.sqrt(r2 ** 2 - r_belts_a.get(str(i)) ** 2)) for i in
                          range(1, num_of_belts + 1)}  # Высоты поясов
        belts_heigth_a[str(num_of_belts)] = belts_heigth.get(str(num_of_belts))     # Высота стягивающего пояса
        leg2 = leg(r_belts_a.get(str(num_of_belts - 1)),
                   belts_heigth_a.get(str(num_of_belts)),
                   belts_heigth_a.get(str(num_of_belts - 1)))
        last_belt_beams_length_a = math.sqrt((tightening_belt_beams_length /
                                              2) ** 2 + leg2 ** 2)  # Длина балки нижнего пояса
        first_beam_length_a = 2 * r2 * math.sin(math.radians(angle_belt_grad_a / 2))    # Длина первой радиальной балки
        delta3 = last_belt_beams_length_a - first_beam_length_a     # Дельта 3
        if round(delta3, 10) == 0:  # Вотрое значение (10) - до какого символа проводить расчеты
            v1x = r_belts_a.get('1')
            v2x = - r_belts_a.get('1')
            v1z = v2z = belts_heigth_a.get('1') - h
            fi = math.degrees(math.acos((v1x * v2x + v1z * v2z) / (     # Угол между радиальными балками
                    math.sqrt(v1x**2 + v1z**2)*math.sqrt(v2x**2 + v2z**2))))

            for i in range(1, num_of_belts):
                for j in range(num_of_beams.get(str(i))):
                    xcoordinates[literal[i] + str(j)] = round(xcord(r_belts_a.get(str(i)), j * knot_angles[i]), 10)
                    ycoordinates[literal[i] + str(j)] = round(ycord(r_belts_a.get(str(i)), j * knot_angles[i]), 10)

            for i in range(num_of_beams[str(num_of_belts)]):
                xcoordinates[literal[num_of_belts] + str(i)] = round(
                    xcord(r_belts_a.get(str(num_of_belts)), offset_angle + i * knot_angles[num_of_belts-1]), 10)
                ycoordinates[literal[num_of_belts] + str(i)] = round(
                    ycord(r_belts_a.get(str(num_of_belts)), offset_angle + i * knot_angles[num_of_belts - 1]), 10)

            for i in range(num_of_beams[str(num_of_belts)]):
                xcoordinates['z' + str(i)] = round(xcord(r1, offset_angle + i * knot_angles[num_of_belts - 1]), 10)
                ycoordinates['z' + str(i)] = round(ycord(r1, offset_angle + i * knot_angles[num_of_belts - 1]), 10)

            # Длины кольцевых балок
            for i in range(1, num_of_belts+1):
                lengths[literal[i]+str(1)] = round(beams_length_by_belts_a.get(str(i)), 10)

            # Длины радиальных балок (с 3-их)
            if num_of_belts == 3:
                lengths[literal[2] + str(3)] = round(length(xcoordinates.get(literal[1] + str(0)),
                                                            ycoordinates.get(literal[1] + str(0)),
                                                            belts_heigth_a.get(str(1)),
                                                            xcoordinates.get(literal[2] + str(1)),
                                                            ycoordinates.get(literal[2] + str(1)),
                                                            belts_heigth_a.get(str(2))), 10)
            else:
                for i in range(3, num_of_belts+1):
                    m = 3
                    j = 0
                    n = i - 2
                    while j < n:
                        lengths[literal[i-1] + str(m)] = round(length(xcoordinates.get(literal[i-2] + str(j)),
                                                                      ycoordinates.get(literal[i-2] + str(j)),
                                                                      belts_heigth_a.get(str(i-2)),
                                                                      xcoordinates.get(literal[i-1] + str(j+1)),
                                                                      ycoordinates.get(literal[i-1] + str(j+1)),
                                                                      belts_heigth_a.get(str(i-1))), 10)
                        j += 1
                        m += 1

            # print('Высоты поясов', belts_heigth_a)
            # print('Координаты по x', xcoordinates)
            # print('Координаты по y', ycoordinates)
            print(len(literal))
            print('Радиус кривизны купола ', r2)
            print('Радиусы поясов ', str(r_belts_a))
            # print('Высота купола', h)
            # print('Формула сферы: x^2+y^2+z^2 =', r2**2)
            # print('Угол радиальных балок', (180-fi)/2)
            # print('Угол радиальных балок', 90-math.acos(first_beam_length_a/2/r2)*180/math.pi)
            # print('Длины балок по поясам ' + str(beams_length_by_belts_a))
            # print('Диаметры поясов ' + str(d_belts_a))
            # print('Углы поясов ' + str(angle_belts_grad_a) + '\n')
            # print(angle_grad_without_support_beam)
            print(lengths)
            print('Длина нижней радиальной балки ', last_belt_beams_length_a)
            print(knot_angles)
            print(quantity)

            # with open(f, 'a', encoding='utf-8') as f:
            #     f.write('Угол половины пояса ' + str(angle_belt_grad_a) + '\n')
            #     f.write('Углы поясов ' + str(angle_belts_grad_a) + '\n')
            #     f.write('Диаметры поясов ' + str(d_belts_a) + '\n')
            #     f.write('Длины балок по поясам ' + str(beams_length_by_belts_a) + '\n')
            #     f.write('Радиусы поясов ' + str(r_belts_a) + '\n')
            #     f.write('Высоты поясов ' + str(belts_heigth_a) + '\n')
            #     f.write('Катет ' + str(leg2) + '\n')
            #     f.write('Длина нижней радиальной балки ' + str(last_belt_beams_length_a) + '\n')
            #     f.write('Длина верхней радиальной балки ' + str(first_beam_length_a) + '\n')
            #     f.write('Дельта 3 ' + str(delta3) + '\n')
            #     f.write('Коэффициент корректировки ' + str(ratio))
            break
        elif delta3 > 0:
            ratio -= encrim
            encrim /= 10
            delta1_a = delta1 / ratio  # Дельта (1) вычисляемая
            increasing_angles = math.degrees(2 * math.asin(delta1_a / (2 * r2)))  # Увеличение углов
        else:
            ratio += encrim
            delta1_a = delta1 / ratio  # Дельта (1) вычисляемая
            increasing_angles = math.degrees(2 * math.asin(delta1_a / (2 * r2)))  # Увеличение углов

    # Вычисляем массу всех балок (по центрам пока что)
    mass = 0
    for key in quantity:
        for i in range(1, quantity[key]+1):
            if i == 1:
                mass += num_of_beams.get(str(literal.index(key))) * lengths.get(key+str(i))
            elif i == 2:
                pass
            else:
                mass += lengths.get(key+str(i)) * 12
    mass += first_beam_length_a * 6 * (len(literal) - 2) + first_beam_length_a * num_of_beams[str(len(literal) - 2)]
    mass *= (6.44/1000)
    print(mass)
    print(num_of_beams)


if __name__ == '__main__':
    calc_length()
