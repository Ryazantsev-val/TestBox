var isSecurityInstanceFound = false;
var securityInstance;

rpc.exports = {
    getsecsign: function (data) {
        return new Promise(function (resolve) {
            Java.perform(function () {
                resolve(securityInstance.signData(String(data)));
            });
        });
    }
}

Java.perform(function () {
    send("Inside java perform function");
    securityInstance = Java.use("ru.ryazantsev.blacktestbox.UtilKt");
    send("script loaded")
});