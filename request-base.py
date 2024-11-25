import requests
import time
from concurrent.futures import ThreadPoolExecutor

# Istio Gateway 엔드포인트
gateway_url = "http://10.80.0.3/gen-img"  # Istio Gateway URL

# Make Span 및 응답 시간 기록 변수
start_time = None
end_time = None
response_times = []  # 각 요청에 대한 응답 시간 기록


# 요청 전송 함수
def send_request(request_id):
    global end_time, response_times
    request_start = time.time()  # 요청 시작 시간 기록
    params = {"prompt": f"A beautiful landscape - {request_id}", "step": 25}  # 쿼리 파라미터
    try:
        # 파일 저장을 위한 스트림 요청
        response = requests.post(gateway_url, params=params, stream=True)
        request_end = time.time()  # 요청 완료 시간 기록
        response_time = request_end - request_start
        response_times.append(response_time)  # 응답 시간 기록

        if response.status_code == 200:
            # 결과를 파일로 저장
            with open(f"generated_image_{request_id}.png", "wb") as file:
                for chunk in response.iter_content(chunk_size=8192):
                    file.write(chunk)
            print(f"Request ID {request_id} succeeded: Status {response.status_code}, Response Time: {response_time:.2f}s")
        else:
            print(f"Request ID {request_id} failed: Status {response.status_code}, Response Time: {response_time:.2f}s")

        # 마지막 요청 응답 시간 업데이트
        end_time = request_end
    except Exception as e:
        print(f"Error sending request {request_id}: {e}")


# 균일 요청 패턴
def uniform_requests(total_requests, interval):
    global start_time
    start_time = time.time()  # 요청 시작 시간 기록
    for request_id in range(total_requests):
        send_request(request_id)
        time.sleep(interval)


# 몰림 요청 패턴
def burst_requests(total_requests, burst_size, interval_between_bursts):
    global start_time
    start_time = time.time()  # 요청 시작 시간 기록
    with ThreadPoolExecutor(max_workers=burst_size) as executor:
        for i in range(0, total_requests, burst_size):
            # 현재 burst 그룹에서 요청 전송
            for request_id in range(i, min(i + burst_size, total_requests)):
                executor.submit(send_request, request_id)
            # 각 burst 그룹 간 간격
            time.sleep(interval_between_bursts)


# 응답 시간 통계 계산 함수
def calculate_response_time_stats():
    if response_times:
        avg_time = sum(response_times) / len(response_times)
        min_time = min(response_times)
        max_time = max(response_times)
        print(f"Response Time Stats - Avg: {avg_time:.2f}s, Min: {min_time:.2f}s, Max: {max_time:.2f}s")
    else:
        print("No response times recorded.")


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

    # Make Span 계산
    if start_time and end_time:
        make_span = end_time - start_time
        print(f"Make Span: {make_span:.2f} seconds")

    # 응답 시간 통계 출력
    calculate_response_time_stats()


# 요청 시나리오 실행
scenario = "uniform"  # "uniform" 또는 "burst"
total_requests = 10  # 총 요청 수
interval = 1  # 요청 간격 (초) (균일 요청에 사용)
burst_size = 5  # 동시에 보낼 요청 수 (몰림 요청에 사용)
interval_between_bursts = 2  # 각 burst 간 간격 (초)

generate_requests(scenario, total_requests, interval=interval, burst_size=burst_size, interval_between_bursts=interval_between_bursts)
