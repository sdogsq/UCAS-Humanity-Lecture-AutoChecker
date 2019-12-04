# UCAS-Humanity-Lecture-AutoChecker

可自动检查人文讲座及报名，若报名成功将以邮件形式通知。挂在服务器上运行效果良好。
较早前写的脚本，自用，代码比较乱。讲座已打卡完毕。

#### 使用方法

- 在参数`params_nocode`与`params_withcode`中填入SEP用户名及密码。

- 在参数`fromaddr`中填写发送邮件邮箱，`password`中填入邮箱密码，`toaddrs`中填入收信邮箱(可多个)。

- 参数`server`设置发送邮箱的SMTP服务器。

- 运行程序。若在UCAS内网运行无需输入验证码，若在外网运行，运行后会自动弹出验证码，输入即可。（此处感谢@xiaolalala 的提醒，在 onestop.ucas.ac.cn 登陆始终无需输入验证码，待改进）
