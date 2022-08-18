function bindCaptchaBtnClick(){
    $("#captcha-btn").on("click",function(event){
        var $this = $(this);
        var email = $("input[name='email']").val();
        if(!email){
            alert("請先輸入Email！");
            return;
        }

        $.ajax({
            url: "/user/captcha",
            method: "POST",
            data: {
                "email": email
            },
            success: function (res){
                var code = res['code'];
                if(code == 200){

                    $this.off("click");

                    var countDown = 30;
                    var timer = setInterval(function (){
                        countDown -= 1;
                        if(countDown > 0){
                            $this.text(countDown+"秒後重新發送");
                        }else{
                            $this.text("獲取驗證碼");

                            bindCaptchaBtnClick();

                            clearInterval(timer);
                        }
                    },1000);
                    alert("驗證碼發送成功！");
                }else{
                    alert(res['message']);
                }
            }
        })
    });
}



$(function () {
    bindCaptchaBtnClick();
});