import os
import re

def remove_prefix_and_number(directory, prefix):
    # 정규 표현식을 사용하여 접두사와 5자리 숫자를 포함한 패턴을 정의합니다.
    pattern = re.compile(rf"^{re.escape(prefix)}\d{{5}}_(.*)$")
    
    # 디렉토리의 모든 파일 리스트를 가져옵니다.
    files = os.listdir(directory)
    
    # 파일 리스트를 순회하며 파일 이름을 변경합니다.
    for filename in files:
        match = pattern.match(filename)
        if match:
            # 원래 파일 이름을 추출합니다.
            original_name = match.group(1)
            new_filename = original_name + os.path.splitext(filename)[1]
            # 파일 이름을 변경합니다.
            os.rename(os.path.join(directory, filename), os.path.join(directory, new_filename))


# 예시 사용법
directory_path = "D:/test"  # 여기에는 변경할 파일들이 있는 디렉토리 경로를 입력하세요.
prefix = "history_"  # 여기에는 추가할 접두사를 입력하세요.
remove_prefix_and_number(directory_path, prefix)
