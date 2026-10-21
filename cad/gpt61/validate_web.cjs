// Khronos validator, kept local to this package. No external-resource access.
const fs = require('fs');
const path = require('path');
const validator = require('./tmp/web-validator/node_modules/gltf-validator');
(async () => {
  const reports = {available: true, validator: 'Khronos glTF Validator', version: validator.version(), models: {}};
  for (const name of ['dart', 'harness', 'aircraft', 'stake']) {
    const file = path.join(__dirname, 'web', name + '.glb');
    const report = await validator.validateBytes(new Uint8Array(fs.readFileSync(file)), {uri: name + '.glb', maxIssues: 2000});
    reports.models[name] = report;
    console.log('KHRONOS', name, 'errors', report.issues.numErrors, 'warnings', report.issues.numWarnings, 'infos', report.issues.numInfos);
  }
  fs.writeFileSync(path.join(__dirname, 'web', 'validation-khronos.json'), JSON.stringify(reports, null, 2) + '\n');
  if (Object.values(reports.models).some(r => r.issues.numErrors)) process.exitCode = 1;
})().catch(e => { console.error(e); process.exitCode = 1; });
