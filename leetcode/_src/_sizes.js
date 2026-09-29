const fs = require('fs');
const base = 'D:/wx/springai/leetcode/_src/';
for (const c of ['ch05','ch06','ch07','ch08']) {
  const f = base + c + '.part';
  const s = fs.readFileSync(f, 'utf8');
  fs.appendFileSync(base + '_sizes_out.txt', c + ' ' + s.length + 'B ' + s.split('\n').length + 'L\n');
}
