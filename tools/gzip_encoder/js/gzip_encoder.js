const ENCODING = 'utf-8';
const MODE_ENCODE = 'encode';
const MODE_DECODE = 'decode';

function main(text, mode) {
  let result = ""
  if (mode === MODE_ENCODE) {
    result = gzip_encode(text);
  } else if (mode === MODE_DECODE) {
    result = gzip_decode(text);
  }
  return result;
}

function gzip_encode(text) {
  const input_bytes = new TextEncoder().encode(text);
  const gzip_bytes = pako.gzip(input_bytes);
  const base64_bytes = btoa(String.fromCharCode(...gzip_bytes));
  const output_text = base64_bytes;

  return output_text;
}

function gzip_decode(text) {
  const input_bytes = new Uint8Array(
    atob(text).split('').map((char) => char.charCodeAt(0))
  );
  const output_bytes = pako.ungzip(input_bytes);
  const output_text = new TextDecoder().decode(output_bytes);

  return output_text;
}
