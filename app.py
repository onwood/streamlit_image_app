import streamlit as st
import os
from PIL import Image, ImageFilter, ImageEnhance
from datetime import datetime

# 깃 연동 테스트

# 이미지 파일 다양하게 편집

def load_image(image_file):
    img = Image.open(image_file)
    return img


# 디렉토리와 이미지를 주면 해당 디렉토리에 이 이미지를 저장하는 함수
def save_uploaded_img(directory, img):
    
    # 1. 디렉토리가 있는지 확인하고 없을 경우 만든다.
    if not os.path.exists(directory):
        os.makedirs(directory)

    # 2. 이미지 파일 저장.(현재 시간으로 활용, 나중에 uuid라고 유니크한 파일명 만드는 방법이 또 있음)
    now_filename = datetime.now().isoformat().replace(':','-').replace('.','-')
    img.save(directory + '/' + now_filename + '.jpg')
    return st.success('Saved file : {} in {}'.format(now_filename, directory))

def main():
    
    print(datetime.now().isoformat())

    st.subheader('이미지파일 업로드')
    # 1. 파일 업로드 하기
    image_file_list = st.file_uploader('Upload Image', type=['png','jpg','jpeg'], accept_multiple_files=True)

    print(image_file_list)
        
    if image_file_list != []:

    # 2. 각 파일을 이미지로 바꿔주기    
        image_list = []
    
    # 2-1. 모든 파일이 image_list에 이미지로 저장됨    
        for image_file in image_file_list:
            img = load_image(image_file)
            image_list.append(img)

    # 3. 이미지를 화면에 확인해 본다.(디버깅 확인용)
        # for img in image_list:
        #     st.image(img)

        option_list=['Show Image', 'Rotate Image', 'Create Thumbnail', 'Crop Image', 'Merge Images', 'Flip Image', 
        'Change Color', 'Filters - Sharpen', 'Filters - Edge Enhance', 'Contrast Image']

        option = st.selectbox('옵션을 선택하세요.', option_list)

            

        if option == 'Show Image':
            for img in image_list:
                st.image(img)
       
            directory = st.text_input('파일 경로 입력')
            if st.button('파일 저장'):
                for img in image_list:
                    save_uploaded_img(directory, img)




        elif option == 'Rotate Image':        
            # 1. 유저가 입력
            degree = st.number_input('각도 입력', 0, 359)
            
            # 2. 모든 이미지를 돌린다.
            rotated_img_list = []
            for img in image_list:
                rotated_img = img.rotate(degree)
                # rotated_img.save('data/rot.jpg')
                st.image(rotated_img)
                rotated_img_list.append(rotated_img)
            directory = st.text_input('파일 경로 입력')
            # 3. 파일저장
            if st.button('파일 저장'):
                for img in rotated_img_list:
                    save_uploaded_img(directory, img)


       
        elif option == 'Create Thumbnail':
            
            width = st.number_input('가로 입력', 1, img.size[0])
            height = st.number_input('세로 입력', 1, img.size[1])
            size = (width, height)
            # 코드 쓰고 확인하면서 점진적으로 하는 것을 애자일방식이라고 한다
            
            Created_img_list = []
            for img in image_list:
                # img.thumbnail(size): img자체를 바꿔주는거라 변수로 받지 않아도 된다
                img.thumbnail(size)
                st.image(img)
                Created_img_list.append(img)
            
            directory = st.text_input('파일 경로 입력')
            if st.button('파일 저장'):
                for img in Created_img_list:
                    save_uploaded_img(directory, img)



        elif option == 'Crop Image':
            # 영역 설정 / 좌상단부터 너비와 높이만큼 자른다
            # 좌상단 좌표: (50,100) / 너비와 높이:(200,200)
            
            st.write('너비와 높이는 x,y좌표보다 크게 입력하세요')
            box_x = st.number_input('x좌표 입력', 0, img.size[0]-1)
            box_y = st.number_input('y좌표 입력', 0, img.size[1]-1)
            # 선생님 예외처리(선생님 방식이 더 좋은 것 같다)
            max_width = img.size[0] - box_x
            max_height = img.size[1] - box_y
            box_width = st.number_input('너비 입력', 1, max_width)
            box_height = st.number_input('높이 입력', 1, max_height)
            # 내가 한거 ㅎ.. 안하는게 좋을덧..
            # if (box_width > (box_x or box_y)) and (box_height > (box_x or box_y)):
            box = (box_x, box_y, box_x + box_width, box_y + box_height)
            

            cropped_img_list = []
            for img in image_list:
                cropped_img = img.crop(box)
                st.image(cropped_img)
                cropped_img_list.append(cropped_img)
            
            directory = st.text_input('파일 경로 입력')
            if st.button('파일 저장'):
                for img in cropped_img_list:
                    save_uploaded_img(directory, img)





        elif option == 'Merge Images':
            merge_file = st.file_uploader('Upload Image', type=['png','jpg','jpeg'], key='merge')

            if merge_file is not None:
                merged_img = load_image(merge_file)
                    
                start_x = st.number_input('x좌표 입력', 0, img.size[0]-1)
                start_y = st.number_input('y좌표 입력', 0, img.size[1]-1)
                
                position = (start_x, start_y)
                
                merged_img_list = []
                for img in image_list:
                    img.paste(merged_img, position)
                    st.image(img)
                    merged_img_list.append(img)
                
                directory = st.text_input('파일 경로 입력')
                if st.button('파일 저장'):
                    for img in merged_img_list:
                        save_uploaded_img(directory, img)




                

        elif option == 'Flip Image':
            
            # 버튼
            # if st.button('좌우반전') : # 버튼이 눌렸을 경우
            #     flipped_img = img.transpose( Image.FLIP_LEFT_RIGHT )
            #     st.image(flipped_img)
            
            # if st.button('상하반전'):
            #     flipped_img = img.transpose( Image.FLIP_TOP_BOTTOM)
            #     st.image(flipped_img)            

            # 선생님은 radio로 만듦
            status = st.radio('플립 선택', ['좌우반전','상하반전'])
            
            flipped_img_list = []
            for img in image_list:
                if status == '좌우반전':
                    flipped_img = img.transpose( Image.FLIP_LEFT_RIGHT )
                elif status == '상하반전':
                    flipped_img = img.transpose( Image.FLIP_TOP_BOTTOM)
                
                st.image(flipped_img)
                flipped_img_list.append(flipped_img)
                
            directory = st.text_input('파일 경로 입력')
            if st.button('파일 저장'):
                for img in flipped_img_list:
                    save_uploaded_img(directory, img)
            
                    
                      


        elif option == 'Change Color':
            
            # # 버튼 L은 grayscale / 1은 흑백 / RGB는 컬러
            # if st.button('흑백') :
            #     bw = img.convert('1')
            #     st.image(bw)

            # if st.button('grayscale') :
            #     bw = img.convert('L')
            #     st.image(bw)


            # 선생님 방법
            status = st.radio('색 변경', ['Black & White','Grayscale','Color(RGB)'])
            if status == 'Color(RGB)':
                color = 'RGB'

            elif status == 'Black & White':
                color = '1'

            elif status == 'Grayscale':
                color = 'L'

            color_img_list = []
            for img in image_list:
                bw = img.convert(color)
                st.image(bw)
                color_img_list.append(bw)
            
            directory = st.text_input('파일 경로 입력')
            if st.button('파일 저장'):
                for img in color_img_list:
                    save_uploaded_img(directory, img)            
            


        elif option == 'Filters - Sharpen':
            
            Sharpen_img_list = []
            for img in image_list:
                sharp_img = img.filter(ImageFilter.SHARPEN)
                st.image(sharp_img)
                Sharpen_img_list.append(sharp_img)
            
            directory = st.text_input('파일 경로 입력')
            if st.button('파일 저장'):
                for img in Sharpen_img_list:
                    save_uploaded_img(directory, img)             



        elif option == 'Filters - Edge Enhance':
            Edge_img_list = []
            for img in image_list:
                edge_img = img.filter(ImageFilter.EDGE_ENHANCE)
                st.image(edge_img)
                Edge_img_list.append(edge_img)
            
            directory = st.text_input('파일 경로 입력')
            if st.button('파일 저장'):
                for img in Edge_img_list:
                    save_uploaded_img(directory, img) 


        elif option == 'Contrast Image':
            # 슬라이드
            contrast_num = st.slider('대조', 0, 10)

            Contrast_img_list = []
            for img in image_list:
                contrast_img = ImageEnhance.Contrast(img).enhance(contrast_num)
                st.image(contrast_img)
                Contrast_img_list.append(contrast_img)
            
            directory = st.text_input('파일 경로 입력')
            if st.button('파일 저장'):
                for img in Contrast_img_list:
                    save_uploaded_img(directory, img)             



# 버튼 안에서 디렉토리 받는 것은 streamlit이라서 할 수 없음 / 일반 프론트엔드 개발에서는 가능

# 3. 여러 파일을 변환할 수 있도록

if __name__ == '__main__':
    main()








