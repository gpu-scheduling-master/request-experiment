import requests
import datetime

prometheus_url = "http://<prometheus-server>/api/v1/query_range"

# Prometheus 쿼리 함수
def query_prometheus(query, start_time, end_time, step):
    params = {
        "query": query,
        "start": start_time,
        "end": end_time,
        "step": step
    }
    response = requests.get(f"{prometheus_url}", params=params)
    if response.status_code == 200:
        return response.json()["data"]["result"]
    else:
        print(f"Error querying Prometheus: {response.status_code}, {response.text}")
        return None

# 시간 범위 설정
start_time = (datetime.datetime.utcnow() - datetime.timedelta(minutes=30)).isoformat() + "Z"
end_time = datetime.datetime.utcnow().isoformat() + "Z"
step = "30s"

# 메트릭 쿼리 예제
queries = {
    "request_duration": "request_duration_seconds",  # 요청 처리 시간
    "gpu_utilization": "node_gpu_utilization",  # GPU 사용률
    "node_traffic": "node_request_count"  # 노드별 요청 수
}

# 각 메트릭에 대한 데이터 가져오기
metrics_data = {}
for name, query in queries.items():
    metrics_data[name] = query_prometheus(query, start_time, end_time, step)

# 결과 출력
for name, data in metrics_data.items():
    print(f"Data for {name}: {data}")

# ========================================================================================

import statistics

# 응답 시간 편차 계산
def calculate_response_time_variance(request_duration_data):
    if request_duration_data:
        response_times = [float(v["value"][1]) for v in request_duration_data]
        return statistics.variance(response_times)
    return None

time_variance = calculate_response_time_variance(metrics_data["request_duration"])
print(f"Response Time Variance: {time_variance}")


# Make Span 계산
def calculate_make_span(request_duration_data):
    if request_duration_data:
        start_times = [float(v["value"][0]) for v in request_duration_data]
        return max(start_times) - min(start_times)
    return None

make_span = calculate_make_span(metrics_data["request_duration"])
print(f"Make Span: {make_span} seconds")

# GPU 사용률 분석
def analyze_gpu_utilization(gpu_data):
    if gpu_data:
        utilizations = [float(v["value"][1]) for v in gpu_data]
        avg_utilization = sum(utilizations) / len(utilizations)
        max_utilization = max(utilizations)
        min_utilization = min(utilizations)
        return avg_utilization, max_utilization, min_utilization
    return None, None, None

avg_gpu, max_gpu, min_gpu = analyze_gpu_utilization(metrics_data["gpu_utilization"])
print(f"GPU Utilization - Avg: {avg_gpu}, Max: {max_gpu}, Min: {min_gpu}")


# 노드별 트래픽 분배 분석
def analyze_node_traffic(node_traffic_data):
    if node_traffic_data:
        traffic_counts = {v["metric"]["instance"]: int(v["value"][1]) for v in node_traffic_data}
        return traffic_counts
    return None

node_traffic = analyze_node_traffic(metrics_data["node_traffic"])
print(f"Node Traffic Distribution: {node_traffic}")

import pandas as pd
import matplotlib.pyplot as plt

# 예제: GPU 사용률 시각화
utilization_df = pd.DataFrame(metrics_data["gpu_utilization"])
utilization_df.plot(x="timestamp", y="value", kind="line")
plt.title("GPU Utilization Over Time")
plt.xlabel("Time")
plt.ylabel("GPU Utilization")
plt.show()
