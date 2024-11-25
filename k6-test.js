import http from "k6/http";
import { sleep } from "k6";

export let options = {
  vus: 19, // 동시 사용자 수
  iterations: 380, // 총 요청 수
};

export default function () {
  const baseUrl = "http://10.80.0.3/gen-img";

  // 요청 파라미터 설정
  const params = {
    prompt: `A beautiful landscape - ${__VU}-${__ITER}`,
    step: 25,
  };

  // URL에 쿼리 파라미터 추가
  const urlWithParams = `${baseUrl}?prompt=${encodeURIComponent(
    params.prompt
  )}&step=${params.step}`;

  // HTTP POST 요청
  const res = http.post(urlWithParams);

  // 응답 처리
  if (res.status === 200) {
    console.log(
      `[VU ${__VU} - ITER ${__ITER}] Success: Response Time ${res.timings.duration} ms`
    );
  } else {
    console.error(
      `[VU ${__VU} - ITER ${__ITER}] Failure: Status ${res.status}, Response Body: ${res.body}`
    );
  }

  // 요청 간 간격
  sleep(1); // 요청 간 대기 시간
}