// KISM-BOILERPLATE: Demo frontend, polls the app's /hello/ endpoint with a client typed from its OpenAPI schema.
import createClient from "openapi-fetch";
import type { paths } from "./generated/openapi";

// 'paths' is generated from the running app's schema, regenerate with `bun run codegen` whenever the api changes.
// The client checks the url against it, so a renamed endpoint or a changed response model fails `bun run check`.
const api = createClient<paths>();

const field = document.getElementById("MY_COOL_FIELD")!;
const result = document.getElementById("MY_COOL_RESULT")!;

function show(ok: boolean, msg: string): void {
  field.textContent = ok ? "API SUCCESS" : "API FAILURE";
  result.textContent = msg;
  result.style.color = ok ? "#008000" : "#800000";
}

async function getHello(): Promise<void> {
  try {
    // AbortSignal.timeout() is native, no AbortController/setTimeout/clearTimeout dance needed.
    const { data, response } = await api.GET("/hello/", { signal: AbortSignal.timeout(1000) });

    if (data) {
      show(true, data.msg); // data is typed as MessageResponse, so .msg is a string.
    } else {
      show(false, `${response.status}`); // Non 2xx, openapi-fetch leaves data undefined.
    }
  } catch (error) {
    // Network failures and the timeout throw rather than returning a response.
    console.error(error);
    show(false, error instanceof DOMException && error.name === "TimeoutError" ? "Fetch Timeout" : "Fetch Error");
  }
}

void getHello(); // Call on page load, setInterval waits for the interval before its first call.
setInterval(getHello, 5000);
