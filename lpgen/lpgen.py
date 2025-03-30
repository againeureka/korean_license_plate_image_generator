#----------------------------------------------------------
# original code : https://github.com/qjadud1994/Korean-license-plate-Generator
# modified by : JPark @ March 2025
#----------------------------------------------------------

import os, random
import cv2, argparse
import numpy as np
from pathlib import Path
import pkg_resources  # 또는 importlib.resources (Python 3.9+)

def get_asset_path(relative_path):
    base = Path(__file__).parent
    return os.path.join(base, 'assets', relative_path)

def apply_augmentation(img, mode='perspective', crop=False):
    h, w = img.shape[:2]

    if mode == 'perspective':
        # Perspective warp
        margin = 30
        pts1 = np.float32([[0, 0], [w, 0], [0, h], [w, h]])
        pts2 = np.float32([
            [random.randint(0, margin), random.randint(0, margin)],
            [w - random.randint(0, margin), random.randint(0, margin)],
            [random.randint(0, margin), h - random.randint(0, margin)],
            [w - random.randint(0, margin), h - random.randint(0, margin)]
        ])
        M = cv2.getPerspectiveTransform(pts1, pts2)
        img = cv2.warpPerspective(img, M, (w, h))

    elif mode == 'affine':
        # Rotation
        ang_rot = np.random.uniform(-6, 6)
        M_rot = cv2.getRotationMatrix2D((w/2, h/2), ang_rot, 0.9)
        img = cv2.warpAffine(img, M_rot, (w, h))

        # Translation
        tx = np.random.uniform(-3, 3)
        ty = np.random.uniform(-3, 3)
        M_trans = np.float32([[1, 0, tx], [0, 1, ty]])
        img = cv2.warpAffine(img, M_trans, (w, h))

        # Shear
        pts1 = np.float32([[5, 5], [20, 5], [5, 20]])
        pt1 = 5 + np.random.uniform(-3, 3)
        pt2 = 20 + np.random.uniform(-3, 3)
        pts2 = np.float32([[pt1, 5], [pt2, pt1], [5, pt2]])
        M_shear = cv2.getAffineTransform(pts1, pts2)
        img = cv2.warpAffine(img, M_shear, (w, h))

    # 2. Affine 변형
    elif mode == 'affine_padding':
        # 패딩 추가
        pad = max(h, w) // 6
        img = cv2.copyMakeBorder(img, pad, pad, pad, pad, cv2.BORDER_CONSTANT, value=[255, 255, 255])
        h_pad, w_pad = img.shape[:2]
        
        # 회전
        ang_rot = np.random.uniform(-6, 6)
        M_rot = cv2.getRotationMatrix2D((w_pad/2, h_pad/2), ang_rot, 0.9)
        img = cv2.warpAffine(img, M_rot, (w_pad, h_pad))

        # 이동
        tx = np.random.uniform(-3, 3)
        ty = np.random.uniform(-3, 3)
        M_trans = np.float32([[1, 0, tx], [0, 1, ty]])
        img = cv2.warpAffine(img, M_trans, (w_pad, h_pad))

        # 시어링
        pts1 = np.float32([[5, 5], [20, 5], [5, 20]])
        pt1 = 5 + np.random.uniform(-3, 3)
        pt2 = 20 + np.random.uniform(-3, 3)
        pts2 = np.float32([[pt1, 5], [pt2, pt1], [5, pt2]])
        M_shear = cv2.getAffineTransform(pts1, pts2)
        img = cv2.warpAffine(img, M_shear, (w_pad, h_pad))

    # Brightness (공통)
    hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV).astype(np.float32)
    hsv[..., 2] *= 0.4 + np.random.uniform()
    hsv[..., 2] = np.clip(hsv[..., 2], 0, 255)
    img = cv2.cvtColor(hsv.astype(np.uint8), cv2.COLOR_HSV2BGR)

    # Blur (공통)
    k = random.choice([1, 3, 5, 7])
    img = cv2.blur(img, (k, k))

    '''
    # Optional crop (중앙부)
    if crop and h >= 280 and w >= 660:
        return img[130:280, 120:660]
    '''

    # 3. 중심부 크롭 (패딩 고려 후 안정적)
    if crop:
        center_y, center_x = h_pad // 2, w_pad // 2
        crop_h, crop_w = h, w  # 원래 크기로 복원
        y1, y2 = center_y - crop_h//2, center_y + crop_h//2
        x1, x2 = center_x - crop_w//2, center_x + crop_w//2
        img = img[y1:y2, x1:x2]


    return img


def image_augmentation(img, crop_type2=False):
    h, w = img.shape[:2]

    # 1. Perspective Warp
    margin = 30
    pts1 = np.float32([[0, 0], [w, 0], [0, h], [w, h]])
    pts2 = np.float32([
        [random.randint(0, margin), random.randint(0, margin)],
        [w - random.randint(0, margin), random.randint(0, margin)],
        [random.randint(0, margin), h - random.randint(0, margin)],
        [w - random.randint(0, margin), h - random.randint(0, margin)]
    ])
    M = cv2.getPerspectiveTransform(pts1, pts2)
    img = cv2.warpPerspective(img, M, (w, h))

    # 2. Random Brightness
    hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV).astype(np.float32)
    hsv[:, :, 2] *= 0.4 + np.random.uniform()
    hsv[:, :, 2] = np.clip(hsv[:, :, 2], 0, 255)
    img = cv2.cvtColor(hsv.astype(np.uint8), cv2.COLOR_HSV2BGR)

    # 3. Blur
    k = random.choice([1, 3, 5, 7])  # 홀수만 허용
    img = cv2.blur(img, (k, k))

    # 4. Crop
    # 크롭 조건 추가
    if crop_type2:
        if h >= 280 and w >= 600:
            return img[130:280, 180:600]
        else:
            print(f"⚠️ 크롭 생략: 이미지 크기 ({h}, {w})가 너무 작음")
            return img
    else:
        if h >= 280 and w >= 660:
            return img[130:280, 120:660]
        else:
            print(f"⚠️ 크롭 생략: 이미지 크기 ({h}, {w})가 너무 작음")
            return img

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

# 자음 및 모음 매핑
chosung_map = {
    'r': 'ㄱ', 's': 'ㄴ', 'e': 'ㄷ', 'f': 'ㄹ', 'a': 'ㅁ',
    'q': 'ㅂ', 't': 'ㅅ', 'd': 'ㅇ', 'w': 'ㅈ', 'c': 'ㅊ',
    'z': 'ㅋ', 'x': 'ㅌ', 'v': 'ㅍ', 'g': 'ㅎ'
}

jungsung_map = {
    'k': 'ㅏ', 'o': 'ㅐ', 'i': 'ㅑ', 'j': 'ㅓ', 'p': 'ㅔ',
    'u': 'ㅕ', 'h': 'ㅗ', 'y': 'ㅛ', 'n': 'ㅜ', 'b': 'ㅠ',
    'm': 'ㅡ', 'l': 'ㅣ'
}

# 자모를 유니코드 한글 문자로 조합하는 함수
def compose_hangul(chosung, jungsung, jongsung=''):
    CHOSUNG_LIST = 'ㄱㄲㄴㄷㄸㄹㅁㅂㅃㅅㅆㅇㅈㅉㅊㅋㅌㅍㅎ'
    JUNGSUNG_LIST = 'ㅏㅐㅑㅒㅓㅔㅕㅖㅗㅘㅙㅚㅛㅜㅝㅞㅟㅠㅡㅢㅣ'
    JONGSUNG_LIST = [''] + list('ㄱㄲㄳㄴㄵㄶㄷㄹㄺㄻㄼㄽㄾㄿㅀㅁㅂㅄㅅㅆㅇㅈㅊㅋㅌㅍㅎ')

    try:
        cho_idx = CHOSUNG_LIST.index(chosung)
        jung_idx = JUNGSUNG_LIST.index(jungsung)
        jong_idx = JONGSUNG_LIST.index(jongsung) if jongsung else 0
        code = 0xAC00 + (cho_idx * 21 * 28) + (jung_idx * 28) + jong_idx
        return chr(code)
    except ValueError:
        return ''  # 변환할 수 없는 경우

# 키보드 코드 -> 한글 변환 함수
def convert_keyboard_code_to_hangul(code):
    if len(code) < 2:
        return ''  # 최소 초성+중성 필요
    cho = chosung_map.get(code[0], '')
    jung = jungsung_map.get(code[1], '')
    jong = ''
    if len(code) >= 3:
        jong = chosung_map.get(code[2], '')  # 종성도 초성과 같은 테이블 사용
    return compose_hangul(cho, jung, jong)

# 예시
#print(convert_keyboard_code_to_hangul('ak'))  # 마
#print(convert_keyboard_code_to_hangul('fj'))  # 러



# 알파벳 지역 코드 매핑
region_code_map = {
    'A': '서울',
    'B': '경기',
    'C': '인천',
    'D': '강원',
    'E': '충남',
    'F': '대전',
    'G': '충북',
    'H': '부산',
    'I': '울산',
    'J': '대구',
    'K': '경북',
    'L': '경남',
    'M': '전남',
    'N': '광주',
    'O': '전북',
    'P': '제주'
}

# 지역 코드 → 한글 지역명 변환 함수
def convert_region_code_to_korean(code):
    return region_code_map.get(code.upper(), '알 수 없음')

# 예시
#print(convert_region_code_to_korean('A'))  # 서울
#print(convert_region_code_to_korean('F'))  # 대전
#print(convert_region_code_to_korean('Z'))  # 알 수 없음

def save_to_file(folder_path, label, Plate):
    """폴더가 없으면 생성합니다."""
    if not os.path.exists(folder_path):
        os.makedirs(folder_path)
        print(f"폴더 '{folder_path}'를 생성했습니다.")
    else:
        #print(f"폴더 '{folder_path}'가 이미 존재합니다.")
        pass

    cv2.imwrite(folder_path + label + ".jpg", Plate)


#================================================================
class ImageGenerator:
    def __init__(self, save_path):
        self.save_path = save_path + '/'

        print( 'path = ', get_asset_path("plate.jpg") )
        
        # Plate
        self.plate_white = cv2.imread( get_asset_path("plate.jpg") )
        self.plate_yellow = cv2.imread(get_asset_path("plate_y.jpg") )
        self.plate_green = cv2.imread(get_asset_path("plate_g.jpg") ) 
        self.plate_green2 = cv2.imread(get_asset_path("plate_g2.jpg") )

        # loading Number
        folder = get_asset_path("num/")
        self.Number, self.number_list = folder_loading(folder)
        
        # loading Char
        folder = get_asset_path("char1/")
        self.Char1, self.char_list = folder_loading(folder)
        
        # loading Number : yellow-two-line
        folder = get_asset_path("num_y/")
        self.Number_y, self.number_list_y = folder_loading(folder)

        # loading Char
        folder = get_asset_path("char1_y/")
        self.Char1_y, self.char_list_y = folder_loading(folder)

        # loading Region
        folder = get_asset_path("region_y/")
        self.Region_y, self.region_list_y = folder_loading(folder)
        
        # loading Number : green-two-line
        folder = get_asset_path("num_g/")
        self.Number_g, self.number_list_g = folder_loading(folder)

        # loading Number : green-two-line
        folder = get_asset_path("num_g2/")
        self.Number_g2, self.number_list_g2 = folder_loading(folder)

        # loading Char
        folder = get_asset_path("char1_g/")
        self.Char1_g, self.char_list_g = folder_loading(folder)

        # loading Char
        folder = get_asset_path("char2_g/")
        self.Char2_g, self.char_list_g = folder_loading(folder)

        # loading Region
        folder = get_asset_path("region_g/")
        self.Region_g, self.region_list_g = folder_loading(folder)
        #===========================================================

    def type01(self, num, is_save=False, warp=True, is_rb=False):
        number = [cv2.resize(number, (56, 83)) for number in self.Number]
        char = [cv2.resize(char1, (60, 83)) for char1 in self.Char1]
        Plate = cv2.resize(self.plate_white, (520, 110))
      
        for i, Iter in enumerate(range(num)):
            Plate = cv2.resize(self.plate_white, (520, 110))
            label = str() 
            
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
            label += convert_keyboard_code_to_hangul ( self.char_list[i%37] )
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

            # ✅ 랜덤 밝기
            if is_rb:
                Plate = random_bright(Plate)

            # ✅ 워핑 옵션
            if warp == 'perspective':
                Plate = apply_augmentation(Plate, mode='perspective')
            elif warp == 'affine':
                Plate = apply_augmentation(Plate, mode='affine')
            
            # ✅ 저장 옵션
            if is_save:
                save_to_file(self.save_path, label, Plate)
                
    def type02(self, num, is_save=False, warp=True, is_rb=False):
        number = [cv2.resize(number, (56, 83)) for number in self.Number_g2]
        char = [cv2.resize(char1, (60, 83)) for char1 in self.Char2_g]
        Plate = cv2.resize(self.plate_white, (520, 110))
      
        for i, Iter in enumerate(range(num)):
            Plate = cv2.resize(self.plate_green2, (520, 110))
            label = str() 
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
            label += convert_keyboard_code_to_hangul ( self.char_list[i%37] )
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
            

            # ✅ 랜덤 밝기
            if is_rb:
                Plate = random_bright(Plate)

            # ✅ 워핑 옵션
            if warp == 'perspective':
                Plate = apply_augmentation(Plate, mode='perspective')
            elif warp == 'affine':
                Plate = apply_augmentation(Plate, mode='affine')
            
            # ✅ 저장 옵션
            if is_save:
                save_to_file(self.save_path, label, Plate)                

    def type03(self, num, is_save=False, warp=True, is_rb=False):
        number = [cv2.resize(number, (45, 83)) for number in self.Number]
        char = [cv2.resize(char1, (49, 70)) for char1 in self.Char1]
        Plate = cv2.resize(self.plate_white, (355, 155))

        for i, Iter in enumerate(range(num)):
            Plate = cv2.resize(self.plate_white, (355, 155))
            label = str() # "t02_"
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
            label += convert_keyboard_code_to_hangul( self.char_list[i%37] )
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

            # ✅ 랜덤 밝기
            if is_rb:
                Plate = random_bright(Plate)

            # ✅ 워핑 옵션
            if warp == 'perspective':
                Plate = apply_augmentation(Plate, mode='perspective')
            elif warp == 'affine':
                Plate = apply_augmentation(Plate, mode='affine')
            
            # ✅ 저장 옵션
            if is_save:
                save_to_file(self.save_path, label, Plate)

    def type04(self, num, is_save=False, warp=True, is_rb=False):
        number1 = [cv2.resize(number, (44, 60)) for number in self.Number_y]
        number2 = [cv2.resize(number, (64, 90)) for number in self.Number_y]
        region = [cv2.resize(region, (88, 60)) for region in self.Region_y]
        char = [cv2.resize(char1, (64, 62)) for char1 in self.Char1_y]

        for i, Iter in enumerate(range(num)):
            Plate = cv2.resize(self.plate_yellow, (336, 170))

            label = str() # "t03_"
            
            # row -> y , col -> x
            row, col = 8, 76

            # region
            label += convert_region_code_to_korean ( self.region_list_y[i % 16] )
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
            label += convert_keyboard_code_to_hangul ( self.char_list_y[i % 37] )
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

            # ✅ 랜덤 밝기
            if is_rb:
                Plate = random_bright(Plate)

            # ✅ 워핑 옵션
            if warp == 'perspective':
                Plate = apply_augmentation(Plate, mode='perspective')
            elif warp == 'affine':
                Plate = apply_augmentation(Plate, mode='affine')
            
            # ✅ 저장 옵션
            if is_save:
                save_to_file(self.save_path, label, Plate)

    def type05(self, num, is_save=False, warp=True, is_rb=False):
        number1 = [cv2.resize(number, (44, 60)) for number in self.Number_g]
        number2 = [cv2.resize(number, (64, 90)) for number in self.Number_g]
        region = [cv2.resize(region, (88, 60)) for region in self.Region_g]
        char = [cv2.resize(char1, (64, 62)) for char1 in self.Char1_g]

        for i, Iter in enumerate(range(num)):
            Plate = cv2.resize(self.plate_green, (336, 170))

            label = str() # "t04_"
            
            # row -> y , col -> x
            row, col = 8, 76

            # region
            label += convert_region_code_to_korean ( self.region_list_g[i % 16] )
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
            label += convert_keyboard_code_to_hangul( self.char_list_g[i % 37] )
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

            # ✅ 랜덤 밝기
            if is_rb:
                Plate = random_bright(Plate)

            # ✅ 워핑 옵션
            if warp == 'perspective':
                Plate = apply_augmentation(Plate, mode='perspective')
            elif warp == 'affine':
                Plate = apply_augmentation(Plate, mode='affine')
            
            # ✅ 저장 옵션
            if is_save:
                save_to_file(self.save_path, label, Plate)

    def type06(self, num, is_save=False, warp=True, is_rb=False):
        number1 = [cv2.resize(number, (60, 65)) for number in self.Number_g]
        number2 = [cv2.resize(number, (80, 90)) for number in self.Number_g]
        char = [cv2.resize(char1, (60, 65)) for char1 in self.Char1_g]

        for i, Iter in enumerate(range(num)):
            Plate = cv2.resize(self.plate_green, (336, 170))
            random_width, random_height = 336, 170
            #label = "Z"
            label = str() # "t05_"

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
            label += convert_keyboard_code_to_hangul ( self.char_list_g[i%37] )
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

            # ✅ 랜덤 밝기
            if is_rb:
                Plate = random_bright(Plate)

            # ✅ 워핑 옵션
            if warp == 'perspective':
                Plate = apply_augmentation(Plate, mode='perspective')
            elif warp == 'affine':
                Plate = apply_augmentation(Plate, mode='affine')
            
            # ✅ 저장 옵션
            if is_save:
                save_to_file(self.save_path, label, Plate)

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("-o", "--output", help="save image directory",
                        type=str, default="./outputs/")
    parser.add_argument("-n", "--num", help="number of image",
                        type=int, default=1)
    parser.add_argument("-s", "--is_save", help="save or imshow",
                        type=bool, default=True)
    parser.add_argument("-w", "--warp", help="{False, perspective, affine}",
                        type=str, default="False")
    parser.add_argument("-b", "--is_random_brightness", help="True, False",
                        type=bool, default=False)
    parser.add_argument('--types', nargs='+', default=['type01', 'type02', 'type03', 'type04', 'type05', 'type06'],
                        help='리스트 형태로 Type 메서드를 선택합니다.')
    args = parser.parse_args()
    
    img_dir = args.output
    ig = ImageGenerator(img_dir)
   
    num_img = args.num
    is_save = args.is_save
    is_random_brightness = args.is_random_brightness
    warp = args.warp
    
    # 선택적으로 호출할 타입 목록 (예: 'type01', 'type03' 등)
    selected_types = args.types  # 리스트 형태로 들어온다고 가정    

    # getattr을 사용하여 동적으로 메서드 호출
    for type_name in selected_types:
        method = getattr(ig, type_name, None)
        if callable(method):
            method(num_img, 
                   is_save = is_save, 
                   warp = warp, 
                   is_rb = is_random_brightness)
            print(f'{type_name} processing is ok')
        else:
            print(f"⚠️ {type_name} is not a valid method of ImageGenerator.")
    
if __name__ == "__main__":
	main()

#----------------------------------------------------------
# End of this file
#----------------------------------------------------------

