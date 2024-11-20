import requests
import time
from concurrent.futures import ThreadPoolExecutor

# Istio Gateway 엔드포인트
gateway_url = "http://istio-gateway-service/api"


# 요청 전송 함수
def send_request(node_url, request_id):
    payload = {"prompt": f"a photograph of an astronaut riding a horse - {request_id}"}
    try:
        response = requests.post(node_url, json=payload)
        print(f"Request ID {request_id} sent to {node_url}: Status {response.status_code}")
    except Exception as e:
        print(f"Error sending request {request_id} to {node_url}: {e}")


# 균일 요청 패턴
def uniform_requests(total_requests, interval):
    for request_id in range(total_requests):
        send_request(gateway_url, request_id)
        time.sleep(interval)


# 몰림 요청 패턴
def burst_requests(total_requests, burst_size, interval_between_bursts):
    with ThreadPoolExecutor(max_workers=burst_size) as executor:
        for i in range(0, total_requests, burst_size):
            # 현재 burst 그룹에서 요청 전송
            for request_id in range(i, min(i + burst_size, total_requests)):
                executor.submit(send_request, gateway_url, request_id)
            # 각 burst 그룹 간 간격
            time.sleep(interval_between_bursts)


# 요청 시나리오 실행 함수
def generate_requests(scenario, total_requests, interval=None, burst_size=None, interval_between_bursts=10):
    if scenario == "uniform":
        print("Starting uniform requests...")
        uniform_requests(total_requests, interval)
    elif scenario == "burst":
        print("Starting burst requests...")
        burst_requests(total_requests, burst_size, interval_between_bursts)
    else:
        print("Invalid scenario. Choose 'uniform' or 'burst'.")


# 요청 시나리오 실행
scenario = "burst"  # "uniform" 또는 "burst"
total_requests = 100  # 총 요청 수
interval = 1  # 요청 간격 (초) (균일 요청에 사용)
burst_size = 10  # 동시에 보낼 요청 수 (몰림 요청에 사용)
interval_between_bursts = 2  # 각 burst 간 간격 (초)

# generate_requests(scenario, total_requests, interval, burst_size)
generate_requests(scenario, total_requests, burst_size=burst_size, interval_between_bursts=interval_between_bursts)

