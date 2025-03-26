#----------------------------------------------------------
# original code : https://github.com/qjadud1994/Korean-license-plate-Generator
# modified by : JPark @ 2025
#----------------------------------------------------------

import os, random
import cv2, argparse
import numpy as np

def mkdir(fpath):
    if not os.path.exists(directory):
        os.makedirs(directory)

# 안전하게 배치하려면: col + width <= Plate.shape[1] 체크
def safe_paste(dst, src, row, col):
    h, w, _ = src.shape
    if row + h <= dst.shape[0] and col + w <= dst.shape[1]:
        dst[row:row + h, col:col + w] = src
    else:
        print(f"❌ Cannot paste: row={row}, col={col}, size={h}x{w}, Plate={dst.shape}")
        
def random_bright(img):
    img = cv2.cvtColor(img, cv2.COLOR_RGB2HSV)
    img = np.array(img, dtype=np.float64)
    random_bright = .5 + np.random.uniform()
    img[:, :, 2] = img[:, :, 2] * random_bright
    img[:, :, 2][img[:, :, 2] > 255] = 255
    img = np.array(img, dtype=np.uint8)
    img = cv2.cvtColor(img, cv2.COLOR_HSV2RGB)
    return img

def folder_loading(folder):
    file_list = os.listdir(folder)
    o = []
    o_list = []
    
    for file in file_list:
        img_path = os.path.join(folder, file)
    
        # 이미지 로딩 시 실패 여부 체크
        img = cv2.imread(img_path)
        if img is None:
            #print(f"❌ Failed to load: {file}")
            continue
    
        o.append(img)
        o_list.append(file[:-4])

    #print(' len(o) = ', len(o))
    #print(o_list)
        
    return o, o_list
    
class ImageGenerator:
    def __init__(self, save_path):
        self.save_path = save_path
        # Plate
        self.plate_white = cv2.imread("assets/plate.jpg")
        self.plate_yellow = cv2.imread("assets/plate_y.jpg")
        self.plate_green = cv2.imread("assets/plate_g.jpg")
        self.plate_green2 = cv2.imread("assets/plate_g2.jpg")

        # loading Number
        folder = "./assets/num/"
        self.Number, self.number_list = folder_loading(folder)
        
        # loading Char
        folder = "./assets/char1/"        
        self.Char1, self.char_list = folder_loading(folder)
        
        # loading Number : yellow-two-line
        folder = "./assets/num_y/"
        self.Number_y, self.number_list_y = folder_loading(folder)

        # loading Char
        folder = "./assets/char1_y/"
        self.Char1_y, self.char_list_y = folder_loading(folder)

        # loading Region
        folder = "./assets/region_y/"
        self.Region_y, self.region_list_y = folder_loading(folder)
        
        # loading Number : green-two-line
        folder = "./assets/num_g/"
        self.Number_g, self.number_list_g = folder_loading(folder)

        # loading Number : green-two-line
        folder = "./assets/num_g2/"
        self.Number_g2, self.number_list_g2 = folder_loading(folder)

        # loading Char
        folder = "./assets/char1_g/"
        self.Char1_g, self.char_list_g = folder_loading(folder)

        # loading Char
        folder = "./assets/char2_g/"
        self.Char2_g, self.char_list_g = folder_loading(folder)

        # loading Region
        folder = "./assets/region_g/"
        self.Region_g, self.region_list_g = folder_loading(folder)
        #===========================================================
    def type01(self, num, save=False):
        number = [cv2.resize(number, (56, 83)) for number in self.Number]
        char = [cv2.resize(char1, (60, 83)) for char1 in self.Char1]
        Plate = cv2.resize(self.plate_white, (520, 110))
      
        for i, Iter in enumerate(range(num)):
            Plate = cv2.resize(self.plate_white, (520, 110))
            label = "t01_"
            # row -> y , col -> x
            row, col = 13, 35  # row + 83, col + 56
            # number 1
            rand_int = random.randint(0, 9)
            label += self.number_list[rand_int]
            #Plate[row:row + 83, col:col + 56, :] = number[rand_int]
            safe_paste(Plate, number[rand_int], row, col)
            col += 56

            # number 2
            rand_int = random.randint(0, 9)
            label += self.number_list[rand_int]
            #Plate[row:row + 83, col:col + 56, :] = number[rand_int]
            safe_paste(Plate, number[rand_int], row, col)
            col += 56

            # character 3
            label += self.char_list[i%37]
            #Plate[row:row + 83, col:col + 60, :] = char[i%37]
            safe_paste(Plate, char[i%37], row, col)
            col += (60 + 36)

            # number 4
            rand_int = random.randint(0, 9)
            label += self.number_list[rand_int]
            #Plate[row:row + 83, col:col + 56, :] = number[rand_int]
            safe_paste(Plate, number[rand_int], row, col)
            col += 56

            # number 5
            rand_int = random.randint(0, 9)
            label += self.number_list[rand_int]
            #Plate[row:row + 83, col:col + 56, :] = number[rand_int]
            safe_paste(Plate, number[rand_int], row, col)
            col += 56

            # number 6
            rand_int = random.randint(0, 9)
            label += self.number_list[rand_int]
            #Plate[row:row + 83, col:col + 56, :] = number[rand_int]
            safe_paste(Plate, number[rand_int], row, col)
            col += 56

            # number 7
            rand_int = random.randint(0, 9)
            label += self.number_list[rand_int]
            #Plate[row:row + 83, col:col + 56, :] = number[rand_int]
            safe_paste(Plate, number[rand_int], row, col)
            col += 56
            
            Plate = random_bright(Plate)
            if save:
                cv2.imwrite(self.save_path + label + ".jpg", Plate)
            else:
                cv2.imshow(label, Plate)
                cv2.waitKey(0)
                cv2.destroyAllWindows()
                
    def type01a(self, num, save=False):
        number = [cv2.resize(number, (56, 83)) for number in self.Number_g2]
        char = [cv2.resize(char1, (60, 83)) for char1 in self.Char2_g]
        Plate = cv2.resize(self.plate_white, (520, 110))
      
        for i, Iter in enumerate(range(num)):
            Plate = cv2.resize(self.plate_green2, (520, 110))
            label = "t01a_"
            # row -> y , col -> x
            row, col = 13, 35  # row + 83, col + 56
            # number 1
            rand_int = random.randint(0, 9)
            label += self.number_list[rand_int]
            #Plate[row:row + 83, col:col + 56, :] = number[rand_int]
            safe_paste(Plate, number[rand_int], row, col)
            col += 56

            # number 2
            rand_int = random.randint(0, 9)
            label += self.number_list[rand_int]
            #Plate[row:row + 83, col:col + 56, :] = number[rand_int]
            safe_paste(Plate, number[rand_int], row, col)
            col += 56

            # character 3
            label += self.char_list[i%37]
            #Plate[row:row + 83, col:col + 60, :] = char[i%37]
            safe_paste(Plate, char[i%37], row, col)
            col += (60 + 36)

            # number 4
            rand_int = random.randint(0, 9)
            label += self.number_list[rand_int]
            #Plate[row:row + 83, col:col + 56, :] = number[rand_int]
            safe_paste(Plate, number[rand_int], row, col)
            col += 56

            # number 5
            rand_int = random.randint(0, 9)
            label += self.number_list[rand_int]
            #Plate[row:row + 83, col:col + 56, :] = number[rand_int]
            safe_paste(Plate, number[rand_int], row, col)
            col += 56

            # number 6
            rand_int = random.randint(0, 9)
            label += self.number_list[rand_int]
            #Plate[row:row + 83, col:col + 56, :] = number[rand_int]
            safe_paste(Plate, number[rand_int], row, col)
            col += 56

            # number 7
            rand_int = random.randint(0, 9)
            label += self.number_list[rand_int]
            #Plate[row:row + 83, col:col + 56, :] = number[rand_int]
            safe_paste(Plate, number[rand_int], row, col)
            col += 56
            
            Plate = random_bright(Plate)
            if save:
                cv2.imwrite(self.save_path + label + ".jpg", Plate)
            else:
                cv2.imshow(label, Plate)
                cv2.waitKey(0)
                cv2.destroyAllWindows()
                

    def type02(self, num, save=False):
        number = [cv2.resize(number, (45, 83)) for number in self.Number]
        char = [cv2.resize(char1, (49, 70)) for char1 in self.Char1]
        Plate = cv2.resize(self.plate_white, (355, 155))

        for i, Iter in enumerate(range(num)):
            Plate = cv2.resize(self.plate_white, (355, 155))
            label = "t02_"
            row, col = 46, 10  # row + 83, col + 56

            # number 1
            rand_int = random.randint(0, 9)
            label += self.number_list[rand_int]
            #Plate[row:row + 83, col:col + 45, :] = number[rand_int]
            safe_paste(Plate, number[rand_int], row, col)
            col += 45

            # number 2
            rand_int = random.randint(0, 9)
            label += self.number_list[rand_int]
            #Plate[row:row + 83, col:col + 45, :] = number[rand_int]
            safe_paste(Plate, number[rand_int], row, col)
            col += 45

            # number 3
            label += self.char_list[i%37]
            #Plate[row + 12:row + 82, col + 2:col + 49 + 2, :] = char[i%37]
            safe_paste(Plate, char[i%37], row, col)
            col += 49 + 2

            # number 4
            rand_int = random.randint(0, 9)
            label += self.number_list[rand_int]
            #Plate[row:row + 83, col + 2:col + 45 + 2, :] = number[rand_int]
            safe_paste(Plate, number[rand_int], row, col)
            col += 45 + 2

            # number 5
            rand_int = random.randint(0, 9)
            label += self.number_list[rand_int]
            Plate[row:row + 83, col:col + 45, :] = number[rand_int]
            col += 45

            # number 6
            rand_int = random.randint(0, 9)
            label += self.number_list[rand_int]
            #Plate[row:row + 83, col:col + 45, :] = number[rand_int]
            safe_paste(Plate, number[rand_int], row, col)
            col += 45

            # number 7
            rand_int = random.randint(0, 9)
            label += self.number_list[rand_int]
            #Plate[row:row + 83, col:col + 45, :] = number[rand_int]
            safe_paste(Plate, number[rand_int], row, col)
            col += 45
            Plate = random_bright(Plate)
            if save:
                cv2.imwrite(self.save_path + label + ".jpg", Plate)
            else:
                cv2.imshow(label, Plate)
                cv2.waitKey(0)
                cv2.destroyAllWindows()

    def type03(self, num, save=False):
        number1 = [cv2.resize(number, (44, 60)) for number in self.Number_y]
        number2 = [cv2.resize(number, (64, 90)) for number in self.Number_y]
        region = [cv2.resize(region, (88, 60)) for region in self.Region_y]
        char = [cv2.resize(char1, (64, 62)) for char1 in self.Char1_y]

        for i, Iter in enumerate(range(num)):
            Plate = cv2.resize(self.plate_yellow, (336, 170))

            #label = str()
            label = 't03_'
            
            # row -> y , col -> x
            row, col = 8, 76

            # region
            label += self.region_list_y[i % 16]
            #Plate[row:row + 60, col:col + 88, :] = region[i % 16]
            safe_paste(Plate, region[i % 16], row, col)
            col += 88 + 8

            # number 1
            rand_int = random.randint(0, 9)
            label += self.number_list_y[rand_int]
            #Plate[row:row + 60, col:col + 44, :] = number1[rand_int]
            safe_paste(Plate, number1[rand_int], row, col)
            col += 44

            # number 2
            rand_int = random.randint(0, 9)
            label += self.number_list_y[rand_int]
            #Plate[row:row + 60, col:col + 44, :] = number1[rand_int]
            safe_paste(Plate, number1[rand_int], row, col)
            row, col = 72, 8

            # character 3
            label += self.char_list_y[i % 37]
            #Plate[row:row + 62, col:col + 64, :] = char[i % 37]
            safe_paste(Plate, char[i % 37], row, col)
            col += 64

            # number 4
            rand_int = random.randint(0, 9)
            label += self.number_list_y[rand_int]
            #Plate[row:row + 90, col:col + 64, :] = number2[rand_int]
            safe_paste(Plate, number2[rand_int], row, col)
            col += 64

            # number 5
            rand_int = random.randint(0, 9)
            label += self.number_list_y[rand_int]
            #Plate[row:row + 90, col:col + 64, :] = number2[rand_int]
            safe_paste(Plate, number2[rand_int], row, col)
            col += 64

            # number 6
            rand_int = random.randint(0, 9)
            label += self.number_list_y[rand_int]
            #Plate[row:row + 90, col:col + 64, :] = number2[rand_int]
            safe_paste(Plate, number2[rand_int], row, col)
            col += 64

            # number 7
            rand_int = random.randint(0, 9)
            label += self.number_list_y[rand_int]
            #Plate[row:row + 90, col:col + 64, :] = number2[rand_int]
            safe_paste(Plate, number2[rand_int], row, col)
            Plate = random_bright(Plate)
            if save:
                cv2.imwrite(self.save_path + label + ".jpg", Plate)
            else:
                cv2.imshow(label, Plate)
                cv2.waitKey(0)
                cv2.destroyAllWindows()

    def type04(self, num, save=False):
        number1 = [cv2.resize(number, (44, 60)) for number in self.Number_g]
        number2 = [cv2.resize(number, (64, 90)) for number in self.Number_g]
        region = [cv2.resize(region, (88, 60)) for region in self.Region_g]
        char = [cv2.resize(char1, (64, 62)) for char1 in self.Char1_g]

        for i, Iter in enumerate(range(num)):
            Plate = cv2.resize(self.plate_green, (336, 170))

            #label = str()
            label = 't04_'
            
            # row -> y , col -> x
            row, col = 8, 76

            # region
            label += self.region_list_g[i % 16]
            #Plate[row:row + 60, col:col + 88, :] = region[i % 16]
            safe_paste(Plate, region[i % 16], row, col)
            col += 88 + 8

            # number 1
            rand_int = random.randint(0, 9)
            label += self.number_list_g[rand_int]
            #Plate[row:row + 60, col:col + 44, :] = number1[rand_int]
            safe_paste(Plate, number1[rand_int], row, col)
            col += 44

            # number 2
            rand_int = random.randint(0, 9)
            label += self.number_list_g[rand_int]
            #Plate[row:row + 60, col:col + 44, :] = number1[rand_int]
            safe_paste(Plate, number1[rand_int], row, col)

            row, col = 72, 8

            # character 3
            label += self.char_list_g[i % 37]
            #Plate[row:row + 62, col:col + 64, :] = char[i % 37]
            safe_paste(Plate, char[i % 37], row, col)
            col += 64

            # number 4
            rand_int = random.randint(0, 9)
            label += self.number_list_g[rand_int]
            #Plate[row:row + 90, col:col + 64, :] = number2[rand_int]
            safe_paste(Plate, number2[rand_int], row, col)
            col += 64

            # number 5
            rand_int = random.randint(0, 9)
            label += self.number_list_g[rand_int]
            #Plate[row:row + 90, col:col + 64, :] = number2[rand_int]
            safe_paste(Plate, number2[rand_int], row, col)
            col += 64

            # number 6
            rand_int = random.randint(0, 9)
            label += self.number_list_g[rand_int]
            #Plate[row:row + 90, col:col + 64, :] = number2[rand_int]
            safe_paste(Plate, number2[rand_int], row, col)
            col += 64

            # number 7
            rand_int = random.randint(0, 9)
            label += self.number_list_g[rand_int]
            #Plate[row:row + 90, col:col + 64, :] = number2[rand_int]
            safe_paste(Plate, number2[rand_int], row, col)
            Plate = random_bright(Plate)
            if save:
                cv2.imwrite(self.save_path + label + ".jpg", Plate)
            else:
                cv2.imshow(label, Plate)
                cv2.waitKey(0)
                cv2.destroyAllWindows()

    def type05(self, num, save=False):
        number1 = [cv2.resize(number, (60, 65)) for number in self.Number_g]
        number2 = [cv2.resize(number, (80, 90)) for number in self.Number_g]
        char = [cv2.resize(char1, (60, 65)) for char1 in self.Char1_g]

        for i, Iter in enumerate(range(num)):
            Plate = cv2.resize(self.plate_green, (336, 170))
            random_width, random_height = 336, 170
            #label = "Z"
            label = 't05_'

            # row -> y , col -> x
            row, col = 8, 78

            # number 1
            rand_int = random.randint(0, 9)
            label += self.number_list_g[rand_int]
            Plate[row:row + 65, col:col + 60, :] = number1[rand_int]
            col += 60

            # number 2
            rand_int = random.randint(0, 9)
            label += self.number_list_g[rand_int]
            Plate[row:row + 65, col:col + 60, :] = number1[rand_int]
            col += 60

            # character 3
            label += self.char_list_g[i%37]
            Plate[row:row + 65, col:col + 60, :] = char[i%37]
            row, col = 75, 8

            # number 4
            rand_int = random.randint(0, 9)
            label += self.number_list_g[rand_int]
            Plate[row:row + 90, col:col + 80, :] = number2[rand_int]
            col += 80

            # number 5
            rand_int = random.randint(0, 9)
            label += self.number_list_g[rand_int]
            Plate[row:row + 90, col:col + 80, :] = number2[rand_int]
            col += 80

            # number 6
            rand_int = random.randint(0, 9)
            label += self.number_list_g[rand_int]
            Plate[row:row + 90, col:col + 80, :] = number2[rand_int]
            col += 80

            # number 7
            rand_int = random.randint(0, 9)
            label += self.number_list_g[rand_int]
            Plate[row:row + 90, col:col + 80, :] = number2[rand_int]

            Plate = random_bright(Plate)

            if save:
                cv2.imwrite(self.save_path + label + ".jpg", Plate)
            else:
                cv2.imshow(label, Plate)
                cv2.waitKey(0)
                cv2.destroyAllWindows()


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("-i", "--img_dir", help="save image directory",              type=str, default="./outputs/")
    parser.add_argument("-n", "--num", help="number of image",
                        type=int, default=1)
    parser.add_argument("-s", "--save", help="save or imshow",
                        type=bool, default=True)
    parser.add_argument('--types', nargs='+', default=['type01', 'type01a', 'type02', 'type03', 'type04', 'type05'],
                        help='리스트 형태로 Type 메서드를 선택합니다.')
    args = parser.parse_args()
    
    img_dir = args.img_dir
    ig = ImageGenerator(img_dir)
    
    num_img = args.num
    is_save = args.save
    
    # 선택적으로 호출할 타입 목록 (예: 'type01', 'type03' 등)
    selected_types = args.types  # 리스트 형태로 들어온다고 가정    
    #print(selected_types)

    # getattr을 사용하여 동적으로 메서드 호출
    for type_name in selected_types:
        #print(type_name)
        method = getattr(ig, type_name, None)
        if callable(method):
            method(num_img, save=is_save)
            print(f'{type_name} processing is ok')
        else:
            print(f"⚠️ {type_name} is not a valid method of ImageGenerator.")

    
if __name__ == "__main__":
	main()

    
#----------------------------------------------------------
# End of this file
#----------------------------------------------------------