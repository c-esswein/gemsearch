const results = [];


function flattenRes() {
  const rows = [];
  Object.keys(results).forEach((embedding, i) => {
    const res = results[embedding];
    for (evalFunc in res) {
      res[evalFunc]['embedding'] = embedding;
      res[evalFunc]['rec_method'] = evalFunc;
      rows.push(res[evalFunc]);
    }      
  });
  return rows;
}

function flattenResLocal() {
  const rows = [];
  results.forEach((keyedRes, i) => {
    const row = keyedRes['values'];
    row['embedding'] = 'default';
    
    // extract precisin @ N
    row['prec+recall@'] = keyedRes['key'].match(/[a-z_]+@([0-9]+)/i)[1];

    row['rec_method'] = keyedRes['key'].replace('@' + row['prec+recall@'], '');
    rows.push(row);
  });
  return rows;
}

// polyfill for Object.values
function objectValues(obj) {
  const arr = [];
  for (key in obj) {
    arr.push(obj[key]);
  }
  return arr;
}

var fs = require('fs');
function writeResultsAt(resRows, precisionAt = 'all') {
  const output = [];

  resRows.forEach((res, i) => {
    // export header row
    if (i === 0) {
      output.push(Object.keys(res).join(';'));
    }

    if ((precisionAt === 'all') || res['rec_method'].endsWith('@' + precisionAt)) {
      output.push(objectValues(res).join(';'));
    }

  });

  writeArrToFile(output, 'rec_result-at_' + precisionAt + '.csv');
}

function writeArrToFile(arr, fileName) {
  // write to file
  let fileContent = arr.join('\n').replace(/\./g, ',');
  fs.writeFile(fileName, fileContent, function (err) {
    if (err) {
      return console.log(err);
    }

    console.log("The file was saved!");
  });
}


// const resRows = flattenRes();
const resRows = flattenResLocal();
sortedRows = resRows.sort((resA, resB) => resB['precision'] - resA['precision']);

writeResultsAt(sortedRows, 'all');
/* writeResultsAt(sortedRows, 1);
writeResultsAt(sortedRows, 10); */

const methodMap = {};
resRows.forEach((res) => {
  if (!methodMap[res['rec_method']]) {
    methodMap[res['rec_method']] = [];
  }

  const precAt = parseInt(res['prec+recall@'], 10);
  methodMap[res['rec_method']][precAt] = res['recall'];
   // methodMap[res['rec_method']][precAt] = parseInt(res['has_hits'], 10) / 2324;
});


const precAtArr = [1, 10, 15];
const resArr = [[
  // 'method', 0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 15
  'method', ...precAtArr
].join(';')];
Object.keys(methodMap).forEach((methodName, i) => {
  resRowData = [methodName];
  precAtArr.forEach(precAt => {
    resRowData.push(methodMap[methodName][precAt]);
  });
  resArr.push(resRowData.join(';'));
});


writeArrToFile(resArr, 'graph.csv');
