function bindEmailCaptchaClick() {
  $("#captcha-btn").click(function (event) {
    var $this = $("#captcha-btn"); // 将当前按钮转换为jQuery对象
    event.preventDefault();

    var email = $("input[name='email']").val();

    $.ajax({
      url: "/auth/captcha/email?email=" + email,
      method: "GET",
      success: function (result) {
        var code = result["code"];
        if (code == 200) {
          var countdown = 60;
          $this.text(countdown + " 秒后重试"); // 立即更新按钮文本
          var timer = setInterval(function () {
            countdown -= 1;
            if (countdown > 0) {
              $this.text(countdown + " 秒后重试");
            } else {
              clearInterval(timer); // 停止定时器
              $this.text("获取验证码"); // 恢复按钮文本
            }
          }, 1000);
        } else {
          alert(result["message"]);
        }
      },
      error: function (xhr, status, errorMsg) {
        console.error("Error: " + errorMsg);
        console.log("Response text: " + xhr.responseText);
      },
    });
  });
}

$(function () {
  bindEmailCaptchaClick();
});
