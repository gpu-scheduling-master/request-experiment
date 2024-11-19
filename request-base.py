import requests
import random
import time

# 노드 API 엔드포인트 목록
nodes = [
    "http://node1-stable-diffusion-service/api",
    "http://node2-stable-diffusion-service/api",
    "http://node3-stable-diffusion-service/api"
]

# 요청 시나리오 설정
def generate_requests(scenario, total_requests, interval):
    if scenario == "random_uniform":
        # 랜덤으로 모든 노드에 균등 분배
        for _ in range(total_requests):
            target_node = random.choice(nodes)
            send_request(target_node)
            time.sleep(interval)
    elif scenario == "skewed":
        # 특정 노드에 편중된 요청 (80% 특정 노드, 20% 다른 노드)
        weights = [0.8, 0.1, 0.1]  # 요청 분배 비율
        for _ in range(total_requests):
            target_node = random.choices(nodes, weights=weights)[0]
            send_request(target_node)
            time.sleep(interval)

# 요청 전송 함수
def send_request(node_url):
    payload = {"prompt": "a photograph of an astronaut riding a horse"}
    try:
        response = requests.post(node_url, json=payload)
        print(f"Request sent to {node_url}: Status {response.status_code}")
    except Exception as e:
        print(f"Error sending request to {node_url}: {e}")

# 요청 시나리오 실행
scenario = "random_uniform"  # 또는 "skewed"
total_requests = 100  # 총 요청 수
interval = 1  # 요청 간격 (초)
generate_requests(scenario, total_requests, interval)
