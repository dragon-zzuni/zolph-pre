from google.cloud import aiplatform

# 프로젝트 ID와 리전을 변경하세요
project_id = "gen-lang-client-0723754498"
region = "asia-northeast3"

def test_vertex_ai():
    aiplatform.init(project=project_id, location=region)
    # 모델 목록 가져오기와 같은 간단한 작업 수행
    models = aiplatform.Model.list(filter="name = 'my-model-name'")
    print(f"모델 목록: {models}")

test_vertex_ai() 
