const fs = require('fs');
const base = 'D:/wx/springai/leetcode/_src/';
let out = '';
for (const c of ['ch05','ch06','ch07','ch08']) {
  const buf = fs.readFileSync(base + c + '.part');
  out += c + ' ' + buf.length + ' bytes ' + buf.toString('utf8').split('\n').length + ' lines\n';
}
fs.writeFileSync(base + '_sz_out.txt', out);
