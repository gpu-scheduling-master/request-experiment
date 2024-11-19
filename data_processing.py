import statistics

metrics_data = {}
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
