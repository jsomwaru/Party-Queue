const { watch } = require('gulp');
const {execSync} = require('child_process')

function build(cb) {
    execSync("npm run build"); 
    cb();
}

exports.default = function() {
    watch(["src/**/*.js", "src/**/*.vue"], build)
}
