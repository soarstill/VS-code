import os

def add_prefix_and_number(directory, prefix):
    # 디렉토리의 모든 파일 리스트를 가져옵니다.
    files = os.listdir(directory)
    
    # 파일 리스트를 순회하며 파일 이름을 변경합니다.
    for i, filename in enumerate(files):
        # 파일의 확장자를 유지합니다.
        file_extension = os.path.splitext(filename)[1]
        original_name = os.path.splitext(filename)[0]
        
        # 새 파일 이름을 생성합니다. 일련번호는 5자리로 포맷팅됩니다.
        new_filename = f"{prefix}{i+1:05}_{original_name}{file_extension}"
        
        # 파일 이름을 변경합니다.
        os.rename(os.path.join(directory, filename), os.path.join(directory, new_filename))

# 예시 사용법
directory_path = "D:/test"  # 여기에는 변경할 파일들이 있는 디렉토리 경로를 입력하세요.
prefix = "history_"  # 여기에는 추가할 접두사를 입력하세요.
add_prefix_and_number(directory_path, prefix)
