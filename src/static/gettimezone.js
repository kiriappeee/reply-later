function getTimezoneInfo(){
    var d = new Date();
    var offSet = d.getTimezoneOffset() * -1;
    var hours = parseInt(offSet / 60);
    var minutes = (offSet/60)%1*60;
    return {hours: hours, minutes: minutes};
}
