// KISM-BOILERPLATE: Demo frontend, polls the app's /hello/ endpoint with a client generated from its OpenAPI schema.
// The sdk in ./generated is generated from the running app's schema, regenerate with `bun run codegen` after any api
// change. A renamed endpoint or a changed response model then fails `bun run check`.
import { getHello } from "../generated";

const field = document.getElementById("MY_COOL_FIELD")!;
const result = document.getElementById("MY_COOL_RESULT")!;

function show(ok: boolean, msg: string): void {
  field.textContent = ok ? "API SUCCESS" : "API FAILURE";
  result.textContent = msg;
  result.style.color = ok ? "#008000" : "#800000";
}

async function poll(): Promise<void> {
  try {
    // AbortSignal.timeout() is native, no AbortController/setTimeout/clearTimeout dance needed.
    const { data, response } = await getHello({ signal: AbortSignal.timeout(1000) });

    if (data) {
      show(true, data.msg); // data is typed as MessageResponse, so .msg is a string.
    } else {
      // Non 2xx leaves data undefined, network failures and the timeout leave response undefined too.
      show(false, response ? `${response.status}` : "Fetch Error");
    }
  } catch (error) {
    console.error(error); // Belt and braces, the client returns rather than throws for the cases above.
    show(false, "Fetch Error");
  }
}

void poll(); // Call on page load, setInterval waits for the interval before its first call.
setInterval(poll, 5000);
