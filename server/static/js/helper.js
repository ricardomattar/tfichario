
function callserver(callback_func, user_name, pw, pr) {
  var ts;
  var password_hash;
  ts = Math.floor(Date.now() / 1000).toString();
  password_hash = CryptoJS.SHA1(pw).toString();
  hash = CryptoJS.SHA1(ts + pr + password_hash).toString();

  $.post("/brv1",
    {
      timestamp: ts,
      username: user_name,
      hmac: hash,
      params: pr
    },callback_func);
}
