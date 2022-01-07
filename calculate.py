import math


def calc_length(d=10430, num_of_belts=3, k=0.8, sup_beam_length=400):
    """Основные вычисления"""
    num_of_beams = {str(i): i * 6 for i in range(1, num_of_belts)}
    num_of_sup_beams = (num_of_belts - 1) * 6  # Количество опорных балок = Количество балок стягивающего пояса
    r1 = d / 2  # Радиус резервуара
    r2 = k * d  # Радиус кривизны купола
    h = r2 - math.sqrt((r2 ** 2) - (r1 ** 2))  # Высота купола
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
    d_last_center = math.sqrt(
        (d_last / 2) ** 2 - (tightening_belt_beams_length / 2) ** 2) * 2  # Диаметр центров балок стягивающего пояса
    r_last_center = d_last_center / 2

    """Пересмотреть после определения реальных длин балок"""
    angle_belt_grad = angle_grad_without_support_beam / 2 / num_of_belts  # Угол половины пояса (градусы)
    angle_belts_rad = {str(i): math.radians(i * 2 * angle_belt_grad) for i in
                       range(1, num_of_belts + 1)}  # Углы поясов (в радианах)
    d_belts = {str(i): 2 * r2 * math.sin(angle_belts_rad.get(str(i)) / 2) for i in
               range(1, num_of_belts + 1)}  # Диаметры поясов
    r_belts = {str(i): d_belts.get(str(i)) / 2 for i in
               range(1, num_of_belts + 1)}  # Радиусы поясов
    belts_heigth = {str(i): h - (r2 - math.sqrt(r2 ** 2 - r_belts.get(str(i)) ** 2)) for i
                    in range(1, num_of_belts + 1)}  # Высоты поясов
    leg = math.sqrt((r_last_center - r_belts.get(str(num_of_belts - 1))) ** 2 + (
            belts_heigth.get(str(num_of_belts)) - belts_heigth.get(
            str(num_of_belts - 1))) ** 2)   # Расстояние от узла предпоследнего пояса \
                                            # до середины балки последнего
    last_belt_beams_length = math.sqrt((tightening_belt_beams_length / 2) ** 2 + leg ** 2)
    first_beam_length = 2 * r2 * math.sin(math.radians(angle_belt_grad / 2))

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

    delta2 = 0.0000000000000001
    while True:
        angle_belt_grad_a = angle_grad_without_support_beam / 2 \
                            / num_of_belts + increasing_angles  # Угол половины пояса (градусы)
        angle_belts_grad_a = {str(i): i * 2 * angle_belt_grad_a for i in
                              range(1, num_of_belts + 1)}  # Углы поясов (в градусах)
        angle_belts_rad_a = {str(i): math.radians(i * 2 * angle_belt_grad_a) for i in
                             range(1, num_of_belts + 1)}  # Углы поясов (в радианах)
        d_belts_a = {str(i): 2 * r2 * math.sin(angle_belts_rad_a.get(str(i)) / 2) for i in
                     range(1, num_of_belts)}  # Диаметры поясов
        d_belts_a[str(num_of_belts)] = d_last
        beams_length_by_belts_a = {str(i): d_belts_a.get(str(i)) * math.sin(
            (math.radians(360 / num_of_beams.get(str(i)))) / 2) for i in
                                   range(1, num_of_belts)}  # Длины балок по поясам
        r_belts_a = {str(i): d_belts_a.get(str(i)) / 2 for i in
                     range(1, num_of_belts)}  # Радиусы поясов
        r_belts_a[str(num_of_belts)] = d_last / 2
        belts_heigth_a = {str(i): h - (r2 - math.sqrt(r2 ** 2 - r_belts_a.get(str(i)) ** 2)) for i in
                          range(1, num_of_belts + 1)}  # Высоты поясов
        belts_heigth_a[str(num_of_belts)] = belts_heigth.get(str(num_of_belts))
        leg_a = math.sqrt((r_last_center - r_belts_a.get(str(num_of_belts - 1))) ** 2 + (
                belts_heigth_a.get(str(num_of_belts)) - belts_heigth_a.get(
                str(num_of_belts - 1))) ** 2)   # Расстояние от узла предпоследнего пояса\
                                                # до середины балки последнего
        last_belt_beams_length_a = math.sqrt((tightening_belt_beams_length / 2) ** 2 + leg_a ** 2)
        first_beam_length_a = 2 * r2 * math.sin(math.radians(angle_belt_grad_a / 2))
        delta3 = last_belt_beams_length_a - first_beam_length_a
        if round(delta3, 12) == 0:
            print(angle_belt_grad_a)
            print(angle_belts_grad_a)
            print(d_belts_a)
            print(beams_length_by_belts_a)
            print(r_belts_a)
            print(belts_heigth_a)
            print(leg_a)
            print(last_belt_beams_length_a)
            print(first_beam_length_a)
            print(delta3)
            print(ratio)
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


if __name__ == '__main__':
    calc_length()