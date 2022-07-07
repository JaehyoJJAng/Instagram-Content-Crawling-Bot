import json
import os.path
from pathlib import Path
from typing import Optional


BASE_DIR = Path(__file__).resolve().parent
JSON_FILE = os.path.join(BASE_DIR,'login_info.json')


def get_login_info(
        key: str,
        default_value: Optional[str] = None,
        json_path : str = JSON_FILE
):
    # Json 파일 읽어온 후 , 변수에 저장
    with open(JSON_FILE) as f :
        secret_data = f.read()

    # 불러온 JSON 파일을 , dict 형태로 형 변환
    secret_data = json.loads(secret_data)

    # return
    try:
        secret_data[key]
    except:
        if default_value:
            return default_value

        raise EnvironmentError(f'Set the {key} environment variable')